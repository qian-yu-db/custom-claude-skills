# Databricks Agent Deployment - Quick Reference

## Installation

Upload the `databricks-agent-deploy.skill` file to Claude.

## Quick Commands

### Create New Agent Project
```bash
python scripts/init_agent_project.py my-agent-name
```

### Deploy to Databricks Apps
```bash
cd my-agent-name
./deploy.sh
```

### Test Deployed Agent
```bash
python scripts/test_agent.py <app-url> --token <token> --message "Hello"
```

## Agent Structure

### Required Methods

```python
import mlflow

class Agent:
    @mlflow.trace
    def invoke(self, messages: list[dict]) -> str:
        """Non-streaming response"""
        pass
    
    @mlflow.trace
    def stream(self, messages: list[dict]) -> Iterator[str]:
        """Streaming response"""
        pass
```

### Server Endpoints

- `GET /health` - Health check
- `POST /invocations` - Agent invocation

## Common Agent Patterns

| Pattern | Use Case | Reference |
|---------|----------|-----------|
| Tool-Calling | External APIs, databases | agent-patterns.md |
| RAG | Document Q&A | agent-patterns.md |
| Multi-Agent | Route to specialists | agent-patterns.md |
| Genie | Data queries | agent-patterns.md |

## Deployment Workflow

1. **Develop** → Implement agent logic locally
2. **Test** → Run server.py and test endpoints
3. **Log** → Use MLflow to log with git hash
4. **Deploy** → Sync and deploy to Apps
5. **Monitor** → Check traces and logs

## Authentication

| Type | Development | Production |
|------|-------------|------------|
| Endpoint | Personal Access Token | OAuth 2.0 |
| Tools | Databricks Secrets | Unity Catalog |
| Genie | API Key | Service Principal |

## CLI Commands

```bash
# Create app
databricks apps create my-agent

# Sync code
databricks sync ./local /Users/you/my-agent

# Deploy
databricks apps deploy my-agent --source-code-path /Workspace/Users/you/my-agent

# View logs
databricks apps logs my-agent

# Get URL
databricks apps get my-agent | jq -r .url
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not responding | Check health endpoint, review logs |
| Auth errors | Test locally first, check permissions |
| Deploy fails | Verify CLI config, check workspace access |
| Streaming issues | Test non-streaming first |

## Best Practices Checklist

- [ ] Use `@mlflow.trace` on all agent methods
- [ ] Test authentication locally before deploying
- [ ] Include git commit hash in MLflow logging
- [ ] Implement `/health` endpoint
- [ ] Handle errors with proper HTTP codes
- [ ] Use OAuth in production (not PATs)
- [ ] Monitor MLflow traces regularly
- [ ] Set minimal required permissions
- [ ] Document tool usage in prompts
- [ ] Version control all code

## Key Files in Generated Project

```
my-agent/
├── src/agent.py          # Your agent implementation
├── server.py             # FastAPI server (ready to use)
├── requirements.txt      # Dependencies (ready to use)
├── app.yaml             # App config (ready to use)
├── deploy.sh            # Deploy script (ready to use)
└── README.md            # Documentation
```

## Resources

- Skill references: Check `references/` folder
- Example patterns: See `agent-patterns.md`
- Deployment guide: See `deployment-workflow.md`
- CLI commands: See `deployment-commands.md`

## Getting Help

Ask Claude:
- "How do I implement a tool-calling agent?"
- "Show me how to add Vector Search to my agent"
- "Help me debug why my agent isn't responding"
- "What's the best way to authenticate with Genie?"
