# Git Worktree Quick Reference

## Slash Commands

| Command | Description |
|---------|-------------|
| `/worktree-add <branch>` | Create worktree with auto-setup |
| `/worktree-add <branch> --no-setup` | Create without installing deps |
| `/worktree-list` | List all worktrees with status |
| `/worktree-list --verbose` | Detailed worktree info |
| `/worktree-clean` | Remove merged worktrees |
| `/worktree-clean --dry-run` | Preview what would be removed |
| `/worktree-clean --include-stale` | Also remove stale (30+ days) |

## Path Convention

```
/project/           → main worktree
/project-feature-x/ → feature/x branch
/project-bugfix-42/ → bugfix/42 branch
```

## Raw Git Commands

```bash
git worktree add <path> <branch>     # Create
git worktree add -b <new> <path>     # Create with new branch
git worktree list                     # List all
git worktree remove <path>            # Remove
git worktree prune                    # Clean stale refs
```

## Package Manager Detection

| Lock File | Command |
|-----------|---------|
| uv.lock / pyproject.toml | `uv sync` |
| package-lock.json | `npm install` |
| yarn.lock | `yarn install` |
| pnpm-lock.yaml | `pnpm install` |
| requirements.txt | `uv pip install -r requirements.txt` |

## Common Workflows

**Quick PR Review:**
```
/worktree-add pr-123
# review code
/worktree-clean
```

**Hotfix while on feature:**
```
/worktree-add hotfix/urgent
# fix, commit, push
git worktree remove ../project-hotfix-urgent
```

**Weekly Cleanup:**
```
/worktree-clean --dry-run
/worktree-clean
```
