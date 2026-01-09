#!/usr/bin/env python3
"""
gghelper - Git Workflow Mentor & Assistant
Version: 2.1.3 (fixed remote detection)
"""

import os
import sys
import subprocess
import tempfile
import argparse
import json
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def get_config_path():
    config_dir = Path.home() / ".config" / "gghelper"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

def read_config():
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def write_config(config):
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def detect_language(args):
    if args.lang:
        return args.lang
    
    config = read_config()
    if config and 'language' in config:
        return config['language']
    
    lang_env = os.getenv("LANG", "en_US.UTF-8").split('_')[0].lower()
    return "hu" if lang_env == "hu" else "en"

# ============================================================================
# CORRECTED GIT OPERATIONS
# ============================================================================

def run_git(cmd, capture=False):
    try:
        if capture:
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
    except subprocess.CalledProcessError:
        if capture:
            return None
        raise

def check_remote_correctly():
    """
    Correctly check if REMOTE has new commits we don't have.
    
    Returns:
        - "up-to-date": local and remote are the same
        - "local-ahead": we have commits to push
        - "remote-ahead": remote has commits we need to pull
        - "diverged": both have new commits
        - "error": couldn't check
    """
    try:
        # Fetch remote changes without modifying anything
        run_git(["fetch", "origin"])
        
        # Get commit hashes
        local = run_git(["rev-parse", "HEAD"], capture=True)
        remote = run_git(["rev-parse", "origin/HEAD"], capture=True)
        base = run_git(["merge-base", "HEAD", "origin/HEAD"], capture=True)
        
        if local == remote:
            return "up-to-date"
        elif local == base:
            # Remote is ahead of us
            return "remote-ahead"
        elif remote == base:
            # We are ahead of remote
            return "local-ahead"
        else:
            # Diverged
            return "diverged"
    except:
        return "error"

def get_commit_message():
    """Get commit message from user (original style)."""
    print("\n✍️  ENTER COMMIT MESSAGE")
    print("• Type or paste your message")
    print("• Empty line + Ctrl+D to finish")
    print("• Ctrl+C to cancel")
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
        print("\n❌ Cancelled.")
        return None
    
    commit_message = "\n".join(lines).strip()
    
    if not commit_message:
        print("❌ Error: Empty message!")
        return None
    
    # Preview and confirm
    while True:
        print("\n🔍 PREVIEW (this will be committed):")
        print("-" * 50)
        print(commit_message)
        print("-" * 50)
        
        choice = input("Options: [y]es (Commit) / [e]dit (Open editor) / [n]o (Cancel): ").lower()
        
        if choice in ['y', 'i', 'yes', 'igen']:
            return commit_message
        elif choice in ['e', 'edit']:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(commit_message)
                temp_path = f.name
            
            try:
                editor = os.getenv('EDITOR', 'nano')
                subprocess.run([editor, temp_path])
                
                with open(temp_path, 'r') as f:
                    edited_message = f.read().strip()
                
                os.unlink(temp_path)
                
                if not edited_message:
                    print("❌ Error: Empty message after edit!")
                    return None
                
                commit_message = edited_message
            except Exception as e:
                print(f"Error editing message: {e}")
                return commit_message
        elif choice in ['n', 'no', 'nem']:
            print("❌ Cancelled.")
            return None
        else:
            continue

# ============================================================================
# CORRECTED MAIN WORKFLOW
# ============================================================================

