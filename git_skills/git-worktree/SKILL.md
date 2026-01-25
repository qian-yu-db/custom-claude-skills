---
name: git-worktree
description: Manage git worktrees with smart automation. Create worktrees with auto-setup (dependencies, env files), list worktrees with merge status, clean up stale worktrees, and switch between worktrees. Use when working on multiple branches simultaneously, doing quick bug fixes, or reviewing PRs without stashing.
version: 1.0.0
author: Custom Skills
tags: [git, worktree, workflow, branches, parallel-development]
---

# Git Worktree Skill

## Purpose

This skill provides enhanced git worktree management with automation beyond raw CLI commands:
- **Auto-setup**: Install dependencies and copy env files when creating worktrees
- **Smart listing**: Show worktrees with merge status and staleness indicators
- **Easy cleanup**: Remove worktrees for merged branches
- **Context switching**: Quick navigation between worktrees

## When to Activate

This skill should activate when the user requests:
- "Create a worktree for feature-x"
- "List my worktrees"
- "Clean up merged worktrees"
- "Switch to worktree for branch X"
- "Work on multiple branches at once"
- "Set up a worktree for PR review"
- `/worktree-add`, `/worktree-list`, `/worktree-clean`

## Slash Commands

### `/worktree-add <branch>`

Create a new worktree with optional auto-setup.

**Syntax:**
```
/worktree-add <branch> [--no-setup] [--path <custom-path>]
```

**What it does:**
1. Creates worktree in sibling directory: `../<repo-name>-<branch>`
2. Detects package manager (uv, npm, yarn, pnpm, pip)
3. Installs dependencies automatically
4. Copies common env files (.env, .env.local) if they exist
5. Reports the worktree path

**Example:**
```
/worktree-add feature/auth
```
Creates `../my-project-feature-auth/` with deps installed.

---

### `/worktree-list`

List all worktrees with status information.

**Syntax:**
```
/worktree-list [--verbose]
```

**Output includes:**
- Worktree path
- Branch name
- Merge status (merged to main/master or not)
- Last commit date
- Stale indicator (no commits in 30+ days)

**Example output:**
```
Worktrees for my-project:

  PATH                              BRANCH              STATUS
  /path/to/my-project               main                (bare)
  /path/to/my-project-feature-auth  feature/auth        active, 2 days ago
  /path/to/my-project-bugfix-123    bugfix/123          MERGED, stale (45 days)
  /path/to/my-project-old-feature   feature/old         stale (90 days)
```

---

### `/worktree-clean`

Remove worktrees for branches that have been merged.

**Syntax:**
```
/worktree-clean [--dry-run] [--include-stale] [--force]
```

**Options:**
- `--dry-run`: Show what would be removed without removing
- `--include-stale`: Also remove worktrees with no commits in 30+ days
- `--force`: Skip confirmation prompt

**What it does:**
1. Finds worktrees where branch is merged to main/master
2. Shows list and asks for confirmation
3. Runs `git worktree remove` for each
4. Optionally prunes tracking references

---

## Core Workflows

### Workflow 1: Create Worktree with Full Setup

```bash
# 1. Create worktree
git worktree add "../${REPO_NAME}-${BRANCH_SAFE}" "${BRANCH}"

# 2. Navigate to worktree
cd "../${REPO_NAME}-${BRANCH_SAFE}"

# 3. Detect and install dependencies
if [ -f "uv.lock" ] || [ -f "pyproject.toml" ]; then
    uv sync
elif [ -f "package-lock.json" ]; then
    npm install
elif [ -f "yarn.lock" ]; then
    yarn install
elif [ -f "pnpm-lock.yaml" ]; then
    pnpm install
elif [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
fi

# 4. Copy env files from main worktree
for envfile in .env .env.local .env.development; do
    if [ -f "../${REPO_NAME}/${envfile}" ]; then
        cp "../${REPO_NAME}/${envfile}" .
    fi
done
```

