# Git Worktree Skill

Enhanced git worktree management with smart automation.

## Quick Start

```bash
# Create worktree with auto-setup
/worktree-add feature/new-auth

# List all worktrees with status
/worktree-list

# Clean up merged worktrees
/worktree-clean
```

## Why Use This Over Raw Git CLI?

| Feature | Raw Git CLI | This Skill |
|---------|-------------|------------|
| Create worktree | `git worktree add ...` | Same + auto-install deps |
| Copy env files | Manual | Automatic |
| List with merge status | Multiple commands | Single command |
| Clean merged worktrees | Manual per-worktree | Batch with confirmation |
| Path naming | You decide | Consistent convention |

## Commands

### `/worktree-add <branch>`
Creates worktree at `../<repo>-<branch>/` with:
- Dependencies installed (detects uv, npm, yarn, pnpm)
- Env files copied (.env, .env.local)

### `/worktree-list`
Shows all worktrees with:
- Branch name
- Merge status (merged to main or not)
- Last commit date
- Staleness indicator

### `/worktree-clean`
Removes worktrees where the branch has been merged. Use `--dry-run` to preview.

## Use Cases

1. **PR Review**: Create worktree, review code, delete when done
2. **Hotfix**: Work on fix without stashing current changes
3. **Parallel Development**: Multiple features simultaneously
4. **Testing**: Run tests on one branch while developing on another

## Installation

Add this skill to your Claude Code configuration to enable the slash commands.

See [SKILL.md](./SKILL.md) for detailed documentation.
