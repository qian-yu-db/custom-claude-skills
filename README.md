# Custom Claude Skills Collection

A curated collection of specialized skills for Claude Code to enhance productivity across Databricks development, LangGraph agents, Python development, planning & visualization, and general software engineering tasks.

## Overview

This repository contains 14 custom skills organized by domain. Each skill provides specialized knowledge, workflows, and tool integrations. See individual skill directories for detailed documentation.

## Available Skills

### Databricks Agent Development Skills (5)

1. **[databricks-agent-app-builder](databricks_agent_dev_skills/databricks-agent-app-builder/)** - Generate complete Databricks App projects with MLflow agent server for LangGraph, OpenAI Agents SDK, or non-conversational agents
2. **[databricks-agent-deploy-model-serving-dab](databricks_agent_dev_skills/databricks-agent-deploy-model-serving-dab/)** - Deploy agents (LangGraph, OpenAI SDK, custom) to Model Serving using Databricks Asset Bundles with serverless compute
3. **[langgraph-mcp-tool](databricks_agent_dev_skills/langgraph-mcp-tool/)** - Create LangChain-compatible tools from Databricks MCP servers (managed and external) for use in any AI agent framework
4. **[langgraph-multi-agent-supervisor](databricks_agent_dev_skills/langgraph-multi-agent-supervisor/)** - Build multi-agent systems with intelligent supervisor orchestration of specialized worker agents
5. **[langgraph-structured-unstructured-tool](databricks_agent_dev_skills/langgraph-structured-unstructured-tool/)** - Set up Databricks retrieval tools using VectorSearchRetrieverTool (RAG) and GenieAgent (SQL)

### Databricks Platform Skills (2)

1. **[databricks-asset-bundle](databricks_platform_skills/databricks-asset-bundle/)** - Generate Databricks Asset Bundle configurations with serverless compute, modular structure, and multiple input formats (text, Mermaid diagrams, workflow images)
2. **[databricks-local-notebook](databricks_platform_skills/databricks-local-notebook/)** - Create Databricks notebooks with local IDE development support via Databricks Connect

### Python Skills (2)

1. **[pytest-test-creator](python_sklls/pytest-test-creator/)** - Auto-generate comprehensive unit tests using pytest, coverage, and uv
2. **[python-code-formatter](python_sklls/python-code-formatter/)** - Format Python code with intelligent tool selection (blackbricks for Databricks, black+isort for regular Python)

### Planning & Visualization Skills (2)

1. **[mermaid-diagrams-creator](develop_planning_skills/mermaid-diagrams-creator/)** - Create clean Mermaid diagrams (flowcharts, sequence, class, ER, state) with automatic PNG/SVG/PDF generation
2. **[cross-platform-skill](develop_planning_skills/cross-platform-skill/)** - Convert Claude Code skills to work with Codex CLI and Gemini CLI for cross-platform compatibility

### Project Skills (1)

1. **[project-starter](project-skills/project-starter/)** - Bootstrap new projects with curated skills, uv environment management, git submodules for skill portability, and comprehensive documentation (v1.2.1)

### General Skills (2)

1. **[jira-epic-creator](general_skills/jira-epic-creator/)** - Transform documents into structured Jira epics with comprehensive user stories
2. **[battle-card-creator](general_skills/battle-card-creator/)** - Automate competitive battle card creation with research guidelines and templates

## Repository Structure

```
custom-claude-skills/
├── databricks_agent_dev_skills/   # 5 Agent development skills
├── databricks_platform_skills/    # 2 Databricks platform skills
├── python_sklls/                  # 2 Python development skills
├── develop_planning_skills/       # 2 Planning & visualization skills
├── project-skills/                # 1 Project bootstrapping skill
├── general_skills/                # 2 General-purpose skills
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

**Bootstrap New Project**:
```bash
# Start a new project with curated skills and uv environment
project-starter → (select skills) → auto-generate project structure + docs + uv setup
```

**Visual Workflow to Production**:
```bash
# Design workflow → generate DAB → deploy with serverless
mermaid-diagrams-creator → databricks-asset-bundle → databricks-agent-deploy-model-serving-dab
```

**Databricks Development**:
```bash
# Create a notebook → orchestrate with DAB → deploy to Model Serving
databricks-local-notebook → databricks-asset-bundle → databricks-agent-deploy-model-serving-dab
```

**LangGraph Agent Development**:
```bash
# Set up retrieval tools → combine with supervisor
langgraph-structured-unstructured-tool + langgraph-mcp-tool → langgraph-multi-agent-supervisor
```

**Python Development**:
```bash
# Format code → generate tests (all with uv)
python-code-formatter → pytest-test-creator
```

**Architecture Documentation**:
```bash
# Create diagrams → export images → document system
mermaid-diagrams-creator → (auto-generate PNG/SVG/PDF)
```

**Project Management**:
```bash
# Document requirements → create JIRA epics → competitive analysis
jira-epic-creator → battle-card-creator
```

**Cross-Platform Sharing**:
```bash
# Convert skills for other AI coding assistants
cross-platform-skill → (generate Codex/Gemini compatible instructions)
```

## Requirements

- Claude Code CLI
- Git for version control
- Skill-specific requirements (see individual skill READMEs)

## License

Apache-2.0

## Version

**v1.3.0** - January 2026

### Recent Updates

**v1.3.0** (January 2026):
- 🔄 **Reorganized skill structure**: Consolidated agent development skills into `databricks_agent_dev_skills/` directory
- ✨ **Added databricks-agent-app-builder**: Generate complete Databricks App projects with MLflow agent server
- 🔧 **Renamed langgraph-mcp-tool-calling-agent** to **langgraph-mcp-tool**: Focused on tool creation from MCP servers
- 🔧 **Renamed langgraph-unstructured-tool-agent** to **langgraph-structured-unstructured-tool**: Combined Vector Search and Genie tools
- 📝 **Added CLAUDE.md**: Project guidance for Claude Code instances
- Total skills: 15 → 14 (consolidated and streamlined)

**v1.2.1** (December 2025):
- Fixed mermaid-diagrams-creator: Made image generation mandatory
- Enhanced project-starter with improved git submodule workflow

**v1.2.0** (December 2025):
- Added mermaid-diagrams-creator and cross-platform-skill
- Enhanced databricks-asset-bundle with serverless compute and Mermaid support
- Added YAML frontmatter to all skills
