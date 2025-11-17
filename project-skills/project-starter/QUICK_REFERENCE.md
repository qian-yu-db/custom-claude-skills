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

## Skill Selection Guide

### By Project Type

#### RAG/Agent Projects
**Skills**: `langgraph-unstructured-tool-agent`, `databricks-agent-deploy2app-skill`, `pytest-test-creator`

**Use when**: Building agents that need to query documents or databases

---

#### Multi-Agent Systems
**Skills**: `langgraph-genie-agent`, `langgraph-unstructured-tool-agent`, `langgraph-multi-agent-supervisor`

**Use when**: Building complex systems with multiple specialized agents

---

#### Databricks Development
**Skills**: `databricks-local-notebook-skill`, `databricks-asset-bundle-skill`, `python-code-formatter`

**Use when**: Developing Databricks notebooks and workflows

---

#### Documentation/Analysis
**Skills**: `battle-card-creator-skill`, `jira-epic-creator-skill`

**Use when**: Creating competitive analysis or project documentation

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
├── .gitignore
├── README.md
└── requirements.txt
```

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
2. Select: databricks-local-notebook-skill, databricks-asset-bundle-skill
3. "Generate initial notebooks"
4. Develop locally with Databricks Connect
5. "Create DAB configuration"
6. Deploy using asset bundles
```

---

## Available Skills Quick List

### Databricks (4 skills)
- `databricks-asset-bundle-skill` - DAB generation
- `databricks-local-notebook-skill` - Local notebook dev
- `databricks-agent-deploy2app-skill` - Deploy to Apps
- `databricks-agent-deploy-model-serving-dab` - Deploy to Model Serving

### LangGraph (4 skills)
- `langgraph-genie-agent` - Genie API integration
- `langgraph-unstructured-tool-agent` - RAG agents
- `langgraph-multi-agent-supervisor` - Multi-agent orchestration
- `langgraph-mcp-tool-calling-agent` - MCP tool integration

### Python (2 skills)
- `pytest-test-creator` - Auto-generate tests
- `python-code-formatter` - Code formatting

### General (2 skills)
- `jira-epic-creator-skill` - Jira epic generation
- `battle-card-creator-skill` - Competitive analysis

---

## Troubleshooting

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
2. Create isolated virtual environment
3. Document in REQUIREMENTS.md

---

## Tips

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

## Version
**v1.0.0** - November 2025
