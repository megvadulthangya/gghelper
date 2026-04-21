"""Commit-message prompting and convention checking."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from typing import Optional

from gghelper import i18n

_GENERIC_PATTERNS = re.compile(
    r"^(update|updates|fix|fixes|change|changes|wip|asdf|test|tmp|todo|stuff|commit|\.|-)$",
    re.IGNORECASE,
)


def _is_generic(message: str) -> bool:
    first_line = message.splitlines()[0].strip() if message else ""
    return bool(_GENERIC_PATTERNS.match(first_line))


def _print_conventional_examples(lang: str, level: str) -> None:
    examples = i18n.level_msg("conventional_commit_examples", lang, level)
    if not examples:
        return
    print(i18n.msg("commit_conventional_header", lang))
    print(examples)


def _check_message_quality(message: str, lang: str) -> bool:
    """Print warnings about the message. Returns True if user wants to re-enter."""
    short = len(message.strip()) < 10
    generic = _is_generic(message)

    if not (short or generic):
        return False

    if short:
        print(i18n.msg("commit_too_short", lang))
    if generic:
        print(i18n.msg("commit_generic", lang))

    try:
        choice = input(i18n.msg("commit_retry_prompt", lang)).strip().lower()
    except EOFError:
        return False
    return choice in {"y", "i", "yes", "igen"}


def get_commit_message(lang: str = "en", level: str = "intermediate") -> Optional[str]:
    """Prompt the user for a commit message.

    Returns the final message, or None if the user cancelled.
    """
    while True:
        _print_conventional_examples(lang, level)

        print()
        print(i18n.msg("commit_prompt_header", lang))
        print(i18n.msg("commit_prompt_hint_type", lang))
        print(i18n.msg("commit_prompt_hint_finish", lang))
        print(i18n.msg("commit_prompt_hint_cancel", lang))
        print("-" * 50)

        lines = []
        try:
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
        except KeyboardInterrupt:
            print()
            print(i18n.msg("cancelled", lang))
            return None

        message = "\n".join(lines).strip()
        if not message:
            print(i18n.msg("commit_empty_error", lang))
            return None

        confirmed = _confirm_or_edit(message, lang)
        if confirmed is None:
            return None
        message = confirmed

        # Convention checks (after final message is decided).
        if _check_message_quality(message, lang):
            continue
        return message


def _confirm_or_edit(message: str, lang: str) -> Optional[str]:
    while True:
        print()
        print(i18n.msg("commit_preview_header", lang))
        print("-" * 50)
        print(message)
        print("-" * 50)

        try:
            choice = input(i18n.msg("commit_confirm_prompt", lang)).strip().lower()
        except EOFError:
            choice = "n"

        if choice in {"y", "i", "yes", "igen"}:
            return message
        if choice in {"e", "edit", "szerkeszt"}:
            edited = _edit_in_editor(message, lang)
            if edited is None:
                return None
            message = edited
            continue
        if choice in {"n", "no", "nem"}:
            print(i18n.msg("cancelled", lang))
            return None


def _edit_in_editor(message: str, lang: str) -> Optional[str]:
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(message)
            temp_path = f.name

        editor = os.getenv("EDITOR", "nano")
        subprocess.run([editor, temp_path], check=False)

        with open(temp_path, "r", encoding="utf-8") as f:
            edited = f.read().strip()
    except OSError as exc:
        print(i18n.msg("commit_edit_error", lang) + str(exc))
        return message
    finally:
        try:
            os.unlink(temp_path)  # type: ignore[name-defined]
        except Exception:
            pass

    if not edited:
        print(i18n.msg("commit_edit_empty", lang))
        return None
    return edited
