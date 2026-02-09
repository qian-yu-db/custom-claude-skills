# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a curated collection of 15 specialized skills for Claude Code organized by domain: Databricks platform, LangGraph agents, Python development, planning/visualization, and general software engineering.

## Skill Structure

Every skill follows this standardized structure:
```
skill-name/
├── SKILL.md              # Main instructions with YAML frontmatter (required)
├── references/           # Technical deep-dives, loaded on demand (optional)
├── scripts/              # Generation/utility scripts (optional)
├── templates/            # Code templates (optional)
├── examples/             # Usage examples (optional)
└── assets/               # Files used in output (optional)
```

### YAML Frontmatter Format

All SKILL.md files must include this frontmatter with only `name` and `description`:
```yaml
---
name: skill-name
description: What the skill does AND when to use it (triggers). This is the primary discovery mechanism.
---
```

The `description` field serves as the triggering mechanism — include both what the skill does and specific use cases/contexts for when to activate it.

### Skill Best Practices

- **Body under 500 lines**: Keep SKILL.md concise. Extract large code blocks and reference material to `references/` files.
- **Progressive disclosure**: Only the description is always loaded. The body loads when triggered. References load on demand.
- **Don't explain what Claude knows**: Only include information Claude doesn't already have (Databricks-specific patterns, project-specific configs, etc.).
- **No extra documentation files**: Do not create README.md, QUICK_REFERENCE.md, CHANGELOG.md, etc. in skill directories.

## Development Guidelines

- **Python package management**: Always use `uv` (never pip). Use `uv run` to execute Python code
- **pyproject.toml**: Keep minimal unless project-specific requirements dictate otherwise
- **Error handling**: Do not add excessive try-except blocks
- **Skills are self-contained**: Each skill should be independently usable without dependencies on other skills

## Directory Organization

```
databricks_agent_dev_skills/   # Agent development (app builder, deploy, MCP, supervisor, retrieval tools)
databricks_platform_skills/    # DAB, notebooks
python_skills/                 # pytest, formatters
develop_planning_skills/       # Mermaid, cross-platform
project-skills/                # Project bootstrapping
general_skills/                # Jira, battle cards
git_skills/                    # Git worktree (plugin format)
```

## Common Commands in Generated Projects

Skills that generate Python projects typically include:
```bash
uv run start-server        # Start MLflow agent server
uv run start-app           # Start app with frontend
uv run agent-evaluate      # Run MLflow evaluation
uv run pytest --cov        # Run tests with coverage
uv run black <file>        # Format Python
uv run isort <file>        # Sort imports
uv run blackbricks <file>  # Format Databricks notebooks
uv run ruff check --fix    # Lint and fix
mmdc -i file.mermaid -o file.png  # Generate diagram images
```
