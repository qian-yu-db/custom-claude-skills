---
name: project-starter
description: Bootstrap new projects by selecting and integrating skills from custom-claude-skills repository with proper structure, uv environment management, and comprehensive documentation. Use when initializing projects, setting up project scaffolding, integrating multiple skills, or generating project documentation (PROJECT_PLAN, REQUIREMENTS, ARCHITECTURE).
---

# Project Starter Skill

Bootstrap new projects by selecting and integrating skills from the custom-claude-skills repository, setting up proper project structure, and generating comprehensive documentation.

## Repository Reference
- **Skills Repository**: https://github.com/qian-yu-db/custom-claude-skills

## Skill Catalog

### Databricks Platform (4)
1. **databricks-asset-bundle** - DAB configs with serverless compute and multiple input formats
2. **databricks-local-notebook** - Notebooks with local IDE development via Databricks Connect
3. **databricks-agent-deploy2app** - Deploy AI agents to Databricks Apps
4. **databricks-agent-deploy-model-serving-dab** - Deploy agents to Model Serving using DABs

### LangGraph (4)
1. **langgraph-genie-agent** - Agents with Databricks Genie API
2. **langgraph-unstructured-tool-agent** - RAG agents with Vector Search
3. **langgraph-multi-agent-supervisor** - Multi-agent systems with supervisor orchestration
4. **langgraph-mcp-tool-calling-agent** - Agents with MCP tools

### Python (2)
1. **pytest-test-creator** - Auto-generate unit tests with coverage
2. **python-code-formatter** - Format code (blackbricks for Databricks, black+isort for regular)

### Planning & Visualization (1)
1. **mermaid-diagrams-creator** - Mermaid diagrams with automatic PNG/SVG/PDF generation

### General (2)
1. **jira-epic-creator** - Transform documents into structured Jira epics
2. **battle-card-creator** - Competitive battle card creation

## Project Structure

```
project-name/
├── .claude/
│   ├── skills-repo/          # Git submodule of custom-claude-skills
│   ├── skills/                # Symlinks to selected skills
│   └── project-context.md     # Generated context for this project
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── REQUIREMENTS.md
│   └── ARCHITECTURE.md        # If applicable
├── src/
├── tests/
├── notebooks/                 # If using Databricks skills
├── configs/
├── .python-version
├── pyproject.toml             # uv managed
├── uv.lock
├── .gitignore
└── README.md
```

## Initialization Workflow

### Step 1: Understand Requirements

Gather: project name, primary goal, skills needed, tech stack preferences.

### Step 2: Select Skills

Recommend skill combinations based on project type:

| Project Type | Recommended Skills |
|---|---|
| RAG/Agent | langgraph-unstructured-tool-agent, databricks-agent-deploy2app, pytest-test-creator, mermaid-diagrams-creator |
| Multi-Agent | langgraph-genie-agent, langgraph-multi-agent-supervisor, databricks-agent-deploy-model-serving-dab, mermaid-diagrams-creator |
| Databricks Workflows | mermaid-diagrams-creator, databricks-asset-bundle, databricks-local-notebook, python-code-formatter |
| Documentation/Analysis | mermaid-diagrams-creator, battle-card-creator, jira-epic-creator |

### Step 3: Create Project Structure

1. Create directories per structure above
2. Initialize git repository
3. Initialize Python project: `uv init --name project-name --python 3.11`
4. Add skills repository as submodule:
   ```bash
   git submodule add https://github.com/qian-yu-db/custom-claude-skills .claude/skills-repo
   git submodule update --init --recursive
   ```
5. Create symlinks for selected skills:
   ```bash
   ln -s ../.claude/skills-repo/[skill-path] .claude/skills/[skill-name]
   ```

### Step 4: Generate Project Context

Create `.claude/project-context.md` with: project overview, selected skills and why, integration points, development workflow.

### Step 5: Generate Documentation

Generate `docs/PROJECT_PLAN.md` and `docs/REQUIREMENTS.md` from templates. See [templates/](templates/) for the template files.

### Step 6: Create Initial Scaffolding

**LangGraph projects:** `src/agent.py`, `src/tools.py`, `src/config.py`, `tests/test_agent.py`
- `uv add langchain langgraph langchain-community`

**Databricks projects:** `notebooks/01_setup.py`, `configs/databricks.yml`, `src/utils.py`
- `uv add databricks-sdk databricks-connect`

**General projects:** `src/main.py`, `tests/test_main.py`, `configs/config.yaml`
- `uv add --dev pytest pytest-cov ruff`

### Step 7: Generate README.md

Include: quick start, prerequisites, installation with `uv sync`, project structure, skills used, links to docs.

### Step 8 (Optional): Cross-Platform Support

If user requests `--cross-platform`, generate instruction files for Claude Code, Codex CLI, and Gemini CLI from a canonical `instructions.md`. Uses `cross-platform-skill/scripts/convert_skill.py` for conversion.

| Platform | Instruction File | Commands Dir |
|----------|-----------------|--------------|
| Claude Code | `CLAUDE.md` | `.claude/commands/` |
| Codex CLI | `AGENTS.md` | `.codex/prompts/` |
| Gemini CLI | `GEMINI.md` | `.gemini/commands/` |

## Commands

### Initialize New Project
"Create a new project called [name] for [purpose]" → Execute Steps 1-7.

### Add Skills to Existing Project
"Add [skill-name] to this project" → Add submodule if needed, create symlink, update context and requirements.

### Generate Project Documentation
"Generate/update project documentation" → Read skill files, analyze code, generate/update docs.

### Validate Project Setup
"Validate project setup" → Verify directory structure, submodule status, symlinks, dependencies.

## References

- [templates/PROJECT_PLAN_template.md](templates/PROJECT_PLAN_template.md) - Project plan template
- [templates/REQUIREMENTS_template.md](templates/REQUIREMENTS_template.md) - Requirements template
- [examples/USAGE_EXAMPLES.md](examples/USAGE_EXAMPLES.md) - Usage examples for different project types
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
