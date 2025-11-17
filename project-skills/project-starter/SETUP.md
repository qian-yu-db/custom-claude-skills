# Project Starter Skill - Setup Guide

Complete installation and configuration guide for the Project Starter skill.

---

## Prerequisites

Before installing the Project Starter skill, ensure you have:

- ✅ **Claude Code** installed and working
- ✅ **Git** (version 2.13 or higher for submodule support)
- ✅ **Python 3.8+** (for generated projects)
- ✅ Terminal/command line access

### Verify Prerequisites

```bash
# Check Claude Code
claude-code --version

# Check Git
git --version

# Check Python
python --version
```

---

## Installation

### Method 1: Direct Clone (Recommended)

1. **Clone to Claude skills directory:**

```bash
# Navigate to Claude skills directory
cd ~/.claude/skills  # macOS/Linux
# or
cd %USERPROFILE%\.claude\skills  # Windows

# Clone the skill
git clone https://github.com/your-username/project-starter.git
```

2. **Verify installation:**

```bash
ls -la project-starter/
# Should see: SKILL.md, QUICK_REFERENCE.md, README.md, templates/, scripts/, examples/
```

3. **Test the skill:**

Start Claude Code and ask:
```
"Use the project-starter skill to create a new project"
```

---

### Method 2: Manual Installation

1. **Download the skill:**
   - Download ZIP from GitHub
   - Extract to a temporary location

2. **Copy to skills directory:**

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skill
cp -r /path/to/extracted/project-starter ~/.claude/skills/
```

3. **Verify installation** (same as Method 1, step 2)

---

## Skill Configuration

### Optional: Customize Skill Catalog

If you want to add custom skills or modify available skills:

1. **Edit SKILL.md:**

```bash
cd ~/.claude/skills/project-starter
nano SKILL.md  # or use your preferred editor
```

2. **Update the Skill Catalog section:**

```markdown
## Skill Catalog

### Your Custom Category
1. **your-custom-skill** - Description of your skill
```

3. **Update the bootstrap script:**

Edit `scripts/bootstrap_project.py` and add your skill to `AVAILABLE_SKILLS`:

```python
AVAILABLE_SKILLS = {
    # ... existing skills ...
    "your_category/your-custom-skill": "Your skill description",
}
```

---

## Using the Skill

### Quick Start

1. **Start Claude Code:**

```bash
claude-code chat
```

2. **Initialize a new project:**

```
Create a new project called "my-agent" for building a RAG agent
```

3. **Claude Code will:**
   - Read the project-starter skill
   - Suggest relevant skills
   - Create project structure
   - Generate documentation
   - Provide next steps

---

### Using the Bootstrap Script Directly

You can also use the bootstrap script directly without Claude Code:

```bash
# Navigate to where you want to create the project
cd ~/projects

# Run bootstrap script
python ~/.claude/skills/project-starter/scripts/bootstrap_project.py \
  my-new-project \
  langgraph_skills/langgraph-unstructured-tool-agent \
  databricks_platform_skills/databricks-agent-deploy2app-skill
```

**Parameters:**
- First argument: Project name
- Remaining arguments: Skill paths from custom-claude-skills repo

---

## Project Workflow

### 1. Initialize Project

```
User: "Create a new RAG agent project called doc-search"
```

### 2. Review Generated Structure

```bash
cd doc-search
tree -L 2
```

You'll see:
```
doc-search/
├── .claude/
│   ├── skills-repo/
│   ├── skills/
│   ├── project-context.md
│   └── init-prompt.md
├── docs/
├── src/
├── tests/
└── README.md
```

### 3. Generate Documentation

```
User: "Use the initialization prompt to generate project documentation"
```

Claude Code will read `.claude/init-prompt.md` and generate:
- `docs/PROJECT_PLAN.md`
- `docs/REQUIREMENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/SETUP.md`

### 4. Start Development

```bash
# Setup environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start coding with Claude Code
claude-code chat
```

---

## Skill Updates

### Update Project Starter Skill

```bash
cd ~/.claude/skills/project-starter
git pull origin main
```

### Update Custom-Claude-Skills in Projects

For existing projects that use skills submodule:

```bash
cd your-project
git submodule update --remote
```

---

## Troubleshooting

### Issue: Skill Not Found

**Symptom:** Claude Code doesn't recognize the project-starter skill

**Solution:**
```bash
# Verify skill location
ls ~/.claude/skills/project-starter/SKILL.md

# If file exists but skill not working, restart Claude Code
```

---

### Issue: Submodule Not Initialized

**Symptom:** `.claude/skills-repo` is empty

**Solution:**
```bash
cd your-project
git submodule update --init --recursive
```

---

### Issue: Symlink Creation Failed (Windows)

**Symptom:** "You do not have sufficient privilege" error

**Solution 1 - Enable Developer Mode:**
1. Open Windows Settings
2. Go to "Update & Security" > "For developers"
3. Enable "Developer Mode"
4. Retry project creation

**Solution 2 - Use Directory Junctions:**
```bash
# Instead of symlinks, use junctions
mklink /D .claude\skills\skill-name .claude\skills-repo\path\to\skill
```

---

### Issue: Import Errors in Generated Projects

**Symptom:** `ModuleNotFoundError` when running code

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify Python path
python -c "import sys; print(sys.path)"

# Check virtual environment
which python  # Should point to venv
```

