# Git Skills Marketplace

This directory is a **Claude Code plugin marketplace** containing git-related plugins.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [git-worktree](git-worktree/) | Manage git worktrees with auto-setup, merge status, and cleanup |

## Installation

### 1. Add the Marketplace

```bash
claude plugin marketplace add /path/to/custom-claude-skills/git_skills
```

### 2. Install Plugins

```bash
claude plugin install git-worktree@custom-git-skills
```

### 3. Restart Claude Code

After installation, restart Claude Code for changes to take effect.

## Commands

After installation, commands are available with the plugin namespace prefix:

- `/git-worktree:worktree-add <branch>` - Create worktree with auto-setup
- `/git-worktree:worktree-list` - List worktrees with merge status
- `/git-worktree:worktree-clean` - Remove merged worktrees

## Managing Plugins

```bash
# List installed plugins
claude plugin list

# Enable/disable a plugin
claude plugin enable git-worktree@custom-git-skills
claude plugin disable git-worktree@custom-git-skills

# Uninstall
claude plugin uninstall git-worktree@custom-git-skills

# Update marketplace
claude plugin marketplace update custom-git-skills
```
