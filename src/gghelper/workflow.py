"""Main gghelper workflow orchestration."""

from __future__ import annotations

import re
import shutil
import subprocess
from typing import List, Optional

from gghelper import i18n
from gghelper.commit import get_commit_message
from gghelper.git_ops import (
    check_remote_correctly,
    get_current_branch,
    get_git_status_short,
    get_remote_url,
    is_git_repo,
    run_git,
)
from gghelper.progress import record_run


def _print_level(key: str, lang: str, level: str) -> None:
    text = i18n.level_msg(key, lang, level)
    if text:
        print(text)


def _confirm(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in {"y", "i", "yes", "igen"}
    except EOFError:
        return False


def _select_files(lang: str, level: str, dry_run: bool) -> Optional[List[str]]:
    """Return the list of file paths to stage, or None if user cancelled.

    Empty list + "all" sentinel is represented by returning ``None`` meaning
    "no changes" and returning ``[]`` meaning "stage everything".
    """
    entries = get_git_status_short()
    if not entries:
        print(i18n.msg("no_changes", lang))
        return None

    _print_level("staging_explain", lang, level)
    print(i18n.msg("staging_header", lang))
    for i, (status, path) in enumerate(entries, 1):
        print(f"  {i}. [{status}] {path}")

    try:
        raw = input(i18n.msg("staging_prompt", lang)).strip()
    except EOFError:
        raw = ""

    if raw == "" or raw.lower() == "all":
        if dry_run:
            print(i18n.msg("dry_run_would_stage", lang))
            for _, path in entries:
                print(f"  {path}")
        return []  # signal "all"

    selected: List[str] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            idx = int(token)
        except ValueError:
            continue
        if 1 <= idx <= len(entries):
            selected.append(entries[idx - 1][1])

    if not selected:
        print(i18n.msg("staging_nothing_selected", lang))
        return None

    if dry_run:
        print(i18n.msg("dry_run_would_stage", lang))
        for path in selected:
            print(f"  {path}")
    return selected


def _run_or_preview(cmd: List[str], dry_run: bool, lang: str) -> bool:
    if dry_run:
        print(i18n.msg("dry_run_would_run", lang) + "git " + " ".join(cmd))
        return True
    try:
        run_git(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def _print_pr_link(branch: str, lang: str, level: str) -> None:
    if not shutil.which("gh"):
        _print_level("gh_cli_suggestion", lang, level)
        _print_compare_url(branch, lang)
        return

    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "list",
                "--head",
                branch,
                "--json",
                "url",
                "--limit",
                "1",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        _print_compare_url(branch, lang)
        return

    out = (result.stdout or "").strip()
    if result.returncode == 0 and out and out != "[]":
        # Minimal JSON parsing: look for "url":"..."
        match = re.search(r'"url"\s*:\s*"([^"]+)"', out)
        if match:
            print(i18n.msg("pr_link_prefix", lang) + match.group(1))
            return
    _print_compare_url(branch, lang)


def _print_compare_url(branch: str, lang: str) -> None:
    url = get_remote_url()
    if not url:
        return
    owner_repo = _parse_github_owner_repo(url)
    if not owner_repo:
        return
    owner, repo = owner_repo
    compare = f"https://github.com/{owner}/{repo}/compare/{branch}"
    print(i18n.msg("compare_link_prefix", lang) + compare)


def _parse_github_owner_repo(url: str):
    # Supports: git@github.com:owner/repo(.git), https://github.com/owner/repo(.git)
    ssh_match = re.match(r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if ssh_match:
        return ssh_match.group(1), ssh_match.group(2)
    https_match = re.match(
        r"https?://[^/]*github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url
    )
    if https_match:
        return https_match.group(1), https_match.group(2)
    return None


def main_workflow(args, lang: str, level: str) -> int:
    dry_run = bool(getattr(args, "dry_run", False))

    print()
    print(i18n.msg("header", lang))

    if not is_git_repo():
        print(i18n.msg("not_a_repo", lang))
        return 1

    # Branch awareness ------------------------------------------------------
    branch = get_current_branch() or "?"
    print(f"{i18n.msg('current_branch', lang)}{branch}")
    _print_level("branch_explain", lang, level)

    if branch in {"main", "master"}:
        prompt = i18n.msg("main_branch_warning", lang).format(branch=branch)
        if not _confirm(prompt):
            print(i18n.msg("main_branch_aborted", lang))
            return 1

    commit_msg_length = 0
    had_conflict = False
    resolve_only = bool(getattr(args, "resolve_only", False))

    # Step 1: add ----------------------------------------------------------
    if not resolve_only:
        print(i18n.msg("adding_changes", lang))
        _print_level("git_add_explain", lang, level)

        selected = _select_files(lang, level, dry_run)
        if selected is None and not dry_run:
            return 0
        if selected is None and dry_run:
            return 0
        if selected == []:
            _run_or_preview(["add", "."], dry_run, lang)
        else:
            _run_or_preview(["add", "--"] + selected, dry_run, lang)

        # Step 2: commit --------------------------------------------------
        print(i18n.msg("creating_commit", lang))
        _print_level("git_commit_explain", lang, level)

        if dry_run:
            print(i18n.msg("dry_run_would_ask_commit", lang))
        else:
            message = get_commit_message(lang=lang, level=level)
            if not message:
                return 0
            commit_msg_length = len(message)
            try:
                run_git(["commit", "-m", message])
                print(i18n.msg("commit_created", lang))
            except subprocess.CalledProcessError:
                return 1
    else:
        print(i18n.msg("resolve_only_skip_commit", lang))

    # Step 3: remote check -------------------------------------------------
    print(i18n.msg("checking_remote", lang))
    _print_level("remote_check_explain", lang, level)

    remote_status = check_remote_correctly()

    if remote_status == "remote-ahead":
        if _confirm(i18n.msg("ask_auto_sync", lang)):
            cmd = ["pull", "--no-rebase"] if getattr(args, "safe", False) else ["pull", "--rebase"]
            if _run_or_preview(cmd, dry_run, lang):
                key = "merge_success" if getattr(args, "safe", False) else "rebase_success"
                print(i18n.msg(key, lang))
            else:
                had_conflict = True
                print(i18n.msg("conflict_detected", lang))
                print(i18n.msg("manual_steps_header", lang))
                print(i18n.msg("manual_step_1", lang))
                print(i18n.msg("manual_step_2_hu", lang))
                print(i18n.msg("manual_step_3", lang))
                print(i18n.msg("manual_step_4", lang))
                record_run(branch, commit_msg_length, had_conflict, success=False)
                return 1
        else:
            print(i18n.msg("skipped_manual_pull", lang))

    elif remote_status == "diverged":
        had_conflict = True
        print(i18n.msg("diverged_header", lang))
        print(i18n.msg("diverged_manual_required", lang))
        print(i18n.msg("manual_step_1", lang))
        print(i18n.msg("diverged_step_2", lang))
        print(i18n.msg("diverged_step_3", lang))
        record_run(branch, commit_msg_length, had_conflict, success=False)
        return 1

    elif remote_status == "local-ahead":
        print(i18n.msg("remote_clean_ready", lang))
    elif remote_status == "up-to-date":
        print(i18n.msg("all_synced", lang))

    # Step 4: push ---------------------------------------------------------
    print(i18n.msg("pushing", lang))
    if not _run_or_preview(["push"], dry_run, lang):
        print(i18n.msg("push_failed", lang))
        record_run(branch, commit_msg_length, had_conflict, success=False)
        return 1

    print()
    print(i18n.msg("success_done", lang))

    if not dry_run:
        _print_pr_link(branch, lang, level)
        record_run(branch, commit_msg_length, had_conflict, success=True)
    return 0
