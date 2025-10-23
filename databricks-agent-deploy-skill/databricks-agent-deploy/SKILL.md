---
name: databricks-agent-deploy
description: Deploy AI agents on Databricks Apps with MLflow tracing, git-based versioning, and async server support. Use when user needs to create, configure, or deploy agents to Databricks Apps (not Model Serving), set up agent infrastructure, implement streaming/non-streaming endpoints, or work with the agent-on-app-proto patterns.
---

# Databricks Agent Deployment

Deploy AI agents on Databricks Apps with MLflow tracing, git-based versioning, and full control over agent invocation behavior.

## When to Use This Skill

Use this skill when:
- Deploying agents to **Databricks Apps** (not Model Serving)
- Creating agent projects with MLflow tracing
- Setting up async FastAPI servers for agent endpoints
- Implementing streaming and non-streaming invocations
- Working with git-based model versioning
- Testing agent deployments
- Integrating tools, Genie spaces, or external APIs with agents

## Quick Start

### Create New Agent Project

Use the initialization script to create a complete agent project structure:

```bash
python scripts/init_agent_project.py my-agent-app
```

This creates:
- `src/agent.py` - Agent implementation with MLflow tracing
- `server.py` - FastAPI async server
- `requirements.txt` - Python dependencies
- `app.yaml` - App configuration
- `deploy.sh` - Deployment script
- `tests/` - Unit tests

### Implement Agent Logic

Edit `src/agent.py` to implement your agent:

```python
import mlflow

class Agent:
    @mlflow.trace
    def invoke(self, messages: list[dict]) -> str:
        # Implement non-streaming logic
        pass
    
    @mlflow.trace
    def stream(self, messages: list[dict]) -> Iterator[str]:
        # Implement streaming logic
        pass
```

### Deploy to Databricks Apps

```bash
cd my-agent-app
./deploy.sh
```

Or manually:

```bash
# Sync code
databricks sync . /Users/your.name/my-agent-app

# Deploy
databricks apps deploy my-agent-app \
  --source-code-path /Workspace/Users/your.name/my-agent-app
```

### Test Deployment

```bash
python scripts/test_agent.py https://workspace.cloud.databricks.com/apps/my-agent-app \
  --token <your-token> \
  --message "Hello!"
```

## Key Concepts

### Apps vs Model Serving

Databricks Apps offers several advantages for agent deployment:

- **Faster validation**: Test authentication with tools/endpoints in seconds
- **Git-based versioning**: Use MLflow git-based logged models
- **Real-time tracing**: Built-in MLflow tracing for debugging
- **Local development**: Develop with IDEs and AI coding tools
- **Custom control**: Full control over async server behavior

### Agent Structure

Agents must implement:

1. **Invoke method**: Non-streaming response
   - Decorated with `@mlflow.trace`
   - Takes `messages: list[dict]` parameter
   - Returns `str` response

2. **Stream method**: Streaming response
   - Decorated with `@mlflow.trace`
   - Takes `messages: list[dict]` parameter
   - Yields `str` chunks

### Server Requirements

FastAPI server must provide:

- `GET /health` - Health check endpoint
- `POST /invocations` - Main agent endpoint
  - Accepts JSON with `messages` and optional `stream` fields
  - Returns JSON response or streaming text

## Common Patterns

### Tool-Calling Agent

For agents that use external tools, see `references/agent-patterns.md` for the complete tool-calling agent pattern using LangChain's `create_tool_calling_agent`.

### RAG Agent

For retrieval-augmented generation, see `references/agent-patterns.md` for the RAG pattern using Databricks Vector Search.

### Multi-Agent System

For routing queries to specialized sub-agents, see `references/agent-patterns.md` for the supervisor agent pattern.

### Genie Integration

For agents that query Genie spaces for data, see `references/agent-patterns.md` for the Genie integration pattern.

## Deployment Workflow

1. **Develop Locally**
   - Implement agent logic
   - Add tools and integrations
   - Test with MLflow tracing

2. **Log with MLflow**
   - Log agent as MLflow model
   - Include git commit hash
   - Verify model signature

3. **Create App**
   - Use CLI to create Databricks App
   - Configure resources (endpoints, etc.)
   - Set permissions

4. **Deploy Code**
   - Sync local code to workspace
   - Deploy app with source code path
   - Verify deployment

5. **Test & Monitor**
   - Test invoke and stream endpoints
   - Review MLflow traces
   - Monitor logs and metrics

For detailed deployment commands, see `references/deployment-commands.md`.

## Authentication

### Tool Authentication
- Store API keys in Databricks secrets
- Use Unity Catalog external connections
- Pass credentials securely to tools

### Endpoint Authentication
- Personal access tokens (development)
- OAuth 2.0 (production recommended)
- Service principal credentials

### Testing Authentication
Validate authentication locally before deploying to Apps. Use the async server to test connections to external services.

## MLflow Tracing

All agent interactions are automatically traced when using the `@mlflow.trace` decorator:

```python
@mlflow.trace
def invoke(self, messages: list[dict]) -> str:
    # All operations inside this method are traced
    result = self.llm.invoke(messages)
    return result
```

View traces in the Databricks MLflow UI to debug agent behavior and monitor performance.

## Scripts

### init_agent_project.py

Creates a new agent project with complete structure:

```bash
python scripts/init_agent_project.py <project-name> [output-dir]
```

### test_agent.py

Tests a deployed agent's endpoints:

```bash
python scripts/test_agent.py <app-url> \
  --token <token> \
  --message "Test message"
```

Options:
- `--health-only`: Test only health endpoint
- `--stream-only`: Test only streaming
- `--no-stream`: Skip streaming tests
- `--message`: Add test messages (can repeat)

## References

- **references/deployment-workflow.md**: Complete deployment workflow guide
- **references/agent-patterns.md**: Code patterns for different agent types
- **references/deployment-commands.md**: CLI commands and deployment scripts

## Troubleshooting

### Agent Not Responding
1. Check health endpoint: `curl https://app-url/health`
2. Review app logs: `databricks apps logs <app-name>`
3. Verify MLflow traces in workspace

### Authentication Errors
1. Validate credentials locally first
2. Check Unity Catalog connection permissions
3. Verify secret scope access

### Deployment Failures
1. Ensure Databricks CLI is configured
2. Check app name doesn't already exist
3. Verify workspace permissions
4. Review deployment logs

### Streaming Issues
1. Test non-streaming first
2. Verify client supports streaming
3. Check network/proxy settings
4. Review server logs for errors

## Best Practices

1. **Always use MLflow tracing** - Decorate all agent methods
2. **Test locally first** - Validate before deploying
3. **Use git versioning** - Log git commit hash with models
4. **Implement health checks** - Always include `/health` endpoint
5. **Handle errors gracefully** - Return proper HTTP status codes
6. **Use OAuth in production** - Avoid personal access tokens
7. **Monitor traces regularly** - Check MLflow UI for issues
8. **Set appropriate permissions** - Follow principle of least privilege
9. **Document tool usage** - Include clear tool descriptions in prompts
10. **Version control everything** - Use git for all agent code
