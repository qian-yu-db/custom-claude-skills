---
allowed-tools: Bash(git worktree:*), Bash(git branch:*), Bash(git symbolic-ref:*), Bash(git -C:*)
description: Remove git worktrees for branches that have been merged
---

# Clean Git Worktrees

Remove worktrees for branches that have been merged to main/master.

## What This Command Does

1. Finds worktrees where the branch is merged to main/master
2. Shows list and asks for confirmation
3. Removes each merged worktree
4. Prunes stale git references

## Arguments

- `--dry-run`: Show what would be removed without removing
- `--include-stale`: Also remove worktrees with no commits in 30+ days
- `--force`: Skip confirmation prompt

## Workflow

```bash
# Find merged worktrees
merged_worktrees=()
main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

for wt_line in $(git worktree list --porcelain | grep "^worktree"); do
    wt_path=$(echo "$wt_line" | cut -d' ' -f2-)
    branch=$(git -C "$wt_path" branch --show-current 2>/dev/null)

    # Skip if it's the main branch
    if [ "$branch" = "$main_branch" ]; then
        continue
    fi

    # Check if merged
    if git branch --merged "$main_branch" 2>/dev/null | grep -q "^\s*${branch}$"; then
        merged_worktrees+=("$wt_path:$branch")
    fi
done

# If --include-stale, also find stale worktrees
if [ "$INCLUDE_STALE" = true ]; then
    # Add stale worktrees (30+ days without commits)
fi

# Show what will be removed
echo "The following worktrees will be removed:"
for wt in "${merged_worktrees[@]}"; do
    echo "  - $wt"
done

# If --dry-run, stop here
if [ "$DRY_RUN" = true ]; then
    echo "(dry run - no changes made)"
    exit 0
fi

# Confirm unless --force
if [ "$FORCE" != true ]; then
    # Ask user for confirmation
fi

# Remove each worktree
for wt in "${merged_worktrees[@]}"; do
    wt_path=$(echo "$wt" | cut -d':' -f1)
    echo "Removing: $wt_path"
    git worktree remove "$wt_path"
done

# Prune stale references
git worktree prune
echo "Cleanup complete!"
```

## Output Example

```
The following worktrees will be removed:

| PATH | BRANCH | REASON |
|------|--------|--------|
| ../project-feature-auth | feature/auth | merged to main |
| ../project-bugfix-42 | bugfix/42 | merged to main |
| ../project-old-experiment | experiment/old | stale (60 days) |

Proceed with removal? [y/N]
```

## Examples

```
/worktree-clean                    # Remove merged, with confirmation
/worktree-clean --dry-run          # Preview what would be removed
/worktree-clean --include-stale    # Also remove stale worktrees
/worktree-clean --force            # Remove without confirmation
```

## Safety

- Never removes the primary worktree
- Never removes worktrees for unmerged branches (unless --include-stale)
- Always confirms before removal (unless --force)
- Runs `git worktree prune` to clean up references
