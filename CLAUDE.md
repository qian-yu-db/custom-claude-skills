# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a curated collection of 15 specialized skills for Claude Code organized by domain: Databricks platform, LangGraph agents, Python development, planning/visualization, and general software engineering.

## Skill Structure

Every skill follows this standardized structure:
```
skill-name/
├── SKILL.md              # Main instructions with YAML frontmatter (required)
├── README.md             # Overview and quick start (required)
├── QUICK_REFERENCE.md    # Command reference card (optional)
├── references/           # Technical deep-dives (optional)
├── scripts/              # Generation/utility scripts (optional)
├── templates/            # Code templates (optional)
└── examples/             # Usage examples (optional)
```

### YAML Frontmatter Format

All SKILL.md files must include this frontmatter:
```yaml
---
name: skill-name
description: Detailed description for discovery
version: 1.0.0
author: Custom Skills
tags: [tag1, tag2, ...]
---
```

## Development Guidelines

- **Python package management**: Always use `uv` (never pip). Use `uv run` to execute Python code
- **pyproject.toml**: Keep minimal unless project-specific requirements dictate otherwise
- **Error handling**: Do not add excessive try-except blocks
- **Skills are self-contained**: Each skill should be independently usable without dependencies on other skills
- **Documentation pattern**: Include clear "When to Use This Skill" sections in SKILL.md

## Directory Organization

```
databricks_agent_dev_skills/   # Agent development (app builder, deploy, MCP, supervisor, retrieval tools)
databricks_platform_skills/    # DAB, notebooks
python_sklls/                  # pytest, formatters
develop_planning_skills/       # Mermaid, cross-platform
project-skills/                # Project bootstrapping
general_skills/                # Jira, battle cards
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
