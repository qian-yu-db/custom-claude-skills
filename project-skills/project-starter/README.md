# Project Starter Skill

Bootstrap new projects with curated skills from [custom-claude-skills](https://github.com/qian-yu-db/custom-claude-skills) repository.

## Overview

The Project Starter skill enables Claude Code to:
- 🚀 Initialize new projects with proper structure
- 🎯 Select and integrate relevant skills from the custom-claude-skills repository
- 📝 Generate comprehensive documentation (PROJECT_PLAN.md, REQUIREMENTS.md)
- 🏗️ Create initial code scaffolding appropriate for selected skills
- ✅ Validate project setup and configuration

## Quick Start

### Installation

1. Clone this skill to your Claude skills directory:
```bash
cd ~/.claude/skills  # or your Claude skills directory
git clone <this-repo-url> project-starter
```

2. The skill will be automatically available in Claude Code

### Basic Usage

**Initialize a new project:**
```
User: "Create a new RAG agent project called doc-search"
```

Claude Code will:
- Create project structure
- Add relevant skills (e.g., langgraph-unstructured-tool-agent)
- Generate PROJECT_PLAN.md and REQUIREMENTS.md
- Create initial code scaffolding

**Add skills to existing project:**
```
User: "Add databricks-agent-deploy2app-skill to this project"
```

**Generate documentation:**
```
User: "Generate project documentation"
```

## What Gets Created

When you initialize a project, you get:

```
project-name/
├── .claude/
│   ├── skills-repo/          # Git submodule of custom-claude-skills
│   ├── skills/                # Symlinked skills
│   └── project-context.md     # Project metadata
├── docs/
│   ├── PROJECT_PLAN.md        # Comprehensive project plan
│   ├── REQUIREMENTS.md        # Technical requirements
│   ├── ARCHITECTURE.md        # System architecture
│   └── SETUP.md              # Setup instructions
├── src/                       # Source code
├── tests/                     # Tests
├── .python-version            # Python version (for uv)
├── pyproject.toml             # Project metadata & dependencies
├── uv.lock                    # Locked dependencies (uv managed)
├── .gitignore
└── README.md
```

**Environment Management**: Projects use **uv** for fast, reliable Python package management.

## Available Skills

The skill can integrate 13 specialized skills:

### Databricks Platform (4)
- **databricks-asset-bundle** - Generate DAB configurations with serverless compute, modular structure, and multiple input formats (text, Mermaid, images)
- **databricks-local-notebook** - Local notebook development with Databricks Connect
- **databricks-agent-deploy2app** - Deploy AI agents to Databricks Apps
- **databricks-agent-deploy-model-serving-dab** - Deploy agents to Model Serving with serverless compute

### LangGraph Agents (4)
- **langgraph-genie-agent** - Databricks Genie API integration
- **langgraph-unstructured-tool-agent** - RAG agents with Vector Search (4 patterns)
- **langgraph-multi-agent-supervisor** - Multi-agent orchestration
- **langgraph-mcp-tool-calling-agent** - MCP tool integration

### Python Development (2)
- **pytest-test-creator** - Auto-generate unit tests with coverage
- **python-code-formatter** - Code formatting (blackbricks + black + isort)

### Planning & Visualization (1)
- **mermaid-diagrams-creator** - Create Mermaid diagrams with automatic PNG/SVG/PDF generation

### General Purpose (2)
- **jira-epic-creator** - Generate Jira epics
- **battle-card-creator** - Competitive analysis

## Example Workflows

### Example 1: RAG Agent Project
```
User: "Create a new RAG agent project for searching internal docs"

Claude Code:
1. Creates project structure
2. Adds langgraph-unstructured-tool-agent skill
3. Generates documentation explaining RAG setup
4. Creates src/agent.py with starter code
5. Adds databricks-agent-deploy2app-skill for deployment
```

### Example 2: Databricks Development
```
User: "Create a Databricks project with local development"

Claude Code:
1. Creates notebooks/ directory
2. Adds databricks-local-notebook-skill
3. Adds databricks-asset-bundle-skill
4. Generates DAB configuration
5. Creates setup instructions for Databricks Connect
```

### Example 3: Multi-Agent System
```
User: "Create a multi-agent system with Genie and RAG"

Claude Code:
1. Creates multi-agent architecture
2. Adds langgraph-genie-agent + langgraph-unstructured-tool-agent
3. Adds langgraph-multi-agent-supervisor
4. Generates architecture diagram
5. Creates supervisor orchestration code
```

## Commands

### Initialize Project
```
"Create a new project called <name> for <purpose>"
"Bootstrap a new <type> project"
"Start a new project with <skill1>, <skill2>"
```

### Manage Skills
```
"Add <skill-name> to this project"
"Remove <skill-name> from this project"
"List available skills"
```

### Documentation
```
"Generate project documentation"
"Update PROJECT_PLAN.md"
"Create architecture diagram"
```

### Validation
```
"Validate project setup"
"Check project configuration"
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill instructions for Claude Code
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference and workflows
- **[templates/](templates/)** - Documentation templates
- **[scripts/](scripts/)** - Automation scripts

## Skill Selection Logic

Claude Code automatically recommends skills based on project type:

| Project Type | Recommended Skills |
|--------------|-------------------|
| RAG Agent | langgraph-unstructured-tool-agent, databricks-agent-deploy2app, mermaid-diagrams-creator |
| Multi-Agent | langgraph-genie-agent, langgraph-multi-agent-supervisor, mermaid-diagrams-creator |
| Databricks Workflow | mermaid-diagrams-creator, databricks-asset-bundle, databricks-local-notebook |
| Data Pipeline | databricks-asset-bundle, databricks-local-notebook, mermaid-diagrams-creator |
| Documentation | mermaid-diagrams-creator, battle-card-creator, jira-epic-creator |
| Architecture | mermaid-diagrams-creator, databricks-asset-bundle |

## Requirements

- **Claude Code** - For executing the skill
- **Git** - For submodule management
- **Python 3.11+** - For generated projects
- **uv** - For Python package management ([install guide](https://github.com/astral-sh/uv))
- **custom-claude-skills** - Auto-added as submodule

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip (if you have Python already)
pip install uv
```

## Best Practices

1. **Start Minimal** - Begin with essential skills, add more as needed
2. **Use uv** - Always use `uv` for package management (10-100x faster than pip)
3. **Commit Lock Files** - Commit `pyproject.toml` and `uv.lock` for reproducibility
4. **Read Skill Docs** - Each skill has detailed documentation
5. **Keep Docs Updated** - Regenerate after major changes
6. **Version Control** - Commit skill submodule references
7. **Use Claude Code** - Leverage integrated skills for development

### Common uv Commands

```bash
# Sync dependencies (after cloning)
uv sync

# Add a package
uv add package-name

# Add a dev dependency
uv add --dev pytest

# Run a command in the project environment
uv run python src/main.py

# Update dependencies
uv lock --upgrade && uv sync
```

## Git Submodules Workflow

Projects created with project-starter use **git submodules** to include the custom-claude-skills repository. This ensures skill source code travels with your project.

### When Creating a Project

The bootstrap script automatically:
1. Adds custom-claude-skills as a submodule in `.claude/skills-repo/`
2. Creates `.gitmodules` file tracking the submodule
3. Creates symlinks in `.claude/skills/` pointing to selected skills

```bash
# After running bootstrap_project.py, commit your project:
cd my-new-project
git add .
git commit -m "Initial project setup with skills"
git remote add origin https://github.com/user/my-new-project.git
git push -u origin main
```

### When Cloning a Project

**Always use `--recurse-submodules`:**
```bash
git clone --recurse-submodules https://github.com/user/my-project.git
```

This ensures you get:
- The project code
- The complete custom-claude-skills repository in `.claude/skills-repo/`
- All skill symlinks working correctly

**If you forgot `--recurse-submodules`:**
```bash
cd my-project
git submodule update --init --recursive
```

### Benefits of Using Submodules

1. **Reproducibility** - Skills pinned to specific commit SHA
2. **Portability** - No manual skill installation needed
3. **Version Control** - Track which skill versions your project uses
4. **Self-Contained** - Project includes all dependencies (code + skills)
5. **Easy Collaboration** - Team members get correct skill versions automatically

### Submodule Structure

```
my-project/
├── .gitmodules                     # Tracks submodule (committed)
├── .claude/
│   ├── skills-repo/                # Git submodule (auto-cloned)
│   │   ├── databricks_platform_skills/
│   │   ├── langgraph_skills/
│   │   ├── python_sklls/
│   │   └── ... (15 skills)
│   └── skills/                     # Symlinks (committed)
│       ├── langgraph-genie-agent -> ../skills-repo/langgraph_skills/langgraph-genie-agent
│       └── databricks-asset-bundle -> ../skills-repo/databricks_platform_skills/databricks-asset-bundle
```

## Troubleshooting

### Submodule Issues

**Problem**: `.claude/skills-repo/` is empty after cloning
```bash
# Solution: Initialize submodules
git submodule update --init --recursive
```

**Problem**: Submodule shows as "modified" in git status
```bash
# Solution: Update to project's expected commit
git submodule update .claude/skills-repo

# Or update to latest remote commit
git submodule update --remote .claude/skills-repo
```

**Problem**: Skills not working after cloning
```bash
# Solution: Reinitialize submodules and verify symlinks
git submodule update --init --recursive
ls -la .claude/skills/  # Verify symlinks point to skills-repo/
```

### Symlink Issues (Windows)
Enable Developer Mode or use directory junctions:
```bash
mklink /D .claude\skills\skill-name .claude\skills-repo\path\to\skill
```

### Skill Conflicts
Review each skill's SKILL.md for dependencies and create isolated virtual environments if needed.

## Contributing

To add new skills to the catalog:
1. Update the Skill Catalog section in SKILL.md
2. Update skill selection logic for new project types
3. Add example workflows
4. Update this README

## Version

**v1.2.1** - December 2025

**Changelog:**
- v1.2.1: Enhanced git submodule documentation and workflow (ensures skills travel with projects)
- v1.2.0: Use uv for Python environment management instead of pip/venv
- v1.1.0: Added mermaid-diagrams-creator skill, updated databricks-asset-bundle with new features
- v1.0.0: Initial release with 12 skills

## License

Apache-2.0

## Support

- **Skill Issues**: Check individual skill documentation in custom-claude-skills repo
- **Project Starter Issues**: Create an issue in this repository
- **Claude Code**: Visit https://docs.claude.com/en/docs/claude-code

---

**Related Resources:**
- [custom-claude-skills Repository](https://github.com/qian-yu-db/custom-claude-skills)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
