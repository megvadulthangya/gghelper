"""Textual-based TUI for selecting watched repositories (Nord theme)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from gghelper import i18n
from gghelper.config import read_config, write_config

try:
    from textual.app import App, ComposeResult
    from textual.containers import VerticalScroll
    from textual.widgets import Button, Checkbox, Footer, Header, Static

    HAS_TEXTUAL = True
except ImportError:
    HAS_TEXTUAL = False


def discover_git_repos(root: Path | None = None, max_depth: int = 6) -> List[Path]:
    root = root or Path.home()
    try:
        result = subprocess.run(
            [
                "find",
                str(root),
                "-maxdepth",
                str(max_depth),
                "-type",
                "d",
                "-name",
                ".git",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []

    repos: List[Path] = []
    for line in result.stdout.splitlines():
        git_dir = Path(line)
        if git_dir.name == ".git":
            repos.append(git_dir.parent)
    repos.sort()
    return repos


def run_watch_config(lang: str = "en") -> int:
    if not HAS_TEXTUAL:
        print(i18n.msg("watch_textual_missing", lang))
        print(i18n.msg("watch_textual_fallback", lang))
        return 1

    app = WatchConfigApp(lang=lang)
    app.run()
    return 0


if HAS_TEXTUAL:

    class WatchConfigApp(App):
        CSS = """
        Screen { background: #2e3440; color: #d8dee9; }
        Header { background: #3b4252; color: #88c0d0; }
        Footer { background: #3b4252; color: #88c0d0; }
        Checkbox { color: #88c0d0; }
        Checkbox:focus { color: #81a1c1; }
        Button { background: #5e81ac; color: #eceff4; }
        Button:hover { background: #81a1c1; }
        VerticalScroll { border: round #4c566a; padding: 1; }
        """

        def __init__(self, lang: str = "en") -> None:
            super().__init__()
            self.lang = lang
            self.repos: List[Path] = []
            self._checkboxes: List[Checkbox] = []

        def compose(self) -> ComposeResult:
            yield Header()
            yield Static("Select repositories to watch:")
            self.repos = discover_git_repos()
            config = read_config()
            watched = set(config.get("watched_repos", []))

            scroll = VerticalScroll()
            yield scroll
            yield Button("Save", id="save")
            yield Footer()

            # Populate checkboxes after compose via on_mount hook.
            self._watched_preset = watched
            self._scroll = scroll

        def on_mount(self) -> None:
            self._checkboxes = []
            for repo in self.repos:
                cb = Checkbox(str(repo), value=str(repo) in self._watched_preset)
                self._checkboxes.append(cb)
                self._scroll.mount(cb)

        def on_button_pressed(self, event: "Button.Pressed") -> None:
            if event.button.id != "save":
                return
            selected = [
                str(self.repos[i])
                for i, cb in enumerate(self._checkboxes)
                if cb.value
            ]
            config = read_config()
            config["watched_repos"] = selected
            write_config(config)
            self.exit()
