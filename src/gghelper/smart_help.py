"""Contextual help based on the current repo state."""

from __future__ import annotations

from gghelper import i18n
from gghelper.git_ops import (
    check_remote_correctly,
    get_git_status_short,
    get_recent_log,
    is_git_repo,
)


def smart_help(lang: str = "en", level: str = "intermediate") -> int:
    print()
    print(i18n.msg("smart_help_header", lang))

    if not is_git_repo():
        print(i18n.msg("smart_help_not_repo", lang))
        return 0

    remote_status = check_remote_correctly()
    changes = get_git_status_short()

    if changes:
        print(i18n.msg("smart_help_uncommitted", lang))

    if remote_status == "remote-ahead":
        print(i18n.msg("smart_help_remote_ahead", lang))
    elif remote_status == "local-ahead":
        print(i18n.msg("smart_help_local_ahead", lang))
    elif remote_status == "diverged":
        print(i18n.msg("smart_help_diverged", lang))
    elif remote_status == "up-to-date" and not changes:
        print(i18n.msg("smart_help_up_to_date", lang))

    log_lines = get_recent_log(5)
    if log_lines:
        print()
        print(i18n.msg("smart_help_recent_log", lang))
        for line in log_lines:
            print(f"  {line}")

    return 0
