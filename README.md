# gghelper - Git Workflow Mentor & Assistant

A smart Git assistant that not only automates your workflow but also teaches you Git concepts as you use it. Perfect for handling GitHub Actions conflicts and learning Git in a team environment.

## ✨ Features

### 🤖 **Automation**
- Automatic detection of GitHub Actions conflicts
- Interactive commit message editing (with nano/editor support)
- Auto-resolution with rebase or merge options
- One-command workflow: `add → commit → resolve → push`

### 🎓 **Learning System**
- **Adaptive learning levels**: Novice → Intermediate → Expert
- **Contextual explanations**: Git concepts explained when relevant
- **Quick quizzes**: Reinforce learning without interrupting workflow
- **Progress tracking**: Stats and milestones in `~/.config/gghelper/`

### 🛡️ **Safety Features**
- Dry-run mode: `--dry-run` to preview actions
- Safe mode: `--safe` uses merge instead of rebase
- Conflict detection with step-by-step guidance
- No destructive operations without confirmation

### 🌐 **International**
- Auto-detects system language (Hungarian/English)
- Force language with `--lang hu` or `--lang en`
- Culturally relevant tips and explanations

## 🚀 Quick Start

### Installation

As of v3.0.0 gghelper is a regular Python package with a thin bash
wrapper. Install options:

```bash
# pip install (recommended)
git clone https://github.com/megvadulthangya/gghelper
cd gghelper
pip install .

# Optional: watch-mode TUI (Nord-themed repo picker)
pip install '.[tui]'

# From a local checkout without pip — the bash wrapper finds the
# package via PYTHONPATH automatically.
git clone https://github.com/megvadulthangya/gghelper
ln -s "$PWD/gghelper/gghelper" ~/.local/bin/gghelper
```

After ``pip install .`` the ``gghelper`` console script and
``python -m gghelper`` both work everywhere.

### Basic Usage

```bash
cd /your/git/repository
gghelper
```

That's it! The interactive guide will walk you through:
1. Scanning for changes
2. Adding changes to staging
3. **Writing commit message** (multi-line, with edit option)
4. **Confirming the commit** (yes/edit/no)
5. Checking remote status
6. Resolving conflicts if needed
7. Pushing to GitHub

## 📖 Detailed Usage

### The Core Workflow (YES, it's still there!)

```bash
gghelper
```
This triggers the familiar interactive workflow:
1. **Adds all changes** (`git add .`)
2. **Asks for commit message** (multi-line, Ctrl+D to finish)
3. **Shows preview and asks**: [y]es / [e]dit / [n]o
   - Press `e` to edit in your default editor (nano by default)
   - Press `y` to proceed with the commit
   - Press `n` to cancel
4. **Checks remote** for GitHub Actions changes
5. **Resolves conflicts** automatically (or guides you if manual needed)
6. **Pushes** to GitHub

### Special Modes

```bash
# Only resolve conflicts (when GitHub Action modified repo)
gghelper --resolve-only

# Use merge instead of rebase (safer, creates merge commit)
gghelper --safe

# Force Hungarian / English language
gghelper --lang hu
gghelper --lang en

# Show what would happen without touching anything
gghelper --dry-run

# Contextual help based on the current repo state
gghelper --smart-help

# Usage statistics (real, backed by ~/.config/gghelper/progress.json)
gghelper --stats

# Learning level
gghelper --level novice        # Full explanations
gghelper --level intermediate  # Short notes (default when auto)
gghelper --level expert        # Action-only, no extra prose
gghelper --level auto          # Behave as intermediate

# Watch multiple repos for remote changes (e.g. CI running)
gghelper --watch                    # Poll every 5 min
gghelper --watch --interval 60      # Poll every 60 s
gghelper --watch-config             # Pick watched repos (Nord TUI)
```

## 🎯 Learning Features

### Adaptive Learning Levels

gghelper detects your experience level and adjusts explanations:

- **Novice**: Detailed step-by-step explanations, quick quizzes
- **Intermediate**: Moderate explanations, tips
- **Expert**: Minimal explanations, just the actions

### Progress Tracking

Your usage is tracked (locally, in `~/.config/gghelper/progress.json`):
- How many times you've used gghelper
- Which Git commands you use most
- Milestones at 5, 10, 20 uses
- Suggested next learning steps

### Smart Help

```bash
gghelper --smart-help
```

This analyzes your current repository situation and gives specific advice:
- Are there uncommitted changes?
- Is the remote ahead of local?
- What commands should you run next?

## 🔧 Common Scenarios

### 1. GitHub Action Modified Repository

**Symptom:** "Updates were rejected because the remote contains work"

**Solution:**
```bash
# Let gghelper handle it automatically
gghelper --resolve-only

# Or use normal workflow - it will detect and resolve
gghelper
```

### 2. Merge Conflicts During Rebase

**Symptom:** Automatic resolution fails

**Solution:**
1. gghelper stops and shows manual steps
2. Check conflicts: `git status`
3. Open files, look for `<<<<<<<`, `=======`, `>>>>>>>` markers
4. Choose which changes to keep, remove markers
5. Mark as resolved: `git add .`
6. Continue: `git rebase --continue`
7. Run `gghelper` again or `git push`

### 3. Team Collaboration Tips

When multiple people work on the same repository:

