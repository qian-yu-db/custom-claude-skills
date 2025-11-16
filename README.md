# Custom Claude Skills Collection

A curated collection of specialized skills for Claude Code to enhance productivity across Databricks development, LangGraph agents, Python development, and general software engineering tasks.

## Overview

This repository contains 11 custom skills organized by domain. Each skill provides specialized knowledge, workflows, and tool integrations. See individual skill directories for detailed documentation.

## Available Skills

### Databricks Platform Skills (3)

1. **[databricks-asset-bundle-skill](databricks_platform_skills/databricks-asset-bundle-skill/)** - Generate Databricks Asset Bundle configurations from notebooks/Python files with task dependencies
2. **[databricks-local-notebook-skill](databricks_platform_skills/databricks-local-notebook-skill/)** - Create Databricks notebooks with local IDE development support via Databricks Connect
3. **[databricks-agent-deploy2app-skill](databricks_platform_skills/databricks-agent-deploy2app-skill/)** - Deploy AI agents to Databricks Apps with complete infrastructure setup

### LangGraph Skills (4)

1. **[langgraph-genie-agent](langgraph_skills/langgraph-genie-agent/)** - Build LangGraph agents with Databricks Genie API for natural language data querying
2. **[langgraph-unstructured-tool-agent](langgraph_skills/langgraph-unstructured-tool-agent/)** - Build RAG agents with Databricks Vector Search (4 patterns: simple, tool-calling, multi-hop, self-query)
3. **[langgraph-multi-agent-supervisor](langgraph_skills/langgraph-multi-agent-supervisor/)** - Build multi-agent systems with intelligent supervisor orchestration
4. **[langgraph-mcp-tool-calling-agent](langgraph_skills/langgraph-mcp-tool-calling-agent/)** - Build agents with Model Context Protocol (MCP) tool integration

### Python Skills (2)

1. **[pytest-test-creator](python_sklls/pytest-test-creator/)** - Auto-generate comprehensive unit tests using pytest, coverage, and uv
2. **[python-code-formatter](python_sklls/python-code-formatter/)** - Format Python code with intelligent tool selection (blackbricks for Databricks, black+isort for regular Python)

### General Skills (2)

1. **[jira-epic-creator-skill](general_skills/jira-epic-creator-skill/)** - Transform documents into structured Jira epics with comprehensive user stories
2. **[battle-card-creator-skill](general_skills/battle-card-creator-skill/)** - Automate competitive battle card creation with research guidelines and templates

## Repository Structure

```
custom-claude-skills/
├── databricks_platform_skills/    # 3 Databricks skills
├── langgraph_skills/              # 4 LangGraph agent skills
├── python_sklls/                  # 2 Python development skills
├── general_skills/                # 2 general-purpose skills
└── README.md
```

## Installation

Each skill is self-contained in its own directory with detailed documentation:

1. Navigate to the specific skill directory
2. Follow the installation instructions in the skill's README.md
3. Upload the skill package to Claude Code as needed

## Documentation

Each skill includes comprehensive documentation in its directory:
- **README.md** - Overview and quick start
- **SKILL.md** - Main skill instructions for Claude
- **QUICK_REFERENCE.md** - Command reference card (where applicable)
- **Reference guides** - Detailed technical documentation

## Quick Start Examples

**Databricks Development**:
```bash
# Create a notebook → orchestrate with DAB → deploy agents to Apps
databricks-local-notebook → databricks-asset-bundle → databricks-agent-deploy2app
```

**LangGraph Agent Development**:
```bash
# Build specialized agents → combine with supervisor
langgraph-genie-agent + langgraph-unstructured-tool-agent → langgraph-multi-agent-supervisor
```

**Python Development**:
```bash
# Format code → generate tests
python-code-formatter → pytest-test-creator
```

## Requirements

- Claude Code CLI
- Git for version control
- Skill-specific requirements (see individual skill READMEs)

## License

Apache-2.0

## Version

Last updated: November 2025
