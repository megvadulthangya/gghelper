#!/usr/bin/env python3
"""
gghelper - Git workflow assistant with GitHub Actions conflict resolution
Version: 1.0.1
Author: Gyöngyösi Gábor
License: MIT
"""

import os
import sys
import subprocess
import tempfile
import argparse

# ============================================================================
# LANGUAGE DETECTION & TEXTS
# ============================================================================

def detect_language():
    """Detect system language from LANG environment variable."""
    lang = os.getenv("LANG", "en_US.UTF-8").split('_')[0].lower()
    return "hu" if lang == "hu" else "en"

def load_texts(lang):
    """Load all text strings for the selected language."""
    if lang == "hu":
        return {
            # UI Elements
            "title": "=== gghelper v1.0.1 ===",
            "not_git_repo": "❌ HIBA: Ez nem Git mappa!",
            
            # Workflow Steps
            "step_scan": "1. 🔍 Mappa állapot ellenőrzése...",
            "step_add": "2. 📦 Változások hozzáadása...",
            "step_commit": "3. 💾 Commit készítése...",
            "step_check": "4. 🌐 Távoli repo ellenőrzése...",
            "step_resolve": "5. ⚙️  Konfliktusok kezelése...",
            "step_push": "6. 🚀 Push GitHubra...",
            "success": "✅ SIKER: Minden kész!",
            
            # Remote Status
            "remote_ahead": "⚠️  A távoli repo változott (GitHub Action)!",
            "auto_resolve_ask": "   Automatikusan megpróbáljam megoldani? [i/n]: ",
            "conflict_detected": "❌ Konfliktus észlelve!",
            "manual_help": """🔧 KÉZI MEGOLDÁS:
  1. git status  (helyzet ellenőrzése)
  2. git pull --rebase  (újrapróbálkozás)
  3. Ha konfliktus van:
     • Javítsd a fájlokat
     • git add .  (javítások hozzáadása)
     • git rebase --continue
  4. git push""",
            
            # Commit Interface
            "commit_header": "✍️  COMMIT ÜZENET MEGADÁSA",
            "commit_instructions": """• Írd vagy másold be az üzenetet
• Üres sor + Ctrl+D a befejezéshez
• Ctrl+C a megszakításhoz""",
            "commit_empty": "❌ Hiba: Üres üzenet!",
            "commit_preview": "🔍 ELLENŐRZÉS (ezt fogom beküldeni):",
            "commit_confirm": "Opciók: [i]gen (Commit) / [e]dit (Szerkesztés) / [n]em (Mégse): ",
            
            # Error Messages
            "no_changes": "ℹ️  Nincsenek változtatások.",
            "push_failed": "❌ Push sikertelen. Próbáld: git pull --rebase",
            "cancelled": "❌ Megszakítva. Semmi nem történt.",
            
            # Help Text
            "help_text": """gghelper v1.0.1 - Git workflow assistant

HASZNÁLAT:
  gghelper                    # Interaktív commit és push
  gghelper --resolve-only     # Csak konfliktusok feloldása
  gghelper --safe            # Használj merge-t rebase helyett
  gghelper --lang hu         # Magyar nyelv kényszerítése
  gghelper --help            # Segítség megjelenítése

GYAKORI PROBLÉMÁK:

1. "Updates were rejected" hiba
   → A GitHub Action módosította a repót.
   → Használd: gghelper --resolve-only
   → Vagy manuálisan: git pull --rebase && git push

2. Konfliktusok a rebase közben
   → Nézd meg: git status
   → Javítsd a konfliktusokat a fájlokban
   → git add .  (javítások hozzáadása)
   → git rebase --continue
   → Futtasd újra: gghelper

3. Commit üzenet szerkesztése
   → Az 'e' opcióval nyílik a szövegszerkesztő.
   → Alapértelmezett: nano, de a $EDITOR változóval módosítható."""
        }
    else:
        return {
            # UI Elements
            "title": "=== gghelper v1.0.1 ===",
            "not_git_repo": "❌ ERROR: Not a Git repository!",
            
            # Workflow Steps
            "step_scan": "1. 🔍 Checking repository status...",
            "step_add": "2. 📦 Adding changes...",
            "step_commit": "3. 💾 Creating commit...",
            "step_check": "4. 🌐 Checking remote repository...",
            "step_resolve": "5. ⚙️  Handling conflicts...",
            "step_push": "6. 🚀 Pushing to GitHub...",
            "success": "✅ SUCCESS: All done!",
            
            # Remote Status
            "remote_ahead": "⚠️  Remote repository has changed (GitHub Action)!",
            "auto_resolve_ask": "   Try to resolve automatically? [y/n]: ",
            "conflict_detected": "❌ Conflict detected!",
            "manual_help": """🔧 MANUAL SOLUTION:
  1. git status  (check situation)
  2. git pull --rebase  (try again)
  3. If conflict occurs:
     • Fix the files
     • git add .  (add fixes)
     • git rebase --continue
  4. git push""",
            
            # Commit Interface
            "commit_header": "✍️  ENTER COMMIT MESSAGE",
            "commit_instructions": """• Type or paste your message
• Empty line + Ctrl+D to finish
• Ctrl+C to cancel""",
            "commit_empty": "❌ Error: Empty message!",
            "commit_preview": "🔍 VERIFY (I will commit this):",
            "commit_confirm": "Options: [y]es (Commit) / [e]dit (Edit) / [n]o (Cancel): ",
            
            # Error Messages
            "no_changes": "ℹ️  No changes to commit.",
            "push_failed": "❌ Push failed. Try: git pull --rebase",
            "cancelled": "❌ Cancelled. No changes made.",
            
            # Help Text
            "help_text": """gghelper v1.0.1 - Git workflow assistant

USAGE:
  gghelper                    # Interactive commit and push
  gghelper --resolve-only     # Only resolve conflicts
  gghelper --safe            # Use merge instead of rebase
  gghelper --lang hu         # Force Hungarian language
  gghelper --help            # Show this help

COMMON ISSUES:

1. "Updates were rejected" error
   → GitHub Action modified the repository.
   → Use: gghelper --resolve-only
   → Or manually: git pull --rebase && git push

2. Merge conflicts during rebase
   → Check: git status
   → Fix conflicts in files
   → git add .  (add fixes)
   → git rebase --continue
   → Run again: gghelper

3. Editing commit message
   → Press 'e' to open text editor.
   → Default: nano, change with $EDITOR variable."""
        }

