"""User-facing strings for gghelper.

All user-facing text flows through this module so it can be translated and
tuned to the user's experience level.
"""

from __future__ import annotations

from typing import Dict

SUPPORTED_LANGS = ("hu", "en")
LEVELS = ("novice", "intermediate", "expert", "auto")

# ---------------------------------------------------------------------------
# Simple messages: one string per language.
# ---------------------------------------------------------------------------
MESSAGES: Dict[str, Dict[str, str]] = {
    "not_a_repo": {
        "hu": "HIBA: Nem Git repó!",
        "en": "ERROR: Not a Git repository!",
    },
    "header": {
        "hu": "=== gghelper ===",
        "en": "=== gghelper ===",
    },
    "adding_changes": {
        "hu": "1. Változtatások hozzáadása...",
        "en": "1. Adding changes...",
    },
    "no_changes": {
        "hu": "Nincs változás a staginghez.",
        "en": "No changes to stage.",
    },
    "creating_commit": {
        "hu": "2. Commit készítése...",
        "en": "2. Creating commit...",
    },
    "commit_created": {
        "hu": "   Commit elkészült",
        "en": "   Commit created",
    },
    "resolve_only_skip_commit": {
        "hu": "Resolve-only mód: commit kihagyva",
        "en": "Resolve-only mode: skipping commit creation",
    },
    "checking_remote": {
        "hu": "3. Távoli repo ellenőrzése...",
        "en": "3. Checking remote repository...",
    },
    "remote_ahead_hu": {
        "hu": "A távoli repóban új változtatások vannak (GitHub Action?)",
        "en": "Remote repository has new changes (GitHub Action?)",
    },
    "ask_auto_sync": {
        "hu": "   Automatikusan szinkronizáljam? [i/n]: ",
        "en": "   Auto-sync? [y/n]: ",
    },
    "merge_success": {
        "hu": "   Merge sikeres",
        "en": "   Merge successful",
    },
    "rebase_success": {
        "hu": "   Rebase sikeres",
        "en": "   Rebase successful",
    },
    "conflict_detected": {
        "hu": "   Konfliktus!",
        "en": "   Conflict detected!",
    },
    "manual_steps_header": {
        "hu": "   Kézi megoldás:",
        "en": "   Manual steps:",
    },
    "manual_step_1": {
        "hu": "      1. git status",
        "en": "      1. git status",
    },
    "manual_step_2_hu": {
        "hu": "      2. Javítsd a konfliktusokat",
        "en": "      2. Fix conflicts",
    },
    "manual_step_3": {
        "hu": "      3. git add .",
        "en": "      3. git add .",
    },
    "manual_step_4": {
        "hu": "      4. git rebase --continue",
        "en": "      4. git rebase --continue",
    },
    "skipped_manual_pull": {
        "hu": "   Kihagyva. Majd manuálisan: git pull --rebase",
        "en": "   Skipped. Manual: git pull --rebase",
    },
    "diverged_header": {
        "hu": "Mindkét oldalon vannak új változtatások!",
        "en": "Both sides have new commits!",
    },
    "diverged_manual_required": {
        "hu": "   Kézi beavatkozás szükséges:",
        "en": "   Manual intervention required:",
    },
    "diverged_step_2": {
        "hu": "   2. git pull --rebase",
        "en": "   2. git pull --rebase",
    },
    "diverged_step_3": {
        "hu": "   3. Konfliktusok javítása",
        "en": "   3. Fix conflicts",
    },
    "remote_clean_ready": {
        "hu": "   A távoli repo friss, pusholhatunk",
        "en": "   Remote is up-to-date, ready to push",
    },
    "all_synced": {
        "hu": "   Minden szinkronban van",
        "en": "   Everything is synchronized",
    },
    "pushing": {
        "hu": "4. Pushing to GitHub...",
        "en": "4. Pushing to GitHub...",
    },
    "success_done": {
        "hu": "SIKER: Minden kész!",
        "en": "SUCCESS: All done!",
    },
    "push_failed": {
        "hu": "Push sikertelen. Próbáld: git pull --rebase",
        "en": "Push failed. Try: git pull --rebase",
    },
    "cancelled_by_user": {
        "hu": "Felhasználó megszakította",
        "en": "Cancelled by user",
    },
    "cancelled": {
        "hu": "Megszakítva.",
        "en": "Cancelled.",
    },
    # Commit prompt strings ------------------------------------------------
    "commit_prompt_header": {
        "hu": "IRJ COMMIT ÜZENETET",
        "en": "ENTER COMMIT MESSAGE",
    },
    "commit_prompt_hint_type": {
        "hu": "- Írd vagy illeszd be az üzenetet",
        "en": "- Type or paste your message",
    },
    "commit_prompt_hint_finish": {
        "hu": "- Üres sor + Ctrl+D = kész",
        "en": "- Empty line + Ctrl+D to finish",
    },
    "commit_prompt_hint_cancel": {
        "hu": "- Ctrl+C = mégse",
        "en": "- Ctrl+C to cancel",
    },
    "commit_empty_error": {
        "hu": "Hiba: üres commit üzenet!",
        "en": "Error: Empty message!",
    },
    "commit_preview_header": {
        "hu": "ELŐNÉZET (ez kerül commitba):",
        "en": "PREVIEW (this will be committed):",
    },
    "commit_confirm_prompt": {
        "hu": "Opciók: [i]gen / [e]szerkeszt / [n]em: ",
        "en": "Options: [y]es (Commit) / [e]dit (Open editor) / [n]o (Cancel): ",
    },
    "commit_edit_empty": {
        "hu": "Hiba: üres üzenet szerkesztés után!",
        "en": "Error: Empty message after edit!",
    },
    "commit_edit_error": {
        "hu": "Hiba az üzenet szerkesztésekor: ",
        "en": "Error editing message: ",
    },
    "commit_too_short": {
        "hu": "Figyelem: a commit üzenet rövid (<10 karakter). Próbálj leíróbb üzenetet írni.",
        "en": "Warning: commit message is short (<10 chars). Try a more descriptive message.",
    },
    "commit_generic": {
        "hu": "Figyelem: általános commit üzenet. Javasolt formátum: 'feat: leírás', 'fix: leírás'.",
        "en": "Warning: generic commit message. Suggested format: 'feat: description', 'fix: description'.",
    },
    "commit_retry_prompt": {
        "hu": "Új üzenet [i], vagy megtartás [n]? ",
        "en": "Re-enter message [y], or keep it [n]? ",
    },
    "commit_conventional_header": {
        "hu": "Conventional Commits példák:",
        "en": "Conventional Commits examples:",
    },
    # Branch awareness -----------------------------------------------------
    "current_branch": {
        "hu": "Aktuális branch: ",
        "en": "Current branch: ",
    },
    "main_branch_warning": {
        "hu": "Figyelem: közvetlenül a {branch} branch-re pusholsz. Biztos vagy benne? [i/n]: ",
        "en": "Warning: you are pushing directly to {branch}. Are you sure? [y/n]: ",
    },
    "main_branch_aborted": {
        "hu": "Megszakítva a main/master védelem miatt.",
        "en": "Aborted due to main/master protection.",
    },
    # Interactive staging --------------------------------------------------
    "staging_header": {
        "hu": "Módosított fájlok:",
        "en": "Changed files:",
    },
    "staging_prompt": {
        "hu": "Válaszd ki a fájlokat (pl. 1,3,5 vagy 'all', Enter = mind): ",
        "en": "Select files (e.g. 1,3,5 or 'all', Enter = all): ",
    },
    "staging_nothing_selected": {
        "hu": "Nincs kiválasztva fájl.",
        "en": "No files selected.",
    },
    # Stats ----------------------------------------------------------------
    "stats_header": {
        "hu": "GGHELPER STATISZTIKA",
        "en": "GGHELPER STATISTICS",
    },
    "stats_total_runs": {
        "hu": "Futtatások száma: ",
        "en": "Total runs: ",
    },
    "stats_successful_runs": {
        "hu": "Sikeres futtatások: ",
        "en": "Successful runs: ",
    },
    "stats_conflicts": {
        "hu": "Konfliktusos futtatások: ",
        "en": "Runs with conflicts: ",
    },
    "stats_last_run": {
        "hu": "Utolsó futtatás: ",
        "en": "Last run: ",
    },
    "stats_language": {
        "hu": "Nyelv: ",
        "en": "Language: ",
    },
    "stats_level": {
        "hu": "Szint: ",
        "en": "Learning level: ",
    },
    "stats_none_yet": {
        "hu": "Még nem futott gghelper.",
        "en": "gghelper has not run yet.",
    },
    # Smart help -----------------------------------------------------------
    "smart_help_header": {
        "hu": "SMART HELP",
        "en": "SMART HELP",
    },
    "smart_help_not_repo": {
        "hu": "Ez nem git repó. Lépj be egy repóba, vagy futtasd: git init",
        "en": "This is not a git repository. Enter a repo or run: git init",
    },
    "smart_help_remote_ahead": {
        "hu": "A remote-on új változás van. Futtasd: gghelper --resolve-only",
        "en": "Remote has new changes. Run: gghelper --resolve-only",
    },
    "smart_help_local_ahead": {
        "hu": "Van lokális commit, amit még nem pusholtál. Futtasd: git push",
        "en": "You have local commits to push. Run: git push",
    },
    "smart_help_uncommitted": {
        "hu": "Van módosított fájlod. Futtasd: gghelper",
        "en": "You have modified files. Run: gghelper",
    },
    "smart_help_diverged": {
        "hu": "Mindkét oldalon van változás, kézi beavatkozás kell (git pull --rebase).",
        "en": "Both sides have changes, manual intervention needed (git pull --rebase).",
    },
    "smart_help_up_to_date": {
        "hu": "Minden rendben, nincs teendő.",
        "en": "Everything is in order, nothing to do.",
    },
    "smart_help_recent_log": {
        "hu": "Legutóbbi commitok:",
        "en": "Recent commits:",
    },
    # Watch ----------------------------------------------------------------
    "watch_no_repos": {
        "hu": "Nincs figyelt repó. Indítom a konfigurátort...",
        "en": "No watched repos configured. Launching the configurator...",
    },
    "watch_running": {
        "hu": "Figyelem {count} repót ({interval}s). Ctrl+C = kilépés.",
        "en": "Watching {count} repos (interval: {interval}s). Ctrl+C to stop.",
    },
    "watch_stopped": {
        "hu": "Watch leállítva.",
        "en": "Watch stopped.",
    },
    "watch_status_line": {
        "hu": "[{name}] {status}",
        "en": "[{name}] {status}",
    },
    "watch_notification_title": {
        "hu": "gghelper: {name}",
        "en": "gghelper: {name}",
    },
    "watch_notification_body": {
        "hu": "Remote változás: {status}",
        "en": "Remote changes detected ({status})",
    },
    "watch_textual_missing": {
        "hu": "A 'textual' csomag szükséges: pip install textual",
        "en": "The 'textual' package is required: pip install textual",
    },
    "watch_textual_fallback": {
        "hu": "Alternatíva: szerkeszd kézzel a ~/.config/gghelper/config.json fájlt.",
        "en": "Alternative: manually edit ~/.config/gghelper/config.json.",
    },
    # PR link --------------------------------------------------------------
    "pr_link_prefix": {
        "hu": "PR: ",
        "en": "PR: ",
    },
    "compare_link_prefix": {
        "hu": "Compare URL: ",
        "en": "Compare URL: ",
    },
    # Dry-run --------------------------------------------------------------
    "dry_run_header": {
        "hu": "[DRY-RUN] Nincs tényleges művelet.",
        "en": "[DRY-RUN] No real actions performed.",
    },
    "dry_run_would_stage": {
        "hu": "[DRY-RUN] Stagingre kerülne:",
        "en": "[DRY-RUN] Would stage:",
    },
    "dry_run_would_ask_commit": {
        "hu": "[DRY-RUN] Bekérné a commit üzenetet",
        "en": "[DRY-RUN] Would ask for commit message",
    },
    "dry_run_would_run": {
        "hu": "[DRY-RUN] Futtatná: ",
        "en": "[DRY-RUN] Would run: ",
    },
    # Config set messages --------------------------------------------------
    "cfg_language_set": {
        "hu": "Nyelv beállítva: ",
        "en": "Language set to: ",
    },
    "cfg_level_set": {
        "hu": "Szint beállítva: ",
        "en": "Learning level set to: ",
    },
    "cfg_current_header": {
        "hu": "Jelenlegi konfiguráció:",
        "en": "Current configuration:",
    },
    "cfg_saved_to": {
        "hu": "Konfig elmentve ide: ",
        "en": "Config saved to: ",
    },
}


