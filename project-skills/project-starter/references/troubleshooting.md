# Project Starter Troubleshooting

## uv Not Installed

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Submodule Issues

### Skills repository not found after cloning
**Cause**: Cloned without `--recurse-submodules`.
```bash
git submodule update --init --recursive
```

### `.claude/skills-repo/` is empty
**Cause**: Submodule not initialized.
```bash
cd <project-root>
git submodule update --init --recursive
```

### Submodule shows as "modified" in git status
**Cause**: Submodule pointing to different commit.
```bash
# Update to project's recorded commit
git submodule update .claude/skills-repo
# Or update to latest remote
git submodule update --remote .claude/skills-repo
```

### Best practice for cloning
```bash
git clone --recurse-submodules https://github.com/user/project.git
```

## Symlink Issues (Windows)

Enable Developer Mode or use directory junctions:
```bash
mklink /D .claude\skills\skill-name .claude\skills-repo\path\to\skill
```

## Skill Conflicts

If skills have conflicting requirements:
1. Review each skill's SKILL.md for dependencies
2. Use `uv add package==version` to pin compatible versions
3. Check `uv.lock` for resolved dependencies

## Python Version Issues

```bash
echo "3.11" > .python-version
uv python install 3.11
uv sync
```
