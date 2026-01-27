---
allowed-tools: Bash(git worktree:*), Bash(git branch:*), Bash(git log:*), Bash(git -C:*)
description: List all git worktrees with merge status and staleness indicators
---

# List Git Worktrees

List all worktrees with status information including merge status and activity.

## What This Command Does

1. Lists all worktrees in the repository
2. Shows merge status (merged to main/master or not)
3. Indicates staleness (no commits in 30+ days)
4. Shows last commit date for each branch

## Arguments

- `--verbose`: Show additional details (full paths, commit hashes)

## Output Format

```
Worktrees for <repo-name>:

| PATH | BRANCH | STATUS | LAST COMMIT |
|------|--------|--------|-------------|
| /path/to/project | main | (primary) | 2 days ago |
| /path/to/project-feature-auth | feature/auth | active | 1 day ago |
| /path/to/project-bugfix-123 | bugfix/123 | MERGED | 5 days ago |
| /path/to/project-old | feature/old | stale (45 days) | 45 days ago |
```

## Status Indicators

- **(primary)**: The main worktree
- **active**: Branch has recent commits, not merged
- **MERGED**: Branch is merged to main/master (candidate for cleanup)
- **stale (N days)**: No commits in 30+ days

## Workflow

```bash
# Get all worktrees
git worktree list --porcelain

# For each worktree, gather info
for worktree in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2-); do
    # Get branch name
    branch=$(git -C "$worktree" branch --show-current 2>/dev/null || echo "detached")

    # Check if merged to main
    if git branch --merged main 2>/dev/null | grep -q "^\s*${branch}$"; then
        status="MERGED"
    else
        status="active"
    fi

    # Get last commit date
    last_commit=$(git -C "$worktree" log -1 --format="%cr" 2>/dev/null || echo "unknown")

    # Check staleness (30+ days)
    days_ago=$(git -C "$worktree" log -1 --format="%ct" 2>/dev/null)
    now=$(date +%s)
    days=$((($now - $days_ago) / 86400))
    if [ $days -gt 30 ]; then
        status="stale ($days days)"
    fi
done
```

## Examples

```
/worktree-list
/worktree-list --verbose
```