# ============================================================================
# GIT OPERATIONS
# ============================================================================

def run_git_command(cmd, capture_output=False):
    """Execute a Git command safely."""
    try:
        if capture_output:
            result = subprocess.run(
                ["git"] + cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(["git"] + cmd, check=True)
            return True
    except subprocess.CalledProcessError as e:
        if capture_output:
            return None
        raise

def check_remote_status():
    """Check if remote repository has changes."""
    try:
        # Fetch remote changes
        run_git_command(["fetch", "origin"])
        
        # Compare local and remote
        local = run_git_command(["rev-parse", "@"], capture_output=True)
        remote = run_git_command(["rev-parse", "@{u}"], capture_output=True)
        base = run_git_command(["merge-base", "@", "@{u}"], capture_output=True)
        
        if local == remote:
            return "up-to-date"
        elif local == base:
            return "need-to-pull"
        elif remote == base:
            return "need-to-push"
        else:
            return "diverged"
    except:
        return "error"

# ============================================================================
# USER INTERFACE
# ============================================================================

def get_commit_message(texts):
    """Get commit message from user with editing capability."""
    print(f"\n{texts['commit_header']}")
    print(f"{texts['commit_instructions']}")
    print("-" * 50)
    
    # Get multiline input
    lines = []
    try:
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print(f"\n{texts['cancelled']}")
        return None
    
    commit_message = "\n".join(lines).strip()
    
    if not commit_message:
        print(f"\n{texts['commit_empty']}")
        return None
    
    # Preview and confirm/edit loop
    while True:
        print(f"\n{texts['commit_preview']}")
        print("-" * 50)
        print(commit_message)
        print("-" * 50)
        
        choice = input(f"{texts['commit_confirm']}").lower()
        
        if choice in ['y', 'i', 'yes', 'igen']:
            return commit_message
        elif choice in ['e', 'edit', 'szerkesztés', 'módosít']:
            # Edit in text editor
            commit_message = edit_in_editor(commit_message)
            if not commit_message:
                print(f"\n{texts['commit_empty']}")
                return None
        elif choice in ['n', 'no', 'nem']:
            print(f"\n{texts['cancelled']}")
            return None
        else:
            # Invalid input, ask again
            continue

def edit_in_editor(current_message):
    """Edit text in user's preferred editor."""
    # Create temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(current_message)
        temp_path = f.name
    
    try:
        # Get editor from environment or use nano
        editor = os.getenv('EDITOR', 'nano')
        subprocess.run([editor, temp_path])
        
        # Read edited message
        with open(temp_path, 'r') as f:
            edited_message = f.read().strip()
        
        os.unlink(temp_path)
        return edited_message
        
    except Exception as e:
        print(f"Error editing message: {e}")
        return current_message

# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main_workflow(args, texts):
    """Execute the main workflow."""
    print(f"\n{texts['title']}")
    
    # Step 1: Check if we're in a git repo
    print(f"\n{texts['step_scan']}")
    try:
        run_git_command(["status"])
    except:
        print(f"\n{texts['not_git_repo']}")
        return 1
    
    # Step 2: Add changes
    print(f"\n{texts['step_add']}")
    run_git_command(["add", "."])
    
    # Step 3: Create commit (unless resolve-only mode)
    commit_created = False
    if not args.resolve_only:
        print(f"\n{texts['step_commit']}")
        commit_message = get_commit_message(texts)
        if commit_message:
            run_git_command(["commit", "-m", commit_message])
            commit_created = True
        else:
            # User cancelled commit creation
            return 0
    else:
        print(f"\nℹ️  Resolve-only mode: skipping commit creation")
    
    # Step 4: Check remote status
    print(f"\n{texts['step_check']}")
    remote_status = check_remote_status()
    
    # Step 5: Handle conflicts if needed
    if remote_status in ["need-to-pull", "diverged"]:
        print(f"\n{texts['step_resolve']}")
        print(f"{texts['remote_ahead']}")
        
        response = input(f"{texts['auto_resolve_ask']}").lower()
        if response in ['y', 'i', 'yes', 'igen']:
            try:
                current_branch = run_git_command(["branch", "--show-current"], capture_output=True)
                if args.safe:
                    run_git_command(["pull", "--no-rebase", "origin", current_branch])
                else:
                    run_git_command(["pull", "--rebase", "origin", current_branch])
                print("✅ Successfully synced with remote.")
            except:
                print(f"\n{texts['conflict_detected']}")
                print(f"\n{texts['manual_help']}")
                return 1
        else:
            print(f"\n{texts['cancelled']}")
            return 0
    
    # Step 6: Push changes
    print(f"\n{texts['step_push']}")
    try:
        run_git_command(["push"])
        print(f"\n{texts['success']}")
        return 0
    except:
        print(f"\n{texts['push_failed']}")
        return 1

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="gghelper - Git workflow assistant",
        add_help=False
    )
    
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    parser.add_argument("--resolve-only", action="store_true", 
                       help="Only resolve conflicts, don't create commit")
    parser.add_argument("--safe", action="store_true", 
                       help="Use merge instead of rebase for conflict resolution")
    parser.add_argument("--lang", choices=["en", "hu"], 
                       help="Force language (en/hu)")
    parser.add_argument("--help", "-h", action="store_true", 
                       help="Show help message")
    parser.add_argument("--version", "-v", action="store_true", 
                       help="Show version information")
    
    args = parser.parse_args()
    
    # Handle version
    if args.version:
        print("gghelper v1.0.1")
        print("License: MIT")
        print("Author: Gyöngyösi Gábor")
        return 0
    
    # Handle help
    if args.help:
        # Auto-detect language for help
        lang = args.lang or detect_language()
        texts = load_texts(lang)
        print(texts["help_text"])
        return 0
    
    # Handle dry-run
    if args.dry_run:
        print("[DRY-RUN] gghelper would execute the workflow")
        return 0
    
    # Determine language
    lang = args.lang or detect_language()
    texts = load_texts(lang)
    
    # Execute workflow
    try:
        return main_workflow(args, texts)
    except KeyboardInterrupt:
        print(f"\n{texts['cancelled']}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
