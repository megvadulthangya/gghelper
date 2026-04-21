"""Configuration persistence for gghelper."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path.home() / ".config" / "gghelper"


def get_config_path() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR / "config.json"


def get_progress_path() -> Path:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR / "progress.json"


def read_config() -> Dict[str, Any]:
    path = get_config_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except (json.JSONDecodeError, OSError):
        return {}


def write_config(config: Dict[str, Any]) -> None:
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def detect_language(args) -> str:
    """Resolve effective language from CLI args > config > env > default."""
    if getattr(args, "lang", None):
        return args.lang

    config = read_config()
    if "language" in config:
        return config["language"]

    lang_env = os.getenv("LANG", "en_US.UTF-8").split("_")[0].lower()
    return "hu" if lang_env == "hu" else "en"


def get_level(config: Dict[str, Any], args) -> str:
    """Resolve effective learning level."""
    args_level = getattr(args, "level", None)
    if args_level:
        return args_level
    return config.get("level", "auto")
