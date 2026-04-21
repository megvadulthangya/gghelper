"""Watch multiple repositories for remote changes and notify."""

from __future__ import annotations

import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any, Dict

from gghelper import i18n
from gghelper.git_ops import check_remote_correctly


def watch_repos(config: Dict[str, Any], interval: int = 300, lang: str = "en") -> int:
    repos = config.get("watched_repos", [])
    if not repos:
        print(i18n.msg("watch_no_repos", lang))
        from gghelper.tui.watch_config import run_watch_config

        return run_watch_config(lang=lang)

    print(i18n.msg("watch_running", lang).format(count=len(repos), interval=interval))
    try:
        while True:
            for repo_path in repos:
                check_single_repo(Path(repo_path), lang=lang)
            time.sleep(interval)
    except KeyboardInterrupt:
        print()
        print(i18n.msg("watch_stopped", lang))
    return 0


def check_single_repo(repo_path: Path, lang: str = "en") -> None:
    if not repo_path.exists():
        return

    previous_cwd = os.getcwd()
    try:
        os.chdir(repo_path)
        status = check_remote_correctly()
    finally:
        os.chdir(previous_cwd)

    if status in {"remote-ahead", "diverged"}:
        name = repo_path.name
        print(i18n.msg("watch_status_line", lang).format(name=name, status=status))
        send_notification(repo_path, status, lang=lang)


def send_notification(repo_path: Path, status: str, lang: str = "en") -> None:
    title = i18n.msg("watch_notification_title", lang).format(name=repo_path.name)
    body = i18n.msg("watch_notification_body", lang).format(status=status)

    system = platform.system()
    try:
        if system == "Linux":
            subprocess.run(["notify-send", title, body], check=False)
        elif system == "Darwin":
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'display notification "{body}" with title "{title}"',
                ],
                check=False,
            )
    except (OSError, subprocess.SubprocessError):
        # Best-effort: if the notification system is missing, fall back to
        # stdout only.
        pass
