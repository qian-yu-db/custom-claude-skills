---
allowed-tools: Bash(git worktree:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(uv sync:*), Bash(npm install:*), Bash(yarn install:*), Bash(pnpm install:*), Bash(cp:*), Bash(cd:*), Bash(ls:*)
description: Create a new git worktree with auto-setup (dependencies, env files)
---

# Create Git Worktree

Create a new worktree for the specified branch with automatic setup.

## What This Command Does

1. Creates worktree in sibling directory: `../<repo-name>-<branch-sanitized>`
2. Detects package manager and installs dependencies
3. Copies env files (.env, .env.local) from main worktree

## Arguments

- `<branch>`: The branch name (required)
- `--no-setup`: Skip dependency installation
- `--path <path>`: Use custom path instead of default

## Workflow

```bash
# 1. Get repo name and sanitize branch
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
BRANCH_SAFE=$(echo "$BRANCH" | tr '/' '-' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')

# 2. Check if branch exists, create if needed
if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    # Ask user if they want to create the branch
fi

# 3. Create worktree
git worktree add "../${REPO_NAME}-${BRANCH_SAFE}" "$BRANCH"

# 4. Install dependencies (unless --no-setup)
cd "../${REPO_NAME}-${BRANCH_SAFE}"
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

# 5. Copy env files
for envfile in .env .env.local .env.development; do
    if [ -f "../${REPO_NAME}/${envfile}" ]; then
        cp "../${REPO_NAME}/${envfile}" .
    fi
done
```

## Package Manager Detection

| Lock File | Command |
|-----------|---------|
| uv.lock / pyproject.toml | `uv sync` |
| package-lock.json | `npm install` |
| yarn.lock | `yarn install` |
| pnpm-lock.yaml | `pnpm install` |
| requirements.txt | `uv pip install -r requirements.txt` |
| Gemfile.lock | `bundle install` |
| go.mod | `go mod download` |

## Path Naming

Branches are sanitized for filesystem safety:
- `feature/auth` → `project-feature-auth`
- `bugfix/123` → `project-bugfix-123`
- `Feature Branch` → `project-feature-branch`

## Examples

```
/worktree-add main
/worktree-add feature/new-auth
/worktree-add hotfix/critical --no-setup
/worktree-add experiment --path ~/experiments/my-test
```

## Error Handling

- If branch doesn't exist: Ask user if they want to create it
- If branch already checked out: Show which worktree has it
- If path exists: Warn and ask for confirmation
