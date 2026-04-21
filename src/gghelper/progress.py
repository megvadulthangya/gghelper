"""Persistent run statistics for gghelper (``progress.json``)."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

from gghelper import i18n
from gghelper.config import get_progress_path


def read_progress() -> Dict[str, Any]:
    path = get_progress_path()
    if not path.exists():
        return {"runs": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except (json.JSONDecodeError, OSError):
        return {"runs": []}
    data.setdefault("runs", [])
    return data


def write_progress(data: Dict[str, Any]) -> None:
    path = get_progress_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def record_run(
    branch: str | None,
    commit_msg_length: int,
    had_conflict: bool,
    success: bool = True,
) -> None:
    data = read_progress()
    data["runs"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "branch": branch,
            "commit_msg_length": commit_msg_length,
            "had_conflict": had_conflict,
            "success": success,
        }
    )
    write_progress(data)


def show_stats(lang: str = "en") -> int:
    from gghelper.config import read_config

    data = read_progress()
    runs = data.get("runs", [])
    config = read_config()

    print()
    print(i18n.msg("stats_header", lang))

    if not runs:
        print(i18n.msg("stats_none_yet", lang))
    else:
        total = len(runs)
        successful = sum(1 for r in runs if r.get("success"))
        conflicts = sum(1 for r in runs if r.get("had_conflict"))
        last_run = runs[-1].get("timestamp", "N/A")

        print(f"{i18n.msg('stats_total_runs', lang)}{total}")
        print(f"{i18n.msg('stats_successful_runs', lang)}{successful}")
        print(f"{i18n.msg('stats_conflicts', lang)}{conflicts}")
        print(f"{i18n.msg('stats_last_run', lang)}{last_run}")

    print(f"{i18n.msg('stats_language', lang)}{config.get('language', 'auto')}")
    print(f"{i18n.msg('stats_level', lang)}{config.get('level', 'auto')}")
    return 0
