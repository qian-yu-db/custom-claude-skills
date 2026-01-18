# Project Starter - Quick Reference

## Quick Commands

### Initialize New Project
```
User: "Create a new project called <name> for <purpose>"
User: "Bootstrap a new <type> project"
User: "Start a new project with <skill1>, <skill2>"
```

**Claude Code will:**
- Create project structure
- Add selected skills as submodules
- Generate documentation
- Create initial scaffolding

---

### Add Skills to Project
```
User: "Add <skill-name> to this project"
User: "Include the <skill-name> skill"
```

**Claude Code will:**
- Link skill to .claude/skills/
- Update project-context.md
- Update requirements.txt
- Suggest integration points

---

### Generate/Update Documentation
```
User: "Generate project documentation"
User: "Update the PROJECT_PLAN.md"
User: "Refresh requirements documentation"
```

**Claude Code will:**
- Read all skill documentation
- Analyze code structure
- Update/create docs/PROJECT_PLAN.md
- Update/create docs/REQUIREMENTS.md

---

### Validate Project
```
User: "Validate project setup"
User: "Check if everything is configured correctly"
```

**Claude Code will:**
- Verify directory structure
- Check git submodules
- Validate skill symlinks
- Check dependencies

---

### Create Cross-Platform Project
```
User: "Create a new project with cross-platform support"
User: "Bootstrap project for Claude Code, Codex, and Gemini"
```

**Script usage:**
```bash
python scripts/bootstrap_project.py my-agent \
  langgraph_skills/langgraph-genie-agent \
  --cross-platform
```

**Claude Code will:**
- Create standard project structure
- Merge selected skills into `instructions.md`
- Generate `CLAUDE.md` (Claude Code)
- Generate `AGENTS.md` (Codex CLI)
- Generate `GEMINI.md` (Gemini CLI)
- Create `scripts/sync_instructions.sh`

---

### Sync Cross-Platform Files
```bash
# After editing instructions.md
./scripts/sync_instructions.sh

# Or manually
python .claude/skills-repo/develop_planning_skills/cross-platform-skill/scripts/convert_skill.py \
  instructions.md --output-dir ./
```

---

## Skill Selection Guide

### By Project Type

#### RAG/Agent Projects
**Skills**: `langgraph-unstructured-tool-agent`, `databricks-agent-deploy2app`, `mermaid-diagrams-creator`, `pytest-test-creator`

**Use when**: Building agents that need to query documents or databases

---

#### Multi-Agent Systems
**Skills**: `langgraph-genie-agent`, `langgraph-unstructured-tool-agent`, `langgraph-multi-agent-supervisor`, `mermaid-diagrams-creator`

**Use when**: Building complex systems with multiple specialized agents

---

#### Databricks Workflow Development
**Skills**: `mermaid-diagrams-creator`, `databricks-asset-bundle`, `databricks-local-notebook`, `python-code-formatter`

**Use when**: Designing and implementing Databricks workflows visually

---

#### Databricks Data Pipelines
**Skills**: `databricks-asset-bundle`, `databricks-local-notebook`, `mermaid-diagrams-creator`, `pytest-test-creator`

**Use when**: Building data pipelines with serverless compute

---

#### Documentation/Analysis
**Skills**: `mermaid-diagrams-creator`, `battle-card-creator`, `jira-epic-creator`

**Use when**: Creating diagrams, competitive analysis, or project documentation

---

#### Architecture & Planning
**Skills**: `mermaid-diagrams-creator`, `databricks-asset-bundle`

**Use when**: Designing system architecture and generating deployable workflows from diagrams

---

## Project Structure Reference

```
project-name/
├── .claude/
│   ├── skills-repo/          # Git submodule
│   ├── skills/                # Symlinked skills
│   └── project-context.md     # Project metadata
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   └── SETUP.md
├── src/                       # Application code
├── tests/                     # Test files
├── notebooks/                 # Databricks notebooks
├── configs/                   # Configuration files
├── .python-version            # Python version (uv)
├── pyproject.toml             # Dependencies & metadata (uv)
├── uv.lock                    # Locked dependencies (uv)
├── .gitignore
└── README.md
```

**Note**: Uses **uv** for Python package management (not pip/venv).

---

## Common Workflows

### Workflow 1: Create RAG Agent Project
```bash
1. "Create a new RAG agent project called doc-search"
2. Claude Code creates structure with langgraph skills
3. "Generate the project documentation"
4. Review docs/PROJECT_PLAN.md
5. Start development with Claude Code
```

### Workflow 2: Add Deployment Capability
```bash
1. "Add databricks-agent-deploy2app-skill to this project"
2. Claude Code links skill and updates docs
3. "How do I deploy this agent?"
4. Claude Code references deployment skill instructions
```

### Workflow 3: Databricks Full Stack
```bash
1. "Create a Databricks project with notebooks and deployment"
2. Select: databricks-local-notebook, databricks-asset-bundle
3. "Generate initial notebooks"
4. Develop locally with Databricks Connect
5. "Create DAB configuration"
6. Deploy using asset bundles
```

### Workflow 4: Visual Workflow to DAB
```bash
1. "Create a data pipeline project from a workflow diagram"
2. Select: mermaid-diagrams-creator, databricks-asset-bundle
3. Draw workflow in Mermaid or upload image
4. Claude generates .mermaid file and visualizations
5. Claude generates DAB configuration from Mermaid diagram
6. Review generated serverless workflow
7. Deploy to Databricks
```

