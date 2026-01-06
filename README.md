# gghelper

Git workflow assistant that automatically handles GitHub Actions conflicts.

## What It Does

When GitHub Actions modifies your repository (like package build scripts), you get this error:

```
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

**gghelper** detects this and resolves it automatically!

## Quick Start

```bash
# In any git repository:
gghelper

# If you only need to resolve conflicts:
gghelper --resolve-only

# For safer conflict resolution (uses merge):
gghelper --safe
```

## Installation

This package is included in the manjaro-awesome repository. To install manually:

```bash
# Build from source:
makepkg -si

# Or install files manually:
sudo cp gghelper.py /usr/bin/
sudo cp gghelper /usr/bin/
sudo chmod +x /usr/bin/gghelper /usr/bin/gghelper.py
```

## Usage Examples

### Normal workflow:
```bash
cd ~/my-project
gghelper
```
This will: add changes → commit → check remote → resolve conflicts → push

### After GitHub Action runs:
```bash
gghelper --resolve-only
```
Only syncs with remote, no new commit.

### Hungarian interface:
```bash
gghelper --lang hu
```

## How It Works

1. **Detects remote changes** - Checks if GitHub Action modified the repository
2. **Automatic resolution** - Uses `git pull --rebase` by default
3. **Safe fallback** - Can use `--safe` flag for merge instead of rebase
4. **User-friendly** - Clear messages and prompts

## Common Issues

### "Updates were rejected"
```bash
# Run this:
gghelper --resolve-only

# Or manually:
git pull --rebase
git push
```

### Merge conflicts
If automatic resolution fails:
1. Check: `git status`
2. Fix conflicting files
3. Mark resolved: `git add .`
4. Continue: `git rebase --continue`
5. Run `gghelper` again

## Author

Gyöngyösi Gábor  
Website: links.gshoots.hu  
GitHub: megvadulthangya

## License

MIT License - See LICENSE file
```