```bash
# Frequent synchronization
gghelper --resolve-only

# Or set up a pre-push hook
echo '#!/bin/bash
git fetch origin
if [ "$(git rev-parse @)" != "$(git rev-parse @{u})" ]; then
    echo "Remote has changes. Running gghelper --resolve-only..."
    gghelper --resolve-only
fi' > .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

## 📊 Example Session

```
$ gghelper

🎉 Welcome to gghelper! (Level: intermediate)

1. 🔍 Checking repository...
   (Shows git status output)

2. 📦 Adding changes...
   📦 Staging: preparing changes for commit

3. 💾 Creating commit...

✍️  ENTER COMMIT MESSAGE
• Type or paste your message
• Empty line + Ctrl+D to finish
• Ctrl+C to cancel
---
Fixed login bug and updated documentation
Added password validation
Improved error messages
---

🔍 Preview (this will be committed):
---
Fixed login bug and updated documentation
Added password validation
Improved error messages
---

Options: [y]es / [e]dit / [n]o: y

4. 🌐 Checking remote...

5. ⚙️  Handling conflicts...
   ⚠️  Remote repository has changed (GitHub Action)!
   Try to resolve automatically? [y/n]: y
   🔄 Using rebase...

6. 🚀 Pushing to GitHub...
   🚀 Push: uploading local commits to remote

✅ SUCCESS! Great job!
```

## 🏗️ Architecture (v3.0.0)

gghelper is a modular Python package:

```
src/gghelper/
├── __init__.py       # __version__
├── __main__.py       # python -m gghelper entry point
├── cli.py            # argparse + dispatch
├── config.py         # ~/.config/gghelper/config.json I/O
├── git_ops.py        # thin git plumbing wrappers
├── commit.py         # commit message prompt + convention checks
├── workflow.py       # add → commit → remote sync → push
├── progress.py       # progress.json (stats)
├── smart_help.py     # --smart-help contextual advice
├── watch.py          # --watch background monitoring
├── i18n.py           # all user-facing strings (hu/en + levels)
└── tui/
    └── watch_config.py  # Nord-themed textual TUI
```

Plus ``gghelper`` (bash wrapper) and ``pyproject.toml`` for packaging.

## 📝 For Developers

### Extending gghelper

All strings live in ``i18n.py``. To add a new message:

```python
# src/gghelper/i18n.py
MESSAGES["my_new_key"] = {
    "hu": "Új üzenet",
    "en": "New message",
}
# Use it
from gghelper import i18n
print(i18n.msg("my_new_key", lang))
```

For level-aware messages (novice/intermediate/expert), add to
``LEVEL_MESSAGES`` and read with ``i18n.level_msg(key, lang, level)``.
Expert values are typically empty strings — experts don't want prose.

### Testing

```bash
# Dry-run to see what would happen
gghelper --dry-run

# Test with a dummy repository
mkdir test-repo && cd test-repo
git init
echo "test" > file.txt
gghelper --dry-run
```

## ⚙️ Configuration Management (NEW in v2.1.0!)

### Permanent Settings
Set your preferences once and gghelper will remember them forever!

```bash
# Set language permanently
gghelper --set-lang hu      # Hungarian forever!
gghelper --set-lang en      # English forever!

# Set learning level
gghelper --set-level novice      # Detailed explanations
gghelper --set-level intermediate # Moderate explanations  
gghelper --set-level expert      # Minimal explanations (like original)
gghelper --set-level auto        # Auto-detect (default)

# Both at once
gghelper --set-lang hu --set-level expert
```

### Config File
Settings live in `~/.config/gghelper/config.json`:
```json
{
  "language": "hu",
  "level": "expert",
  "watched_repos": ["/home/me/code/project-a", "/home/me/code/project-b"]
}
```

Run statistics (counts, conflicts, timestamps) live in
`~/.config/gghelper/progress.json` and are shown by `gghelper --stats`.

Old v2.x configs are forward-compatible — unknown keys are preserved
and missing ones fall back to sensible defaults.

### Reset Configuration
```bash
rm -rf ~/.config/gghelper
```

### For Hungarian Users 🇭🇺
```bash
# Csak egyszer futtasd:
gghelper --set-lang hu

# Innentől mindig magyar:
gghelper  # automatikusan magyarul!
```

## ❓ FAQ

### Q: Is my data tracked or sent anywhere?
**A:** No. All progress tracking is local (`~/.config/gghelper/`). No data leaves your computer.

### Q: Can I use this in CI/CD pipelines?
**A:** Yes, but use `--resolve-only` and appropriate levels. For automation, consider expert level.

### Q: What if I don't want the learning features?
**A:** Use `--level expert` or they'll automatically reduce as you gain experience.

### Q: How do I reset my progress?
**A:** Delete `~/.config/gghelper/progress.json`

### Q: Can I use a different text editor?
**A:** Yes, set the `EDITOR` environment variable:
```bash
export EDITOR=vim
gghelper  # Will use vim for editing commit messages
```

## 👨‍💻 Author

**Gyöngyösi Gábor**  
- GitHub: [@megvadulthangya](https://github.com/megvadulthangya)
- Website: [links.gshoots.hu](https://links.gshoots.hu)

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

*gghelper - Because Git should be helpful, not headache-inducing!* 🚀