def main_workflow(args, lang):
    """Corrected workflow with proper remote detection."""
    
    print(f"\n=== gghelper ===")
    
    # Step 1: Check if git repo
    try:
        run_git(["status"])
    except:
        print("❌ ERROR: Not a Git repository!")
        return 1
    
    # Step 2: Add changes
    print("1. 📦 Adding changes...")
    run_git(["add", "."])
    
    # Step 3: Create commit (unless resolve-only)
    if not args.resolve_only:
        print("2. 💾 Creating commit...")
        message = get_commit_message()
        if message:
            run_git(["commit", "-m", message])
            print("   ✅ Commit created")
        else:
            return 0
    else:
        print("ℹ️  Resolve-only mode: skipping commit creation")
    
    # Step 4: Check remote CORRECTLY
    print("3. 🌐 Checking remote repository...")
    remote_status = check_remote_correctly()
    
    # Step 5: Handle ONLY if remote is ahead or diverged
    if remote_status == "remote-ahead":
        # Remote has new commits (e.g., GitHub Action ran)
        if lang == "hu":
            print("⚠️  A távoli repóban új változtatások vannak (GitHub Action?)")
            response = input("   Automatikusan szinkronizáljam? [i/n]: ").lower()
        else:
            print("⚠️  Remote repository has new changes (GitHub Action?)")
            response = input("   Auto-sync? [y/n]: ").lower()
        
        if response in ['y', 'i', 'yes', 'igen']:
            try:
                if args.safe:
                    run_git(["pull", "--no-rebase"])
                    print("   ✅ Merge successful")
                else:
                    run_git(["pull", "--rebase"])
                    print("   ✅ Rebase successful")
            except:
                print("   ❌ Conflict detected!")
                if lang == "hu":
                    print("   🔧 Kézi megoldás:")
                    print("      1. git status")
                    print("      2. Javítsd a konfliktusokat")
                    print("      3. git add .")
                    print("      4. git rebase --continue")
                else:
                    print("   🔧 Manual steps:")
                    print("      1. git status")
                    print("      2. Fix conflicts")
                    print("      3. git add .")
                    print("      4. git rebase --continue")
                return 1
        else:
            if lang == "hu":
                print("   ℹ️  Kihagyva. Majd manuálisan: git pull --rebase")
            else:
                print("   ℹ️  Skipped. Manual: git pull --rebase")
    
    elif remote_status == "diverged":
        # Both have new commits (rare, needs manual merge)
        if lang == "hu":
            print("⚡ Mindkét oldalon vannak új változtatások!")
            print("   Kézi beavatkozás szükséges:")
            print("   1. git status")
            print("   2. git pull --rebase")
            print("   3. Konfliktusok javítása")
        else:
            print("⚡ Both sides have new commits!")
            print("   Manual intervention required:")
            print("   1. git status")
            print("   2. git pull --rebase")
            print("   3. Fix conflicts")
        return 1
    
    elif remote_status == "local-ahead":
        # Normal case: we have commits to push, remote is clean
        if lang == "hu":
            print("   ✅ A távoli repo friss, pusholhatunk")
        else:
            print("   ✅ Remote is up-to-date, ready to push")
    
    elif remote_status == "up-to-date":
        # Shouldn't happen after commit, but handle it
        if lang == "hu":
            print("   ℹ️  Minden szinkronban van")
        else:
            print("   ℹ️  Everything is synchronized")
    
    # Step 6: Push
    print("4. 🚀 Pushing to GitHub...")
    try:
        run_git(["push"])
        if lang == "hu":
            print("\n✅ SIKER: Minden kész!")
        else:
            print("\n✅ SUCCESS: All done!")
        return 0
    except:
        if lang == "hu":
            print("❌ Push sikertelen. Próbáld: git pull --rebase")
        else:
            print("❌ Push failed. Try: git pull --rebase")
        return 1

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="gghelper - Git Workflow Mentor",
        add_help=False,
        usage="gghelper [--dry-run] [--resolve-only] [--safe] [--lang {en,hu}] [--level {novice,intermediate,expert,auto}] [--set-lang {en,hu}] [--set-level {novice,intermediate,expert,auto}] [--help] [--smart-help] [--stats] [--version]"
    )
    
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--resolve-only", action="store_true", help="Only resolve conflicts")
    parser.add_argument("--safe", action="store_true", help="Use merge instead of rebase")
    parser.add_argument("--lang", choices=["en", "hu"], help="Force language")
    parser.add_argument("--level", choices=["novice", "intermediate", "expert", "auto"], help="Learning level")
    parser.add_argument("--set-lang", choices=["en", "hu"], help="Set default language permanently")
    parser.add_argument("--set-level", choices=["novice", "intermediate", "expert", "auto"], help="Set default learning level permanently")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--smart-help", action="store_true", help="Show smart help")
    parser.add_argument("--stats", action="store_true", help="Show usage statistics")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    
    return parser.parse_args()

def show_help():
    print("""
gghelper v2.1.3 - Git Workflow Mentor

USAGE:
  gghelper                    # Interactive commit and push
  gghelper --resolve-only     # Only resolve conflicts
  gghelper --safe            # Use merge instead of rebase
  gghelper --lang hu         # Hungarian for this run
  gghelper --lang en         # English for this run

CONFIGURATION:
  gghelper --set-lang hu     # Set Hungarian permanently
  gghelper --set-lang en     # Set English permanently
  gghelper --set-level novice      # Detailed explanations
  gghelper --set-level intermediate # Moderate explanations
  gghelper --set-level expert      # Minimal explanations
  gghelper --set-level auto        # Auto-detect (default)

INFORMATION:
  gghelper --help           # Show this help
  gghelper --smart-help     # Contextual help
  gghelper --stats          # Usage statistics
  gghelper --version        # Version info

EXAMPLES:
  gghelper --set-lang hu    # Set Hungarian forever
  gghelper                  # Normal workflow in Hungarian
  gghelper --resolve-only   # Sync with remote only
""")

def main():
    args = parse_arguments()
    
    # Handle config commands
    if args.set_lang or args.set_level:
        config = read_config()
        
        if args.set_lang:
            config['language'] = args.set_lang
            print(f"✅ Language set to: {args.set_lang}")
        
        if args.set_level:
            config['level'] = args.set_level
            print(f"✅ Learning level set to: {args.set_level}")
        
        write_config(config)
        
        print("\n📋 Current configuration:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        print(f"\n💡 Config saved to: {get_config_path()}")
        return 0
    
    if args.help:
        show_help()
        return 0
    
    if args.smart_help:
        print("\n🤔 SMART HELP: Use 'gghelper' for normal workflow, 'gghelper --resolve-only' if GitHub Action modified repo")
        return 0
    
    if args.stats:
        config = read_config()
        print("\n📊 GGHELPER STATISTICS")
        print(f"Language: {config.get('language', 'auto')}")
        print(f"Learning level: {config.get('level', 'auto')}")
        return 0
    
    if args.version:
        print("gghelper v2.1.3 - Fixed remote detection")
        return 0
    
    if args.dry_run:
        print("[DRY-RUN] gghelper would execute workflow")
        return 0
    
    # Detect language
    lang = detect_language(args)
    
    # Run workflow
    try:
        return main_workflow(args, lang)
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
