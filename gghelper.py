#!/usr/bin/env python3
"""
gghelper - Git workflow assistant with GitHub Actions conflict resolution
Version: 1.0.0
Author: Gyöngyösi Gábor
License: MIT
"""

import os
import sys
import subprocess
import argparse
import textwrap

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_git(cmd, capture=False):
    """Run git command."""
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
    except subprocess.CalledProcessError as e:
        if capture:
            return None
        raise

def show_help():
    """Show help information."""
    help_text = """
gghelper v1.0.0 - Git workflow assistant

USAGE:
  gghelper                    # Interactive commit and push
  gghelper --resolve-only     # Only resolve conflicts, don't create commit
  gghelper --safe            # Use merge instead of rebase
  gghelper --lang hu         # Hungarian interface
  gghelper --help            # Show this help
  gghelper --how-to          # Detailed how-to guide

COMMON SCENARIOS:

1. GitHub Action modified repository:
   When you see "Updates were rejected because the remote contains work":
   → Run: gghelper --resolve-only
   → Or manually: git pull --rebase && git push

2. Merge conflicts during rebase:
   → Check: git status
   → Fix the conflicting files
   → Mark resolved: git add .
   → Continue: git rebase --continue
   → Push: gghelper

3. Editing commit message:
   → When prompted, press 'e' to edit
   → Uses $EDITOR (default: nano)
   → Save and exit to continue

AUTHOR:
  Gyöngyösi Gábor
  GitHub: https://github.com/megvadulthangya
"""
    print(help_text)

def show_how_to():
    """Show detailed how-to guide."""
    how_to = """
DETAILED HOW-TO GUIDE:

PROBLEM 1: "Updates were rejected" error
----------------------------------------
This happens when GitHub Actions modified the repository while you were
working locally.

SOLUTION 1 (Automatic):
  gghelper --resolve-only

SOLUTION 2 (Manual):
  1. git fetch origin
  2. git rebase origin/main
  3. git push

PROBLEM 2: Merge conflicts during rebase
----------------------------------------
When automatic conflict resolution fails.

SOLUTION:
  1. Check status: git status
  2. Open files with conflict markers (<<<<<<<, =======, >>>>>>>)
  3. Choose which changes to keep
  4. Remove conflict markers
  5. Mark as resolved: git add .
  6. Continue rebase: git rebase --continue
  7. Push: git push

PROBLEM 3: I want to use merge instead of rebase
------------------------------------------------
Some prefer merge commits for clarity.

SOLUTION:
  gghelper --safe

INSTALLATION:
  This package is part of the manjaro-awesome repository.
  It's automatically included in the custom Manjaro spin.
"""
    print(how_to)

# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="gghelper - Git workflow assistant",
        add_help=False
    )
    
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--resolve-only", action="store_true", help="Only resolve conflicts")
    parser.add_argument("--safe", action="store_true", help="Use merge instead of rebase")
    parser.add_argument("--lang", choices=["en", "hu"], help="Force language (en/hu)")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--how-to", action="store_true", help="Show detailed how-to guide")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return 0
    
    if args.how_to:
        show_how_to()
        return 0
    
    if args.version:
        print("gghelper v1.0.0")
        print("License: MIT")
        print("Author: Gyöngyösi Gábor")
        return 0
    
    if args.dry_run:
        print("[DRY-RUN] gghelper would execute workflow")
        return 0
    
    # Detect language
    lang = args.lang
    if not lang:
        lang_env = os.getenv("LANG", "").lower()
        lang = "hu" if "hu" in lang_env else "en"
    
    # Simple workflow
    print("\n=== gghelper v1.0.0 ===")
    
    try:
        # Step 1: Add changes
        print("1. Adding changes...")
        run_git(["add", "."])
        
        # Step 2: Commit (unless resolve-only)
        if not args.resolve_only:
            print("2. Creating commit...")
            # Get commit message
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("# Enter commit message above this line\n")
                temp_file = f.name
            
            editor = os.getenv('EDITOR', 'nano')
            subprocess.run([editor, temp_file])
            
            with open(temp_file, 'r') as f:
                lines = [line.strip() for line in f if not line.startswith('#') and line.strip()]
                message = "\n".join(lines)
            
            os.unlink(temp_file)
            
            if message:
                run_git(["commit", "-m", message])
            else:
                print("No commit message provided, skipping commit.")
        
        # Step 3: Check remote
        print("3. Checking remote repository...")
        try:
            run_git(["fetch", "origin"])
            
            # Check if remote has changes
            local = run_git(["rev-parse", "@"], capture=True)
            remote = run_git(["rev-parse", "@{u}"], capture=True)
            
            if local != remote:
                print("   Remote has changes, resolving...")
                
                if args.safe:
                    run_git(["pull", "--no-rebase", "origin", run_git(["branch", "--show-current"], capture=True)])
                else:
                    try:
                        run_git(["pull", "--rebase", "origin", run_git(["branch", "--show-current"], capture=True)])
                    except:
                        print("   Conflict detected! Resolve manually:")
                        print("   git status")
                        print("   git rebase --continue (after fixing conflicts)")
                        return 1
        
        except subprocess.CalledProcessError:
            print("   Warning: Could not check remote status")
        
        # Step 4: Push
        print("4. Pushing to GitHub...")
        run_git(["push"])
        
        print("\n✅ Success!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
