---
name: git-worktree
description: Manage git worktrees with smart automation. Create worktrees with auto-setup (dependencies, env files), list worktrees with merge status, clean up stale worktrees, and switch between worktrees. Use when working on multiple branches simultaneously, doing quick bug fixes, or reviewing PRs without stashing.
version: 1.0.0
author: Custom Skills
tags: [git, worktree, workflow, branches, parallel-development]
---

# Git Worktree Skill

Enhanced git worktree management with automation beyond raw CLI commands.

## Available Commands

| Command | Description |
|---------|-------------|
| `/worktree-add <branch>` | Create worktree with auto-setup |
| `/worktree-list` | List worktrees with merge status |
| `/worktree-clean` | Remove merged worktrees |

## Quick Examples

```bash
# Create worktree for a branch
/worktree-add feature/auth

# See all worktrees with status
/worktree-list

# Clean up merged worktrees
/worktree-clean --dry-run
/worktree-clean
```

## When to Use

- Working on multiple branches simultaneously
- Quick bug fixes without stashing
- Reviewing PRs in isolation
- Testing different versions in parallel

## Key Features

- **Auto-setup**: Installs dependencies and copies env files
- **Smart listing**: Shows merge status and staleness indicators
- **Safe cleanup**: Only removes merged branches, with confirmation

## Path Convention

Worktrees are created as sibling directories:
```
/project/               → main worktree
/project-feature-auth/  → feature/auth branch
/project-bugfix-42/     → bugfix/42 branch
```

## Package Manager Detection

Automatically detects and runs:
- `uv sync` for Python (uv.lock/pyproject.toml)
- `npm install` for Node (package-lock.json)
- `yarn install` for Yarn (yarn.lock)
- `pnpm install` for pnpm (pnpm-lock.yaml)

See individual command files in `commands/` for detailed documentation.
