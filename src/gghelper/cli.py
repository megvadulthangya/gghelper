"""Command-line entry point for gghelper."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from gghelper import __version__, i18n
from gghelper.config import detect_language, get_config_path, get_level, read_config, write_config


HELP_TEXT = """
gghelper v{version} - Git Workflow Mentor

USAGE:
  gghelper                      # Interactive commit and push
  gghelper --resolve-only       # Only resolve conflicts
  gghelper --safe               # Use merge instead of rebase
  gghelper --dry-run            # Preview actions without executing
  gghelper --lang hu            # Hungarian for this run
  gghelper --lang en            # English for this run
  gghelper --level novice       # Detailed explanations
  gghelper --level intermediate # Moderate explanations
  gghelper --level expert       # Minimal explanations

CONFIGURATION:
  gghelper --set-lang hu        # Set Hungarian permanently
  gghelper --set-lang en        # Set English permanently
  gghelper --set-level novice   # Persist novice level
  gghelper --set-level expert   # Persist expert level

WATCH MODE:
  gghelper --watch              # Watch configured repos for remote changes
  gghelper --watch --interval 60  # Poll every 60 seconds (default 300)
  gghelper --watch-config       # Open the TUI to pick repos to watch

INFORMATION:
  gghelper --help               # Show this help
  gghelper --smart-help         # Contextual help
  gghelper --stats              # Usage statistics
  gghelper --version            # Version info
"""


def parse_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="gghelper",
        description="gghelper - Git Workflow Mentor",
        add_help=False,
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--resolve-only", action="store_true", help="Only resolve conflicts")
    parser.add_argument("--safe", action="store_true", help="Use merge instead of rebase")
    parser.add_argument("--lang", choices=list(i18n.SUPPORTED_LANGS), help="Force language")
    parser.add_argument(
        "--level",
        choices=list(i18n.LEVELS),
        help="Learning level",
    )
    parser.add_argument("--set-lang", choices=list(i18n.SUPPORTED_LANGS), help="Persist default language")
    parser.add_argument(
        "--set-level",
        choices=list(i18n.LEVELS),
        help="Persist default learning level",
    )
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--smart-help", action="store_true", help="Show contextual help")
    parser.add_argument("--stats", action="store_true", help="Show usage statistics")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--watch", action="store_true", help="Watch configured repos")
    parser.add_argument("--watch-config", action="store_true", help="Configure watched repos (TUI)")
    parser.add_argument("--interval", type=int, default=300, help="Watch poll interval in seconds")
    return parser.parse_args(argv)


def _handle_set_config(args: argparse.Namespace, lang: str) -> int:
    config = read_config()
    if args.set_lang:
        config["language"] = args.set_lang
        print(i18n.msg("cfg_language_set", lang) + args.set_lang)
    if args.set_level:
        config["level"] = args.set_level
        print(i18n.msg("cfg_level_set", lang) + args.set_level)
    write_config(config)

    print()
    print(i18n.msg("cfg_current_header", lang))
    for key, value in config.items():
        print(f"   {key}: {value}")
    print()
    print(i18n.msg("cfg_saved_to", lang) + str(get_config_path()))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_arguments(argv)
    lang = detect_language(args)

    if args.set_lang or args.set_level:
        return _handle_set_config(args, lang)

    if args.help:
        print(HELP_TEXT.format(version=__version__))
        return 0

    if args.version:
        print(f"gghelper v{__version__}")
        return 0

    config = read_config()
    level = get_level(config, args)

    if args.stats:
        from gghelper.progress import show_stats

        return show_stats(lang=lang)

    if args.smart_help:
        from gghelper.smart_help import smart_help

        return smart_help(lang=lang, level=level)

    if args.watch_config:
        from gghelper.tui.watch_config import run_watch_config

        return run_watch_config(lang=lang)

    if args.watch:
        from gghelper.watch import watch_repos

        return watch_repos(config, interval=args.interval, lang=lang)

    from gghelper.workflow import main_workflow

    try:
        return main_workflow(args, lang=lang, level=level)
    except KeyboardInterrupt:
        print()
        print(i18n.msg("cancelled_by_user", lang))
        return 1
    except Exception as exc:  # noqa: BLE001 - surface unexpected errors to user
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