# ---------------------------------------------------------------------------
# Level-aware messages. Each entry: key -> lang -> level -> str.
# Expert level is empty by design: experts don't want explanations.
# ---------------------------------------------------------------------------
LEVEL_MESSAGES: Dict[str, Dict[str, Dict[str, str]]] = {
    "git_add_explain": {
        "hu": {
            "novice": (
                "A `git add .` azt jelenti, hogy minden módosított fájlt "
                "előkészítünk a commithoz. A staging area egy köztes terület "
                "a working directory és a repository között."
            ),
            "intermediate": "Staging: fájlok előkészítése commithoz",
            "expert": "",
        },
        "en": {
            "novice": (
                "`git add .` means we prepare all modified files for the "
                "commit. The staging area is an intermediate zone between "
                "your working directory and the repository."
            ),
            "intermediate": "Staging: preparing files for commit",
            "expert": "",
        },
    },
    "git_commit_explain": {
        "hu": {
            "novice": (
                "A commit egy pillanatkép a staginghez adott változtatásokról. "
                "Írd le röviden, mit módosítottál — jól használható commit "
                "üzenetekkel később könnyen visszafejthető a történet."
            ),
            "intermediate": "Commit készítése a staging tartalmával",
            "expert": "",
        },
        "en": {
            "novice": (
                "A commit is a snapshot of the staged changes. Describe "
                "briefly what you changed — clear commit messages make the "
                "project history easy to follow later."
            ),
            "intermediate": "Creating a commit from staged changes",
            "expert": "",
        },
    },
    "remote_check_explain": {
        "hu": {
            "novice": (
                "Megnézzük a távoli repót (origin). Ha új commitok vannak ott, "
                "amiket nem látunk, előbb szinkronizálnunk kell, különben a "
                "push sikertelen lesz."
            ),
            "intermediate": "Távoli repo ellenőrzése (git fetch + hash összehasonlítás)",
            "expert": "",
        },
        "en": {
            "novice": (
                "We check the remote (origin). If there are new commits we "
                "don't yet have, we must sync before pushing, otherwise the "
                "push will be rejected."
            ),
            "intermediate": "Checking remote (git fetch + hash compare)",
            "expert": "",
        },
    },
    "branch_explain": {
        "hu": {
            "novice": (
                "A branch egy független fejlesztési vonal. A `main` / `master` "
                "branch általában a stabil, kiadható kódot tartalmazza. Új "
                "funkciókhoz külön branch-et érdemes nyitni."
            ),
            "intermediate": "",
            "expert": "",
        },
        "en": {
            "novice": (
                "A branch is an independent line of development. The `main` / "
                "`master` branch usually holds stable, release-ready code. "
                "For new features, prefer a dedicated branch."
            ),
            "intermediate": "",
            "expert": "",
        },
    },
    "staging_explain": {
        "hu": {
            "novice": (
                "Staging: csak a kiválasztott fájlok kerülnek a commitba. "
                "Az unstaged fájlok modified állapotban maradnak."
            ),
            "intermediate": "",
            "expert": "",
        },
        "en": {
            "novice": (
                "Staging: only selected files will be included in the commit. "
                "Unstaged files remain in modified state."
            ),
            "intermediate": "",
            "expert": "",
        },
    },
    "conventional_commit_examples": {
        "hu": {
            "novice": (
                "  feat: új funkció hozzáadása\n"
                "  fix: hiba javítása\n"
                "  docs: dokumentáció frissítése\n"
                "  refactor: kód átszervezése"
            ),
            "intermediate": "",
            "expert": "",
        },
        "en": {
            "novice": (
                "  feat: add a new feature\n"
                "  fix: fix a bug\n"
                "  docs: update documentation\n"
                "  refactor: restructure code without behavior change"
            ),
            "intermediate": "",
            "expert": "",
        },
    },
    "gh_cli_suggestion": {
        "hu": {
            "novice": (
                "Tipp: telepítsd a GitHub CLI-t (gh), hogy a PR linket automatikusan kapd."
            ),
            "intermediate": "",
            "expert": "",
        },
        "en": {
            "novice": (
                "Tip: install the GitHub CLI (gh) to get PR links automatically."
            ),
            "intermediate": "",
            "expert": "",
        },
    },
}


def _lang(lang: str) -> str:
    return lang if lang in SUPPORTED_LANGS else "en"


def _level(level: str) -> str:
    if level == "auto" or level not in LEVELS:
        return "intermediate"
    return level


def msg(key: str, lang: str = "en") -> str:
    """Return a simple message for ``key`` in ``lang``.

    Falls back to English, then to the key itself when not found.
    """
    lang = _lang(lang)
    entry = MESSAGES.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("en") or key


def level_msg(key: str, lang: str = "en", level: str = "intermediate") -> str:
    """Return a level-aware message. May be empty (intentionally)."""
    lang = _lang(lang)
    level = _level(level)
    entry = LEVEL_MESSAGES.get(key, {})
    per_lang = entry.get(lang) or entry.get("en") or {}
    return per_lang.get(level, "")
