#!/usr/bin/env python3
"""
gghelper - Git Workflow Mentor & Assistant
Version: 2.0.0 - "Learn as you use"
Author: Gyöngyösi Gábor
License: MIT
"""

import os
import sys
import subprocess
import tempfile
import argparse
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION & LEARNING SYSTEM
# ============================================================================

class LearningLevel:
    """Define user learning levels."""
    NOVICE = "novice"      # Detailed explanations, step-by-step
    INTERMEDIATE = "intermediate"  # Some explanations
    EXPERT = "expert"      # Minimal explanations
    
    @staticmethod
    def detect_from_history():
        """Try to detect user's experience level from git history."""
        try:
            # Check how many commits user has
            result = subprocess.run(
                ["git", "log", "--oneline", "--author=$(git config user.email)", "--all"],
                capture_output=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            commit_count = len(result.stdout.strip().split('\n')) if result.stdout else 0
            
            if commit_count > 100:
                return LearningLevel.EXPERT
            elif commit_count > 20:
                return LearningLevel.INTERMEDIATE
            else:
                return LearningLevel.NOVICE
        except:
            return LearningLevel.NOVICE

class TipsDatabase:
    """Database of contextual tips for different scenarios."""
    
    TIPS = {
        "multi_user_conflict": {
            "hu": [
                "💡 TIPP: Ha több ember dolgozik egy repón, gyakrabban pull-olj!",
                "🧠 AJÁNLAT: Mielőtt pusholsz, mindig futtass `git fetch`-et",
                "⚡ TRÜKK: Használd a `git log --oneline --graph --all` parancsot a történet megjelenítésére"
            ],
            "en": [
                "💡 TIP: When multiple people work on a repo, pull more frequently!",
                "🧠 ADVICE: Always run `git fetch` before pushing",
                "⚡ TRICK: Use `git log --oneline --graph --all` to visualize history"
            ]
        },
        "github_actions": {
            "hu": [
                "🤖 MEGJEGYZÉS: A GitHub Action automatikusan módosítja a repót",
                "⏰ TIMING: Dolgozz lokálisan, commitolj, majd futtasd a gghelper-t",
                "🔄 WORKFLOW: GitHub Action → változás → gghelper → push"
            ],
            "en": [
                "🤖 NOTE: GitHub Action automatically modifies the repository",
                "⏰ TIMING: Work locally, commit, then run gghelper",
                "🔄 WORKFLOW: GitHub Action → changes → gghelper → push"
            ]
        },
        "branch_management": {
            "hu": [
                "🌿 STRATÉGIA: Használj feature brancheket új funkciókhoz",
                "🔀 MERGE: `git merge` vs `git rebase` - a rebase tisztább történetet ad",
                "🏷️ TAG: Fontos release-ekhez használj tag-eket"
            ],
            "en": [
                "🌿 STRATEGY: Use feature branches for new features",
                "🔀 MERGE: `git merge` vs `git rebase` - rebase gives cleaner history",
                "🏷️ TAG: Use tags for important releases"
            ]
        },
        "conflict_resolution": {
            "hu": [
                "⚔️ KONFLIKTUS: Két ember ugyanazt a sort módosította",
                "🔧 MEGOLDÁS: Nyisd meg a fájlt, nézd meg a <<<<<<< és >>>>>>> jeleket",
                "✅ JELÖLÉS: Konfliktus feloldása után `git add .`"
            ],
            "en": [
                "⚔️ CONFLICT: Two people modified the same line",
                "🔧 SOLUTION: Open the file, look for <<<<<<< and >>>>>>> markers",
                "✅ MARKING: After resolving conflict, `git add .`"
            ]
        }
    }
    
    @staticmethod
    def get_tip(scenario, lang="en"):
        """Get a random tip for a scenario."""
        import random
        tips = TipsDatabase.TIPS.get(scenario, {}).get(lang, [])
        return random.choice(tips) if tips else ""

# ============================================================================
# INTERACTIVE TUTORIAL SYSTEM
# ============================================================================

class GitTutor:
    """Interactive Git tutor that explains concepts."""
    
    def __init__(self, lang="en", level="intermediate"):
        self.lang = lang
        self.level = level
        self.explanations_given = []
        
    def explain(self, concept, details=None):
        """Explain a Git concept if user is at appropriate level."""
        
        # Skip if expert level
        if self.level == LearningLevel.EXPERT and concept not in ["warning", "error"]:
            return
        
        explanations = {
            "git_add": {
                "hu": {
                    "novice": "📚 A 'git add .' parancs hozzáadja az ÖSSZES változást a 'staging area'-hoz.",
                    "intermediate": "📦 Staging: változások előkészítése commitolásra"
                },
                "en": {
                    "novice": "📚 The 'git add .' command adds ALL changes to the 'staging area'.",
                    "intermediate": "📦 Staging: preparing changes for commit"
                }
            },
            "git_commit": {
                "hu": {
                    "novice": "💾 A commit egy pillanatkép a változásokról. Mindig írj értelmes üzenetet!",
                    "intermediate": "💾 Commit: változások rögzítése történetbe"
                },
                "en": {
                    "novice": "💾 A commit is a snapshot of your changes. Always write meaningful messages!",
                    "intermediate": "💾 Commit: recording changes to history"
                }
            },
            "git_push": {
                "hu": {
                    "novice": "🚀 A push feltölti a commitjaidat a távoli szerverre (pl. GitHub).",
                    "intermediate": "🚀 Push: lokális commitok feltöltése távolira"
                },
                "en": {
                    "novice": "🚀 Push uploads your commits to the remote server (e.g., GitHub).",
                    "intermediate": "🚀 Push: uploading local commits to remote"
                }
            },
            "git_pull_rebase": {
                "hu": {
                    "novice": "🔄 A 'git pull --rebase' letölti a távoli változásokat, majd újraalkalmazza a tiédet.",
                    "intermediate": "🔄 Rebase: újraalapozás a legfrissebb változásokra"
                },
                "en": {
                    "novice": "🔄 'git pull --rebase' downloads remote changes, then reapplies yours on top.",
                    "intermediate": "🔄 Rebase: reapplying changes on newest base"
                }
            },
            "github_actions_conflict": {
                "hu": {
                    "novice": "🤖 A GitHub Action is módosította a repót. Ezért kell először pull-olni!",
                    "intermediate": "🤖 GitHub Action módosított - szinkronizálás szükséges"
                },
                "en": {
                    "novice": "🤖 GitHub Action also modified the repo. That's why we need to pull first!",
                    "intermediate": "🤖 GitHub Action modified - synchronization needed"
                }
            },
            "merge_vs_rebase": {
                "hu": {
                    "novice": "🔀 Merge vs Rebase: merge létrehoz egy új commitot, rebase átrendezi a történetet",
                    "intermediate": "🔀 Merge: új commit, Rebase: történet átrendezése"
                },
                "en": {
                    "novice": "🔀 Merge vs Rebase: merge creates new commit, rebase reorders history",
                    "intermediate": "🔀 Merge: new commit, Rebase: history reordering"
                }
            }
        }
        
        if concept in explanations:
            explanation = explanations[concept][self.lang].get(self.level)
            if explanation and concept not in self.explanations_given:
                print(f"\n{explanation}")
                self.explanations_given.append(concept)
                
                # Show a random tip related to this concept
                if concept == "github_actions_conflict":
                    tip = TipsDatabase.get_tip("github_actions", self.lang)
                elif concept == "merge_vs_rebase":
                    tip = TipsDatabase.get_tip("conflict_resolution", self.lang)
                elif "push" in concept:
                    tip = TipsDatabase.get_tip("multi_user_conflict", self.lang)
                
                if tip and self.level != LearningLevel.EXPERT:
                    print(f"   {tip}")
    
    def ask_quick_quiz(self, question, options, correct_index, explanation):
        """Ask a quick quiz question to reinforce learning."""
        if self.level == LearningLevel.NOVICE and len(self.explanations_given) % 3 == 0:
            print(f"\n🧠 QUICK QUIZ: {question}")
            for i, option in enumerate(options):
                print(f"  {i+1}. {option}")
            
            try:
                answer = input("Válasz (1-3 vagy 'skip'): " if self.lang == "hu" else "Answer (1-3 or 'skip'): ")
                if answer.isdigit() and 1 <= int(answer) <= 3:
                    if int(answer) == correct_index + 1:
                        print("✅ Helyes!" if self.lang == "hu" else "✅ Correct!")
                    else:
                        print(f"❌ Majd legközelebb! {explanation}")
                elif answer.lower() != 'skip':
                    print(f"ℹ️  A helyes válasz: {correct_index + 1}. {explanation}")
            except:
                pass

# ============================================================================
# USER PROGRESS TRACKING
# ============================================================================

class ProgressTracker:
    """Track user progress and suggest next learning steps."""
    
    def __init__(self):
        self.config_path = Path.home() / ".config" / "gghelper"
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.progress_file = self.config_path / "progress.json"
        
    def load_progress(self):
        """Load user progress from file."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "usage_count": 0,
            "last_used": None,
            "scenarios_seen": [],
            "commands_used": {},
            "tips_shown": []
        }
    
    def save_progress(self, progress):
        """Save user progress to file."""
        progress["last_used"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def record_command(self, command):
        """Record that a command was used."""
        progress = self.load_progress()
        progress["usage_count"] = progress.get("usage_count", 0) + 1
        
        if command in progress["commands_used"]:
            progress["commands_used"][command] += 1
        else:
            progress["commands_used"][command] = 1
        
        self.save_progress(progress)
    
    def get_next_learning_step(self, progress):
        """Suggest next learning step based on usage."""
        usage = progress.get("usage_count", 0)
        
        if usage < 3:
            return "first_steps"
        elif usage < 10:
            return "basic_workflow"
        elif usage < 20:
            return "advanced_topics"
        else:
            return "expert_tips"

# ============================================================================
# MAIN SCRIPT WITH ENHANCED LEARNING
# ============================================================================

def run_git_command(cmd, capture=False):
    """Run git command with error handling."""
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

def interactive_commit_workflow(tutor, lang):
    """Interactive commit message input with learning."""
    
    instructions = {
        "hu": {
            "header": "✍️  COMMIT ÜZENET MEGADÁSA",
            "instructions": """• Írd vagy másold be az üzenetet
• Egy üres sor, majd Ctrl+D a befejezéshez
• Ctrl+C a megszakításhoz""",
            "empty_error": "❌ Üres üzenet!",
            "preview": "🔍 Előnézet (ezt fogom commitolni):",
            "confirm": "Opciók: [i]gen / [e]dit / [n]em: ",
            "edit_prompt": "Nyomj Enter-t a szerkesztéshez, vagy 'n' a megszakításhoz: ",
            "good_practice": "💡 JÓ GYAKORLAT: Használj rövid, leíró commit üzeneteket!"
        },
        "en": {
            "header": "✍️  ENTER COMMIT MESSAGE",
            "instructions": """• Type or paste your message
• Empty line + Ctrl+D to finish
• Ctrl+C to cancel""",
            "empty_error": "❌ Empty message!",
            "preview": "🔍 Preview (this will be committed):",
            "confirm": "Options: [y]es / [e]dit / [n]o: ",
            "edit_prompt": "Press Enter to edit, or 'n' to cancel: ",
            "good_practice": "💡 GOOD PRACTICE: Use short, descriptive commit messages!"
        }
    }
    
    text = instructions[lang]
    
    print(f"\n{text['header']}")
    print(text['instructions'])
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
        print(f"\n{'❌ Megszakítva' if lang == 'hu' else '❌ Cancelled'}")
        return None
    
    message = "\n".join(lines).strip()
    
    if not message:
        print(f"\n{text['empty_error']}")
        return None
    
    # Show good practice tip for novices
    if tutor.level == LearningLevel.NOVICE:
        print(f"\n{text['good_practice']}")
    
    while True:
        print(f"\n{text['preview']}")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        choice = input(f"{text['confirm']}").lower()
        
        if choice in ['y', 'i', 'yes', 'igen']:
            return message
        elif choice in ['e', 'edit']:
            # Edit in editor
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(message)
                temp_path = f.name
            
            try:
                editor = os.getenv('EDITOR', 'nano')
                subprocess.run([editor, temp_path])
                
                with open(temp_path, 'r') as f:
                    edited_message = f.read().strip()
                
                os.unlink(temp_path)
                
                if not edited_message:
                    print(f"\n{text['empty_error']}")
                    return None
                
                message = edited_message
            except Exception as e:
                print(f"Error: {e}")
                return message
        elif choice in ['n', 'no', 'nem']:
            return None
        else:
            continue

def show_smart_help(args, tutor, progress_tracker):
    """Show contextual help based on user's situation."""
    
    # Check current git status
    try:
        status = run_git_command(["status", "--porcelain"], capture=True)
        has_changes = bool(status)
        
        branch = run_git_command(["branch", "--show-current"], capture=True)
        
        # Check if we're behind remote
        run_git_command(["fetch", "origin"], capture=True)
        local = run_git_command(["rev-parse", "@"], capture=True)
        remote = run_git_command(["rev-parse", "@{u}"], capture=True)
        behind_remote = local != remote
        
    except:
        has_changes = False
        behind_remote = False
        branch = "unknown"
    
    # Show contextual help
    print("\n" + "="*60)
    print("🤔 CONTEXTUAL HELP BASED ON YOUR SITUATION")
    print("="*60)
    
    if not has_changes:
        print("📭 No uncommitted changes detected.")
        print("   Try making some changes first, then run 'gghelper'")
    
    if behind_remote:
        print("🔄 Remote repository has newer changes.")
        print("   Use 'gghelper --resolve-only' to sync first")
    
    # Show usage statistics
    progress = progress_tracker.load_progress()
    usage_count = progress.get("usage_count", 0)
    
    print(f"\n📊 YOUR STATS: Used {usage_count} time{'s' if usage_count != 1 else ''}")
    
    if usage_count > 0:
        print("\n🎓 NEXT LEARNING STEP:")
        next_step = progress_tracker.get_next_learning_step(progress)
        
        if next_step == "first_steps":
            print("   • Try making your first commit with 'gghelper'")
            print("   • Learn about 'git add', 'git commit', 'git push'")
        elif next_step == "basic_workflow":
            print("   • Experiment with 'gghelper --resolve-only'")
            print("   • Learn about merge conflicts")
        elif next_step == "advanced_topics":
            print("   • Try 'gghelper --safe' to see merge vs rebase")
            print("   • Learn about branching strategies")
        else:
            print("   • You're doing great! Consider helping others learn Git")
    
    print("\n💡 QUICK COMMANDS:")
    print("   gghelper                    # Normal workflow")
    print("   gghelper --resolve-only     # Sync with remote")
    print("   gghelper --safe            # Use merge instead of rebase")
    print("   gghelper --lang hu         # Hungarian interface")
    print("\n📚 LEARNING RESOURCES:")
    print("   https://git-scm.com/book      # Pro Git book (free!)")
    print("   https://ohmygit.org/          # Git learning game")
    print("="*60)

def main():
    """Main entry point with enhanced learning features."""
    
    parser = argparse.ArgumentParser(
        description="gghelper - Git Workflow Mentor",
        add_help=False
    )
    
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done")
    parser.add_argument("--resolve-only", action="store_true", 
                       help="Only resolve conflicts")
    parser.add_argument("--safe", action="store_true", 
                       help="Use merge instead of rebase")
    parser.add_argument("--lang", choices=["en", "hu"], 
                       help="Force language")
    parser.add_argument("--level", choices=["novice", "intermediate", "expert", "auto"],
                       help="Learning level (auto = detect from git history)")
    parser.add_argument("--help", "-h", action="store_true", 
                       help="Show contextual help")
    parser.add_argument("--smart-help", action="store_true",
                       help="Show smart help based on current situation")
    parser.add_argument("--stats", action="store_true",
                       help="Show your usage statistics")
    parser.add_argument("--version", "-v", action="store_true", 
                       help="Show version")
    
    args = parser.parse_args()
    
    # Detect language
    lang = args.lang or ("hu" if os.getenv("LANG", "").startswith("hu") else "en")
    
    # Initialize progress tracker
    progress_tracker = ProgressTracker()
    
    # Handle special commands
    if args.smart_help:
        tutor = GitTutor(lang, "intermediate")
        show_smart_help(args, tutor, progress_tracker)
        return 0
    
    if args.stats:
        progress = progress_tracker.load_progress()
        print("\n📊 YOUR GGHELPER STATISTICS")
        print("="*40)
        print(f"Total uses: {progress.get('usage_count', 0)}")
        if progress.get('last_used'):
            last_used = datetime.fromisoformat(progress['last_used'])
            print(f"Last used: {last_used.strftime('%Y-%m-%d %H:%M')}")
        
        if progress.get('commands_used'):
            print("\nMost used commands:")
            for cmd, count in sorted(progress['commands_used'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {cmd}: {count} times")
        
        # Suggest next steps
        next_step = progress_tracker.get_next_learning_step(progress)
        print(f"\n🎯 Next learning step: {next_step}")
        return 0
    
    if args.help or args.version:
        # Simple help/version
        if args.version:
            print("gghelper v2.0.0 - Git Workflow Mentor")
            return 0
        else:
            tutor = GitTutor(lang, "intermediate")
            show_smart_help(args, tutor, progress_tracker)
            return 0
    
    # Determine learning level
    if args.level == "auto" or not args.level:
        level = LearningLevel.detect_from_history()
    else:
        level = args.level
    
    # Initialize tutor
    tutor = GitTutor(lang, level)
    
    # Record this usage
    progress_tracker.record_command("gghelper")
    
    # Start with a welcome message
    welcome = {
        "hu": f"\n🎉 Üdv a gghelper-ben! (Szint: {level})",
        "en": f"\n🎉 Welcome to gghelper! (Level: {level})"
    }
    print(welcome[lang])
    
    if level == LearningLevel.NOVICE:
        intro = {
            "hu": "Ez a program segít megtanulni a Git használatát. Figyelj az útmutatásokra!",
            "en": "This program helps you learn Git. Pay attention to the guidance!"
        }
        print(intro[lang])
    
    try:
        # Step 1: Check repo and add changes
        print(f"\n{'1. 🔍 Mappa ellenőrzése...' if lang == 'hu' else '1. 🔍 Checking repository...'}")
        run_git_command(["status"])
        tutor.explain("git_add")
        
        print(f"\n{'2. 📦 Változások hozzáadása...' if lang == 'hu' else '2. 📦 Adding changes...'}")
        run_git_command(["add", "."])
        progress_tracker.record_command("git_add")
        
        # Step 2: Commit (unless resolve-only)
        if not args.resolve_only:
            print(f"\n{'3. 💾 Commit készítése...' if lang == 'hu' else '3. 💾 Creating commit...'}")
            tutor.explain("git_commit")
            
            message = interactive_commit_workflow(tutor, lang)
            if message:
                run_git_command(["commit", "-m", message])
                progress_tracker.record_command("git_commit")
            else:
                return 0
        else:
            print(f"\n{'ℹ️  Csak szinkronizálás mód...' if lang == 'hu' else 'ℹ️  Sync-only mode...'}")
        
        # Step 3: Check remote
        print(f"\n{'4. 🌐 Távoli repo ellenőrzése...' if lang == 'hu' else '4. 🌐 Checking remote...'}")
        run_git_command(["fetch", "origin"])
        
        local = run_git_command(["rev-parse", "@"], capture=True)
        remote = run_git_command(["rev-parse", "@{u}"], capture=True)
        
        # Step 4: Handle conflicts if needed
        if local != remote:
            print(f"\n{'5. ⚙️  Konfliktusok kezelése...' if lang == 'hu' else '5. ⚙️  Handling conflicts...'}")
            tutor.explain("github_actions_conflict")
            
            if args.safe:
                tutor.explain("merge_vs_rebase")
                print(f"{'🔀 Biztonságos merge használata...' if lang == 'hu' else '🔀 Using safe merge...'}")
                current_branch = run_git_command(["branch", "--show-current"], capture=True)
                run_git_command(["pull", "--no-rebase", "origin", current_branch])
                progress_tracker.record_command("git_merge")
            else:
                tutor.explain("git_pull_rebase")
                print(f"{'🔄 Rebase használata...' if lang == 'hu' else '🔄 Using rebase...'}")
                current_branch = run_git_command(["branch", "--show-current"], capture=True)
                try:
                    run_git_command(["pull", "--rebase", "origin", current_branch])
                    progress_tracker.record_command("git_rebase")
                except subprocess.CalledProcessError:
                    print(f"{'❌ Konfliktus! A tutor segít megoldani.' if lang == 'hu' else '❌ Conflict! Tutor will help resolve.'}")
                    tutor.explain("conflict_resolution")
                    
                    # Ask quiz about conflict resolution
                    if level == LearningLevel.NOVICE:
                        quiz = {
                            "hu": ("Mi az első lépés konfliktus feloldásakor?", 
                                   ["git push --force", "git status", "git commit --amend"], 
                                   1,
                                   "Először nézd meg, mely fájlokban van konfliktus: git status"),
                            "en": ("What's the first step in conflict resolution?",
                                   ["git push --force", "git status", "git commit --amend"],
                                   1,
                                   "First check which files have conflicts: git status")
                        }
                        tutor.ask_quick_quiz(*quiz[lang])
                    return 1
        
        # Step 5: Push
        print(f"\n{'6. 🚀 Push GitHubra...' if lang == 'hu' else '6. 🚀 Pushing to GitHub...'}")
        tutor.explain("git_push")
        run_git_command(["push"])
        progress_tracker.record_command("git_push")
        
        # Success message with learning encouragement
        success_messages = {
            "hu": [
                "✅ SIKER! Jó munka!",
                "✅ Kész! Egyre jobb leszel!",
                "✅ Nagyszerű! Következő alkalommal próbáld ki a --resolve-only opciót!"
            ],
            "en": [
                "✅ SUCCESS! Great job!",
                "✅ Done! You're getting better!",
                "✅ Excellent! Next time try the --resolve-only option!"
            ]
        }
        
        import random
        print(f"\n{random.choice(success_messages[lang])}")
        
        # Show progress
        progress = progress_tracker.load_progress()
        if progress["usage_count"] % 5 == 0:
            milestone = {
                "hu": f"🎯 Mérföldkő: {progress['usage_count']} alkalommal használtad a gghelper-t!",
                "en": f"🎯 Milestone: You've used gghelper {progress['usage_count']} times!"
            }
            print(f"\n{milestone[lang]}")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{'⏹️  Megszakítva' if lang == 'hu' else '⏹️  Cancelled'}")
        return 1
    except Exception as e:
        print(f"\n{'❌ Hiba:' if lang == 'hu' else '❌ Error:'} {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