### Workflow 5: Architecture Documentation
```bash
1. "Create a project for documenting system architecture"
2. Select: mermaid-diagrams-creator, battle-card-creator
3. "Generate architecture diagrams for our multi-agent system"
4. Claude creates flowcharts, sequence diagrams, and component diagrams
5. "Export diagrams as PNG and SVG"
6. Claude generates image files automatically
7. Use in documentation and presentations
```

### Workflow 6: Cross-Platform Agent Project
```bash
1. "Create a new RAG agent with cross-platform support"
2. Select skills: langgraph-unstructured-tool-agent
3. Claude merges skills into instructions.md
4. Claude generates CLAUDE.md, AGENTS.md, GEMINI.md
5. Edit instructions.md as canonical source
6. Run ./scripts/sync_instructions.sh to regenerate
7. Project works with Claude Code, Codex CLI, and Gemini CLI
```

---

## Available Skills Quick List

### Databricks (4 skills)
- `databricks-asset-bundle` - DAB generation (serverless, modular, Mermaid support)
- `databricks-local-notebook` - Local notebook dev
- `databricks-agent-deploy2app` - Deploy to Apps
- `databricks-agent-deploy-model-serving-dab` - Deploy to Model Serving

### LangGraph (4 skills)
- `langgraph-genie-agent` - Genie API integration
- `langgraph-unstructured-tool-agent` - RAG agents (4 patterns)
- `langgraph-multi-agent-supervisor` - Multi-agent orchestration
- `langgraph-mcp-tool-calling-agent` - MCP tool integration

### Python (2 skills)
- `pytest-test-creator` - Auto-generate tests
- `python-code-formatter` - Code formatting

### Planning & Visualization (2 skills)
- `mermaid-diagrams-creator` - Create diagrams with PNG/SVG/PDF generation
- `cross-platform-skill` - Convert skills for Codex CLI and Gemini CLI

### General (2 skills)
- `jira-epic-creator` - Jira epic generation
- `battle-card-creator` - Competitive analysis

---

## uv Commands Reference

### Install & Sync
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv and installs packages)
uv sync

# Sync after pulling changes
git pull && uv sync
```

### Add Packages
```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev pytest

# Add specific version
uv add package-name==1.2.3
```

### Run Commands
```bash
# Run Python script in project environment
uv run python src/main.py

# Run pytest
uv run pytest

# Run any command in project environment
uv run <command>
```

### Update Dependencies
```bash
# Update all dependencies
uv lock --upgrade
uv sync

# Update specific package
uv add package-name --upgrade
```

### Python Version Management
```bash
# Set Python version
echo "3.11" > .python-version

# Install Python version with uv
uv python install 3.11

# Use specific Python version
uv init --python 3.11
```

---

## Troubleshooting

### uv not installed
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Submodule not initialized
```bash
git submodule update --init --recursive
```

### Symlink broken
```bash
# Remove and recreate
rm .claude/skills/skill-name
ln -s ../.claude/skills-repo/path/to/skill .claude/skills/skill-name
```

### Windows symlink issues
```bash
# Enable Developer Mode in Windows Settings, or:
mklink /D .claude\skills\skill-name .claude\skills-repo\path\to\skill
```

### Skill conflicts
1. Check each skill's requirements
2. Use `uv add package==version` to specify versions
3. Check `uv.lock` for resolved dependencies
4. Document in REQUIREMENTS.md

### Dependencies out of sync
```bash
# After pulling changes
uv sync

# If still issues, reset environment
rm -rf .venv uv.lock
uv sync
```

---

## Tips

- **Use uv**: 10-100x faster than pip for package installation
- **Commit lock files**: Always commit `pyproject.toml` and `uv.lock`
- **Start minimal**: Add skills as you need them
- **Read skill docs**: Each skill has detailed SKILL.md
- **Keep docs updated**: Regenerate after major changes
- **Use Claude Code**: Leverage skills for development tasks
- **Version control**: Commit submodule references

---

## Getting Help

- **Skill documentation**: `.claude/skills/<skill-name>/SKILL.md`
- **Project context**: `.claude/project-context.md`
- **Requirements**: `docs/REQUIREMENTS.md`
- **Setup guide**: `docs/SETUP.md`

---

## Cross-Platform Reference

### File Mapping

| Platform | Instruction File | Slash Commands | MCP Config |
|----------|-----------------|----------------|------------|
| Claude Code | `CLAUDE.md` | `.claude/commands/` | `.mcp.json` |
| Codex CLI | `AGENTS.md` | `.codex/prompts/` | `~/.codex/config.toml` |
| Gemini CLI | `GEMINI.md` | `.gemini/commands/` | `.gemini/settings.json` |

### Sync Workflow

```bash
# 1. Edit canonical source
vim instructions.md

# 2. Regenerate platform files
./scripts/sync_instructions.sh

# 3. Commit all files
git add instructions.md CLAUDE.md AGENTS.md GEMINI.md
git commit -m "Update instructions"
```

---

## Version
**v1.3.0** - December 2025

**Updates:**
- v1.3.0: Added cross-platform support (`--cross-platform` flag)
- v1.2.0: Use uv for Python environment management
- v1.1.0: Added mermaid-diagrams-creator skill, updated databricks-asset-bundle
- v1.0.0: Initial release