---

### Issue: Git Submodule Conflicts

**Symptom:** Git reports submodule conflicts

**Solution:**
```bash
# Reset submodule
git submodule deinit -f .claude/skills-repo
git submodule update --init --recursive

# Or start fresh
rm -rf .claude/skills-repo
git submodule add https://github.com/qian-yu-db/custom-claude-skills .claude/skills-repo
```

---

## Advanced Configuration

### Custom Templates

You can customize the documentation templates:

1. **Copy templates:**
```bash
cp ~/.claude/skills/project-starter/templates/PROJECT_PLAN_template.md \
   ~/.claude/skills/project-starter/templates/PROJECT_PLAN_custom.md
```

2. **Modify the custom template**

3. **Update SKILL.md** to reference your custom template

---

### Custom Bootstrap Script

Create your own wrapper around the bootstrap script:

```bash
#!/bin/bash
# my-bootstrap.sh - Custom project bootstrap

PROJECT_NAME=$1
PROJECT_TYPE=$2

case $PROJECT_TYPE in
  "rag")
    SKILLS="langgraph_skills/langgraph-unstructured-tool-agent \
            databricks_platform_skills/databricks-agent-deploy2app-skill"
    ;;
  "multi-agent")
    SKILLS="langgraph_skills/langgraph-genie-agent \
            langgraph_skills/langgraph-multi-agent-supervisor"
    ;;
  *)
    echo "Unknown project type: $PROJECT_TYPE"
    exit 1
    ;;
esac

python ~/.claude/skills/project-starter/scripts/bootstrap_project.py \
  $PROJECT_NAME $SKILLS
```

**Usage:**
```bash
./my-bootstrap.sh my-rag-agent rag
```

---

## Integration with IDEs

### VS Code

1. **Install Claude extension** (if available)

2. **Configure workspace:**

Add to `.vscode/settings.json`:
```json
{
  "files.associations": {
    "*.md": "markdown"
  },
  "python.analysis.extraPaths": [
    "${workspaceFolder}/.claude/skills"
  ]
}
```

3. **Use integrated terminal:**
```bash
# From VS Code terminal
claude-code chat
```

---

### PyCharm

1. **Mark directories:**
   - Right-click `.claude/skills` → Mark Directory as → Sources Root

2. **Configure external tools:**
   - Settings → Tools → External Tools
   - Add new tool: Claude Code
   - Program: `claude-code`
   - Arguments: `chat`

---

## Best Practices

### Do's ✅

- ✅ **Start simple** - Begin with minimal skills, add more as needed
- ✅ **Read skill docs** - Each skill has detailed SKILL.md
- ✅ **Keep docs updated** - Regenerate after major changes
- ✅ **Commit regularly** - Include submodule commits
- ✅ **Use Claude Code** - Leverage integrated skills for development

### Don'ts ❌

- ❌ **Don't modify submodule** - Changes in `.claude/skills-repo` will be lost
- ❌ **Don't skip initialization prompt** - It's essential for good documentation
- ❌ **Don't ignore symlink issues** - Fix them before proceeding
- ❌ **Don't mix skill versions** - Keep submodule consistent across team

---

## Getting Help

### Documentation
- **Skill Documentation**: `~/.claude/skills/project-starter/SKILL.md`
- **Quick Reference**: `~/.claude/skills/project-starter/QUICK_REFERENCE.md`
- **Examples**: `~/.claude/skills/project-starter/examples/USAGE_EXAMPLES.md`

### Community
- **custom-claude-skills repo**: https://github.com/qian-yu-db/custom-claude-skills
- **Claude Code docs**: https://docs.claude.com/en/docs/claude-code

### Debugging

Enable verbose output:
```bash
# Run bootstrap with debugging
python -v ~/.claude/skills/project-starter/scripts/bootstrap_project.py my-project
```

Check Claude Code logs:
```bash
# Location varies by platform
~/.claude/logs/  # Check your Claude Code installation
```

---

## Uninstallation

To remove the project-starter skill:

```bash
# Remove skill directory
rm -rf ~/.claude/skills/project-starter

# Existing projects will continue to work
# The skill is only needed for creating new projects
```

To remove from existing projects:
```bash
# Remove submodule (optional)
git submodule deinit -f .claude/skills-repo
git rm -f .claude/skills-repo
rm -rf .git/modules/.claude/skills-repo
```

---

## Version Information

**Current Version**: 1.0.0  
**Last Updated**: November 2025  
**Compatible With**: 
- Claude Code (latest)
- custom-claude-skills v1.x
- Git 2.13+
- Python 3.8+

---

## Changelog

### v1.0.0 - November 2025
- Initial release
- 12 skills from custom-claude-skills supported
- Bootstrap script for project initialization
- Documentation templates
- Examples and usage guide

---

For more information, see the [README.md](README.md) or [SKILL.md](SKILL.md).
