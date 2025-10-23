# Databricks Agent Deployment Skill

A comprehensive skill for deploying AI agents on Databricks Apps, based on the agent-on-app-proto repository patterns.

## What This Skill Provides

This skill enables Claude to help you:

1. **Create agent projects** with complete infrastructure
2. **Deploy agents to Databricks Apps** (not Model Serving)
3. **Implement streaming and non-streaming endpoints**
4. **Set up MLflow tracing** for debugging and monitoring
5. **Test deployed agents** via their API endpoints
6. **Work with common agent patterns** (tool-calling, RAG, multi-agent, Genie integration)

## Key Features

### 🚀 Quick Start Scripts
- **init_agent_project.py**: Creates a complete agent project structure with all necessary files
- **test_agent.py**: Tests deployed agents with support for streaming and non-streaming

### 📚 Comprehensive References
- **deployment-workflow.md**: Complete guide to the agent deployment workflow
- **agent-patterns.md**: Code patterns for common agent types (tool-calling, RAG, multi-agent, Genie)
- **deployment-commands.md**: CLI commands and deployment scripts

### ⚡ Advantages of Apps vs Model Serving
- Faster authentication validation (seconds vs minutes)
- Git-based MLflow model versioning
- Real-time tracing for debugging
- Local development with IDEs and AI tools
- Full control over async server behavior

## How to Use This Skill

Once installed, Claude will automatically use this skill when you ask questions like:

- "Create a new agent project for deployment on Databricks Apps"
- "Help me deploy my agent to Databricks Apps"
- "Set up streaming and non-streaming endpoints for my agent"
- "Show me how to implement a tool-calling agent for Databricks"
- "How do I test my deployed agent?"
- "Create an agent that uses Genie spaces"

## What Gets Created

When you ask Claude to create a new agent project, it will generate:

```
my-agent-app/
├── src/
│   └── agent.py          # Agent implementation with MLflow tracing
├── tests/
│   └── test_agent.py     # Unit tests
├── config/               # Configuration files
├── server.py             # FastAPI async server
├── requirements.txt      # Python dependencies
├── app.yaml             # App configuration
├── deploy.sh            # Deployment script
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## Common Workflows

### 1. Create and Deploy a New Agent

```bash
# Claude creates the project
python scripts/init_agent_project.py my-agent

# You implement the logic
cd my-agent
# Edit src/agent.py

# Test locally
python server.py

# Deploy to Databricks Apps
./deploy.sh
```

### 2. Test a Deployed Agent

```bash
# Claude provides the test script
python scripts/test_agent.py https://workspace.cloud.databricks.com/apps/my-agent \
  --token <your-token> \
  --message "Test query"
```

### 3. Implement Different Agent Types

Claude can help you implement:
- **Tool-calling agents** using LangChain
- **RAG agents** with Vector Search
- **Multi-agent systems** with supervisor pattern
- **Genie integration** for data queries

## Agent Patterns Included

### Tool-Calling Agent
Agents that can use external tools (APIs, databases, etc.)

### RAG (Retrieval Augmented Generation)
Agents that search vector databases to ground responses in documents

### Multi-Agent Supervisor
Routes queries to specialized sub-agents based on intent

### Genie Space Integration
Queries Databricks Genie spaces for data analysis

## Authentication Support

The skill includes guidance for:
- Tool authentication (API keys, Unity Catalog connections)
- Endpoint authentication (PATs, OAuth, service principals)
- Local testing before deployment
- Secure credential management

## MLflow Tracing

All agents created with this skill include automatic MLflow tracing:
- Debug agent behavior in real-time
- Monitor performance metrics
- Track tool usage and responses
- Review conversation history

## Requirements

To use this skill, you'll need:
- Databricks workspace with Apps enabled
- Databricks CLI installed and configured
- Python 3.11+
- Appropriate workspace permissions

## Best Practices Built In

The skill follows all Databricks best practices:
1. MLflow tracing on all agent methods
2. Git-based model versioning
3. Health check endpoints
4. Proper error handling
5. OAuth for production (not PATs)
6. Comprehensive testing
7. Clear documentation

## Troubleshooting

The skill includes troubleshooting guides for common issues:
- Agent not responding
- Authentication errors
- Deployment failures
- Streaming issues

## Support

For questions or issues related to:
- **This skill**: Ask Claude for help
- **Databricks Apps**: Check Databricks documentation
- **Agent-on-app-proto**: See the original repository at https://github.com/bbqiu/agent-on-app-proto

## Version

Based on the agent-on-app-proto repository patterns and Databricks best practices as of October 2025.