### Workflow 2: List Worktrees with Status

```bash
# Get all worktrees
git worktree list --porcelain

# For each worktree, check if merged
for branch in $(git worktree list --porcelain | grep "^branch" | cut -d' ' -f2); do
    # Check if merged to main
    if git branch --merged main | grep -q "${branch#refs/heads/}"; then
        echo "${branch}: MERGED"
    fi

    # Check last commit date
    last_commit=$(git log -1 --format="%cr" "${branch}")
    echo "  Last commit: ${last_commit}"
done
```

### Workflow 3: Clean Merged Worktrees

```bash
# Find merged worktrees
merged_worktrees=()
for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
    branch=$(git -C "$wt" branch --show-current)
    if git branch --merged main | grep -q "$branch"; then
        merged_worktrees+=("$wt")
    fi
done

# Remove each
for wt in "${merged_worktrees[@]}"; do
    echo "Removing: $wt"
    git worktree remove "$wt"
done

# Prune stale references
git worktree prune
```

## Package Manager Detection

The skill auto-detects package managers in this order:

| File Present | Package Manager | Install Command |
|--------------|-----------------|-----------------|
| `uv.lock` or `pyproject.toml` | uv | `uv sync` |
| `package-lock.json` | npm | `npm install` |
| `yarn.lock` | yarn | `yarn install` |
| `pnpm-lock.yaml` | pnpm | `pnpm install` |
| `requirements.txt` | uv (pip compat) | `uv pip install -r requirements.txt` |
| `Gemfile.lock` | bundler | `bundle install` |
| `go.mod` | go | `go mod download` |

## Path Naming Convention

Worktrees are created as sibling directories with sanitized branch names:

```
/path/to/my-project/           # Main worktree
/path/to/my-project-feature-auth/    # feature/auth branch
/path/to/my-project-bugfix-123/      # bugfix/123 branch
/path/to/my-project-release-v2/      # release/v2 branch
```

**Sanitization rules:**
- Replace `/` with `-`
- Replace spaces with `-`
- Remove special characters
- Lowercase everything

## Integration with Claude Code

When using worktrees with Claude Code:

1. **After creating a worktree**, Claude can add it to additional working directories
2. **When switching context**, Claude can focus on the specific worktree
3. **For cleanup**, Claude handles the git operations automatically

## Best Practices

### 1. Use for PR Reviews
```
/worktree-add pr-123-review
```
Review code without disrupting your current work.

### 2. Quick Bug Fixes
```
/worktree-add hotfix/critical-bug
```
Fix and deploy while keeping feature work intact.

### 3. Regular Cleanup
```
/worktree-clean --dry-run
```
Run weekly to keep your workspace tidy.

### 4. Parallel Testing
Create multiple worktrees to test different branches simultaneously.

## Common Issues

### "fatal: is already checked out"
The branch is already checked out in another worktree. Use `/worktree-list` to find it.

### Worktree shows as "prunable"
The worktree directory was deleted but not properly removed. Run:
```bash
git worktree prune
```

### Dependencies out of sync
When switching between worktrees, dependencies may differ. Always run the appropriate install command after switching.

## Reference Commands

Quick reference for raw git commands:

```bash
# Create worktree
git worktree add <path> <branch>

# Create worktree with new branch
git worktree add -b <new-branch> <path> <start-point>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Prune stale entries
git worktree prune

# Lock worktree (prevent pruning)
git worktree lock <path>

# Unlock worktree
git worktree unlock <path>
```

## Tips for Claude

When handling worktree requests:

1. **Always check if branch exists** before creating worktree
2. **Sanitize branch names** for filesystem-safe paths
3. **Detect package manager** and install deps automatically
4. **Copy env files** only if they exist in main worktree
5. **Show clear status** with merge info and staleness
6. **Confirm before cleanup** unless `--force` is specified
7. **Report the new path** so user knows where to find it
