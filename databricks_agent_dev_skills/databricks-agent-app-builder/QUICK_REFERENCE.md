# Databricks Agent App Builder - Quick Reference

## Local Development Commands

```bash
# First-time setup
./scripts/quickstart.sh

# Start server (default port 8000)
uv run start-server

# Start with hot-reload
uv run start-server --reload

# Custom port
uv run start-server --port 8001

# Multiple workers
uv run start-server --workers 4

# Run evaluation
uv run agent-evaluate
```

## Test API

```bash
# Conversational (streaming)
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}], "stream": true}'

# Conversational (non-streaming)
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'

# Non-conversational
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"document_text": "...", "questions": ["..."]}'
```

## Deployment Commands

```bash
# Using deploy.sh script
./scripts/deploy.sh APP_NAME --create      # Create and deploy new app
./scripts/deploy.sh APP_NAME --update      # Update existing app
./scripts/deploy.sh APP_NAME --dry-run     # Show commands without executing

# Manual deployment
databricks apps create APP_NAME
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/APP_NAME"
databricks apps deploy APP_NAME --source-code-path /Workspace/Users/$DATABRICKS_USERNAME/APP_NAME
```

## Query Deployed App

```bash
# Get OAuth token (required - PATs not supported)
databricks auth token

# Query app
curl -X POST <app-url>/invocations \
  -H "Authorization: Bearer <oauth-token>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

## Environment Variables

```bash
# .env.local (backend agent)
DATABRICKS_CONFIG_PROFILE=DEFAULT          # Or use HOST/TOKEN
MLFLOW_EXPERIMENT_ID=<experiment-id>       # Required
MLFLOW_TRACKING_URI="databricks"
MLFLOW_REGISTRY_URI="databricks-uc"
```

## Frontend Setup (Optional)

For conversational agents that need a production chat UI:

```bash
# Sparse checkout frontend from app-templates repo
git clone --filter=blob:none --sparse https://github.com/databricks/app-templates.git temp-clone
cd temp-clone
git sparse-checkout set agent-langgraph/e2e-chatbot-app-next
mv agent-langgraph/e2e-chatbot-app-next ../my-agent-frontend
cd .. && rm -rf temp-clone

# Setup and run frontend
cd my-agent-frontend
./scripts/quickstart.sh     # Interactive setup (recommended)
# OR
npm install && npm run dev  # Manual setup (localhost:3000)
```

### Frontend Environment Variables

```bash
# .env.local (frontend)
DATABRICKS_CONFIG_PROFILE=DEFAULT
DATABRICKS_SERVING_ENDPOINT=my-agent-endpoint  # Your deployed agent

# Optional: Database for persistent chat history
PGUSER=your-databricks-username
PGHOST=your-lakebase-host
PGDATABASE=databricks_postgres
PGPORT=5432
```

### Frontend Deployment

```bash
cd my-agent-frontend
databricks bundle validate
databricks bundle deploy
databricks bundle run databricks_chatbot
```

## Key Files

| File | Purpose |
|------|---------|
| `agent_server/agent.py` | Agent logic, model, tools |
| `agent_server/start_server.py` | MLflow AgentServer setup |
| `agent_server/utils.py` | Auth helpers, stream processing |
| `agent_server/evaluate_agent.py` | MLflow evaluation |
| `app.yaml` | Databricks Apps config |
| `pyproject.toml` | Python dependencies |

## Framework Comparison

| Aspect | LangGraph | OpenAI Agents SDK | Non-Conversational |
|--------|-----------|-------------------|-------------------|
| Streaming | Yes | Yes | No |
| MCP Client | `DatabricksMultiServerMCPClient` | `McpServer` | Optional |
| LLM | `ChatDatabricks` | `AsyncDatabricksOpenAI` | SDK OpenAI client |
| Execution | `agent.astream()` | `Runner.run()` | Direct `@invoke()` |
| agent_type | `"ResponsesAgent"` | `"ResponsesAgent"` | `None` |

## Common MCP Server Patterns

```python
# LangGraph - Unity Catalog function
DatabricksMCPServer.from_uc_function(
    catalog="main", schema="tools", function_name="send_email"
)

# LangGraph - Vector Search
DatabricksMCPServer.from_vector_search(
    catalog="main", schema="embeddings", index_name="docs"
)

# LangGraph - Genie Space
DatabricksMCPServer(
    name="genie",
    url=f"{host}/api/2.0/mcp/genie/{genie_space_id}",
)

# OpenAI Agents SDK
McpServer(
    url=f"{host}/api/2.0/mcp/functions/system/ai",
    name="system.ai"
)
```

## MLflow Decorators

```python
from mlflow.genai.agent_server import invoke, stream

@invoke()  # Register for non-streaming calls and evaluation
async def invoke_fn(request): ...

@stream()  # Register for streaming calls
async def stream_fn(request): ...
```
