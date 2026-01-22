# Databricks Agent App Builder

Generate complete Databricks App projects with MLflow AgentServer for AI agents.

## Overview

This skill creates production-ready agent applications that deploy to Databricks Apps with:
- **MLflow AgentServer** for HTTP routing and automatic tracing
- **FastAPI + Uvicorn** backend
- **MCP tool integration** for Unity Catalog functions, Vector Search, and Genie
- **Parameterized deployment scripts** for easy CI/CD
- **Optional Frontend** - Production chat UI via sparse checkout from `app-templates` repo

## Supported Frameworks

| Framework | Use Case | Key Features |
|-----------|----------|--------------|
| **LangGraph** | Complex workflows | State machines, conditional routing, multi-step |
| **OpenAI Agents SDK** | Simple conversational | Direct MCP integration, minimal setup |
| **Non-Conversational** | Stateless APIs | Custom schemas, discrete task processing |

## Quick Start

### Generate a New Project

```bash
# Invoke the skill
/databricks-agent-app-builder

# Answer the prompts:
# 1. Agent type (conversational / non-conversational)
# 2. Framework (LangGraph / OpenAI Agents SDK)
# 3. Project name
# 4. Agent description
# 5. Frontend (optional - production chat UI via sparse checkout)
```

### Project Structure

```
my-agent-app/
├── agent_server/
│   ├── agent.py              # Your agent logic
│   ├── start_server.py       # MLflow AgentServer
│   ├── utils.py              # Utilities
│   └── evaluate_agent.py     # MLflow evaluation
├── scripts/
│   ├── quickstart.sh         # Local setup
│   └── deploy.sh             # Deployment automation
├── app.yaml                  # Databricks Apps config
├── pyproject.toml            # Dependencies
└── README.md
```

### Run Locally

```bash
cd my-agent-app
./scripts/quickstart.sh       # First-time setup
uv run start-server           # Start on port 8000
```

### Deploy to Databricks

```bash
./scripts/deploy.sh my-agent-app --create
```

## Installation

Add this skill to your Claude Code configuration:

```bash
# Copy skill to your .claude/skills directory
cp -r databricks-agent-app-builder ~/.claude/skills/
```

Or reference from the custom-claude-skills repository.

## Requirements

- **Python**: >= 3.11
- **uv**: Python package manager
- **Databricks CLI**: For deployment
- **Databricks Workspace**: With Apps enabled

## Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](SKILL.md) | Main skill instructions |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Command cheat sheet |
| [references/](references/) | Detailed pattern guides |
| [templates/](templates/) | Code templates |

## Version

**v1.0.0** - January 2025

## License

Apache-2.0
