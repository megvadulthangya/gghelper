"""Thin, typed wrappers around common git plumbing commands."""

from __future__ import annotations

import subprocess
from typing import List, Optional, Tuple


def run_git(cmd: List[str], capture: bool = False) -> Optional[str] | bool:
    """Run ``git`` with ``cmd``.

    When ``capture`` is False, runs interactively (stdout/stderr passthrough)
    and returns True on success or raises ``subprocess.CalledProcessError``.
    When ``capture`` is True, returns the stripped stdout or None on failure.
    """
    try:
        if capture:
            result = subprocess.run(
                ["git"] + cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        subprocess.run(["git"] + cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        if capture:
            return None
        raise


def check_remote_correctly() -> str:
    """Compare local/remote/base hashes.

    Returns one of: ``up-to-date``, ``local-ahead``, ``remote-ahead``,
    ``diverged``, ``error``.
    """
    try:
        run_git(["fetch", "origin"])
        local = run_git(["rev-parse", "HEAD"], capture=True)
        remote = run_git(["rev-parse", "origin/HEAD"], capture=True)
        base = run_git(["merge-base", "HEAD", "origin/HEAD"], capture=True)

        if not local or not remote or not base:
            return "error"

        if local == remote:
            return "up-to-date"
        if local == base:
            return "remote-ahead"
        if remote == base:
            return "local-ahead"
        return "diverged"
    except subprocess.CalledProcessError:
        return "error"
    except Exception:
        return "error"


def is_git_repo() -> bool:
    try:
        run_git(["rev-parse", "--is-inside-work-tree"], capture=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False


def get_current_branch() -> Optional[str]:
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"], capture=True)  # type: ignore[return-value]


def get_git_status_short() -> List[Tuple[str, str]]:
    """Return a list of ``(status, filepath)`` from ``git status --short``.

    We go around ``run_git`` here because its ``capture=True`` path strips
    leading whitespace, which destroys the first column for statuses like
    ``" M path"``.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, OSError):
        return []
    out = result.stdout
    if not out:
        return []
    entries: List[Tuple[str, str]] = []
    for line in out.splitlines():
        # Porcelain-v1 short format: XY<space>path (or "XY path -> new")
        if len(line) < 3:
            continue
        status = line[:2]
        rest = line[3:]
        # Handle renames: "oldname -> newname" — take the new path.
        if " -> " in rest:
            rest = rest.split(" -> ", 1)[1]
        entries.append((status.strip() or status, rest))
    return entries


def get_recent_log(n: int = 5) -> List[str]:
    out = run_git(["log", "--oneline", f"-{n}"], capture=True)
    if not out:
        return []
    return out.splitlines()


def get_remote_url() -> Optional[str]:
    return run_git(["remote", "get-url", "origin"], capture=True)  # type: ignore[return-value]
