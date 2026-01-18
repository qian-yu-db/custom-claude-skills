# Databricks Agent Deploy to Model Serving via DAB

Deploy AI agents (LangGraph, OpenAI SDK, custom frameworks) to Databricks Model Serving using Databricks Asset Bundles (DAB) for infrastructure-as-code agent deployment.

## Overview

This skill automates the deployment of AI agents to Databricks Model Serving using Databricks Asset Bundles. It supports multiple agent frameworks, multi-environment deployments, and optional evaluation workflows.

## Key Features

- **Multi-framework Support**: LangGraph, OpenAI SDK, and custom agent frameworks
- **Infrastructure-as-Code**: Complete DAB configuration with `databricks.yml`
- **Multi-environment**: Separate dev/staging/prod deployments
- **MLflow Integration**: Automatic model logging and registration
- **Model Serving**: Automated endpoint creation and configuration
- **Optional Evaluation**: Add evaluation jobs when requested
- **Profile-based Deployment**: Use Databricks profiles for authentication

## Supported Agent Frameworks

1. **LangGraph**: Full LangGraph applications with state graphs and tools
2. **OpenAI SDK**: Agents using OpenAI Assistants API or custom OpenAI implementations
3. **Custom Frameworks**: Any agent following MLflow pyfunc pattern

## Quick Start

### Prerequisites

- Databricks CLI installed (`pip install databricks-cli`)
- Databricks workspace access with Model Serving enabled
- Unity Catalog enabled workspace
- Databricks profile configured
- Agent code ready for deployment

### Basic Usage

Tell Claude Code:
```
"Deploy my LangGraph agent to Databricks Model Serving using DAB with profile 'my-profile'"
```

Claude will:
1. Analyze your agent code
2. Generate MLflow logging code
3. Create complete DAB structure
4. Generate deployment scripts
5. Guide you through deployment

### Example Workflow

```bash
# 1. Log and register agent
python scripts/log_and_register.py \
    --agent-path src/agent/agent.py \
    --model-name main.agents.my_agent \
    --agent-type langgraph

# 2. Deploy to dev
./scripts/deploy.sh dev my-databricks-profile

# 3. Test the endpoint
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "Hello"}]}'

# 4. Deploy to prod
./scripts/deploy.sh prod my-databricks-profile
```

## Use Cases

- Deploy LangGraph multi-agent systems to production
- Set up RAG agents with Vector Search integration
- Deploy tool-calling agents with Unity Catalog functions
- Create multi-environment agent deployments (dev/staging/prod)
- Integrate agent deployment with CI/CD pipelines
- Manage agent versions and traffic routing

## Generated DAB Structure

```
agent-dab/
├── databricks.yml              # Main DAB configuration
├── resources/
│   ├── model_serving.yml       # Model serving endpoint config
│   └── evaluation_job.yml      # Optional: Evaluation job
├── src/
│   ├── agent/
│   │   ├── agent.py            # Agent implementation
│   │   └── config.py           # Configuration
│   └── evaluation/
│       └── eval.py             # Optional: Evaluation script
├── scripts/
│   ├── deploy.sh               # Deployment script
│   └── log_and_register.py     # MLflow logging script
└── README.md
```

## Configuration Options

### Environment Variables

The agent can access environment variables in Model Serving:
- `DATABRICKS_HOST`: Workspace URL
- `DATABRICKS_TOKEN`: Authentication token (from secrets)
- Custom variables for API keys, endpoints, etc.

### Workload Sizes

- **Small**: Low-traffic agents, testing
- **Medium**: Production agents with moderate traffic
- **Large**: High-traffic agents requiring more resources

### Traffic Routing

Configure A/B testing and gradual rollouts:
- Route traffic between model versions
- Canary deployments
- Blue/green deployments

## Documentation

- **[SKILL.md](databricks-agent-deploy-model-serving-dab/SKILL.md)**: Complete implementation guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Quick command reference
- **Reference Guides**:
  - DAB structure and configuration
  - Model serving options
  - Agent framework examples
  - Deployment commands

## Requirements

- Python 3.10+
- Databricks CLI
- MLflow
- Agent framework dependencies (langchain, langgraph, openai, etc.)
- Databricks workspace with:
  - Model Serving enabled
  - Unity Catalog enabled
  - Appropriate permissions

## Best Practices

1. **Version Control**: Keep DAB configurations in git
2. **Separate Environments**: Use different catalogs for dev/staging/prod
3. **Pin Versions**: Use specific model versions in production
4. **Test First**: Always test in dev before promoting to prod
5. **Monitor**: Enable auto-capture for inference logs
6. **Permissions**: Set appropriate access controls for each environment

## Example Prompts

- "Deploy my LangGraph agent to Model Serving using DAB"
- "Create a DAB configuration for my OpenAI agent with evaluation"
- "Update my agent deployment to use a new model version"
- "Set up multi-environment deployment for my RAG agent"
- "Deploy my agent with A/B testing configuration"

## Support

For issues or questions:
- Check the SKILL.md for detailed instructions
- Review reference documentation for specific configurations
- Consult Databricks documentation for Model Serving and DAB

## Version

Created: November 2025
