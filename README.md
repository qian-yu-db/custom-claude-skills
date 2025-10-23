# Custom Claude Skills Collection

A curated collection of specialized skills for Claude Code to enhance productivity across Databricks development, project management, and general software engineering tasks.

## Overview

This repository contains custom skills that extend Claude's capabilities in specific domains. Each skill provides specialized knowledge, workflows, and tool integrations to help you accomplish complex tasks more effectively.

## Available Skills

### Databricks Skills

#### 1. Databricks Asset Bundle (`databricks-asset-bundle`)
**Purpose**: Automatically generate Databricks Asset Bundle configurations from notebooks or Python files with task dependencies.

**Key Features**:
- Automatic task type detection (.ipynb → notebooks, .py → Python wheel tasks)
- Flexible dependency graph support (linear, parallel, complex patterns)
- Configurable cluster settings
- Multi-environment targets (dev/prod)

**Use Cases**: ETL pipelines, ML workflows, data integration, analytics jobs

**Location**: `databricks_skills/databricks-asset-bundle-skill/`

#### 2. Databricks Local Notebook (`databricks-local-notebook`)
**Purpose**: Generate Databricks notebooks (.py) with seamless local IDE development support using Databricks Connect.

**Key Features**:
- Dual environment support (local IDE + Databricks workspace)
- Four notebook types: Agent, ML, ETL, General
- Automatic environment detection and connection
- Type-specific starter code and imports

**Use Cases**: AI agent development, ML model training, ETL pipelines, data analysis

**Location**: `databricks_skills/databricks-local-notebook-skill/`

#### 3. Databricks Agent Deploy (`databricks-agent-deploy`)
**Purpose**: Deploy AI agents on Databricks Apps with complete infrastructure setup.

**Key Features**:
- Complete agent project scaffolding
- Streaming and non-streaming endpoints
- MLflow tracing integration
- Support for tool-calling, RAG, multi-agent, and Genie patterns

**Use Cases**: LangGraph agents, chatbots, RAG systems, multi-agent workflows

**Location**: `databricks_skills/databricks-agent-deploy-skill/`

### General Skills

#### 4. Jira Epic Creator (`jira-epic-creator`)
**Purpose**: Transform documents into structured Jira epics with comprehensive user stories following a standardized 5-section template.

**Key Features**:
- 5-section epic template enforcement
- Automatic story breakdown with acceptance criteria
- Document analysis (extracts problems, solutions, metrics)
- INVEST principles and vertical slicing

**Use Cases**: Requirements docs, feature requests, project proposals, sprint planning

**Location**: `general_skills/jira-epic-creator/`

## Repository Structure

```
custom-claude-skills/
├── databricks_skills/
│   ├── databricks-asset-bundle-skill/
│   ├── databricks-local-notebook-skill/
│   └── databricks-agent-deploy-skill/
├── general_skills/
│   └── jira-epic-creator/
├── langgraph_skills/          # Future LangGraph-specific skills
├── python_sklls/              # Future Python-specific skills
└── README.md                  # This file
```

## Installation

Each skill is self-contained in its own directory. To use a skill:

1. Navigate to the specific skill directory
2. Follow the installation instructions in the skill's README.md
3. Upload the skill package (.zip) to Claude Code

Example:
```bash
cd databricks_skills/databricks-asset-bundle-skill
# Follow instructions in README.md
```

## Quick Start Guide

### For Databricks Development
1. Start with `databricks-local-notebook` to create notebooks
2. Use `databricks-asset-bundle` to orchestrate workflows
3. Deploy agents with `databricks-agent-deploy`

### For Project Management
1. Use `jira-epic-creator` to transform requirements into actionable epics

## Documentation

Each skill includes comprehensive documentation:

- **README.md**: Overview and quick start
- **USAGE_GUIDE.md**: Detailed examples and scenarios
- **QUICK_REFERENCE.md**: Command reference card
- **SKILL.md**: Main skill instructions for Claude

## Contributing

Skills are organized by domain:
- `databricks_skills/`: Databricks-specific capabilities
- `general_skills/`: Cross-domain utilities
- `langgraph_skills/`: LangGraph development (coming soon)
- `python_sklls/`: Python development utilities (coming soon)

## Requirements

### General
- Claude Code CLI
- Git for version control

### Skill-Specific
Refer to individual skill READMEs for specific requirements:
- Databricks skills require Databricks workspace and CLI
- Agent skills require Python 3.10+
- JIRA skills work with any text document format

## Support

For issues or questions:
- Check the specific skill's documentation
- Review the QUICK_REFERENCE.md for common operations
- Consult the USAGE_GUIDE.md for examples

## License

Apache-2.0

## Version

Last updated: October 2025
