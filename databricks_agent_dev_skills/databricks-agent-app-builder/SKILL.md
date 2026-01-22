---
name: databricks-agent-app-builder
description: Generate complete Databricks App projects with MLflow agent server for LangGraph, OpenAI Agents SDK, or non-conversational agents
version: 1.0.0
author: Custom Skills
tags: [databricks, mlflow, agent, langgraph, openai, fastapi, databricks-apps]
---

# Databricks Agent App Builder

Generate production-ready Databricks App projects with MLflow AgentServer for AI agents.

## When to Use This Skill

Use this skill when:
- Creating a new AI agent application for Databricks Apps
- Building conversational agents with LangGraph or OpenAI Agents SDK
- Building non-conversational (stateless) API agents
- Setting up MLflow tracing for agent observability
- Deploying agents to Databricks workspace

## Skill Workflow

### Step 1: Gather Requirements

Ask the user these questions to determine the project configuration:

1. **Agent Type**: "What type of agent are you building?"
   - **Conversational**: Chat-based agents with streaming support
   - **Non-Conversational**: Stateless API agents for discrete tasks

2. **Framework** (if conversational): "Which framework do you prefer?"
   - **LangGraph**: For complex multi-step workflows, state machines, conditional routing
   - **OpenAI Agents SDK**: For simpler conversational agents with direct MCP integration

3. **Project Name**: "What should I name the project?"
   - Use kebab-case (e.g., `my-agent-app`)

4. **Agent Description**: "Briefly describe what your agent does"
   - Used for instructions and documentation

5. **Frontend** (if conversational): "Do you want a production chat UI frontend?"
   - **Yes**: Will sparse checkout `e2e-chatbot-app-next` from app-templates repo
   - **No**: API-only deployment (can add frontend later)

### Step 2: Generate Project Structure

Based on user selections, generate the following structure:

```
{project-name}/
├── agent_server/
│   ├── __init__.py
│   ├── agent.py              # Framework-specific agent logic
│   ├── start_server.py       # MLflow AgentServer setup
│   ├── utils.py              # Auth & stream utilities (conversational only)
│   └── evaluate_agent.py     # MLflow evaluation script
├── scripts/
│   ├── quickstart.sh         # Local setup wizard
│   └── deploy.sh             # Parameterized deployment script
├── app.yaml                  # Databricks Apps configuration
├── pyproject.toml            # Python dependencies (uv)
├── .env.example              # Environment template
├── .gitignore
└── README.md                 # Project documentation
```

### Step 3: Generate Files

Use the templates in `templates/` directory as reference. Customize based on:
- Framework selection (LangGraph / OpenAI Agents SDK / Non-Conversational)
- Agent description and purpose
- Project name

### Step 4: Setup Frontend (Optional)

If the user requested a frontend for conversational agents, set it up via sparse checkout:

#### 4.1 Sparse Checkout Frontend

```bash
# Create a temporary clone with sparse checkout
git clone --filter=blob:none --sparse https://github.com/databricks/app-templates.git temp-app-templates
cd temp-app-templates
git sparse-checkout set agent-langgraph/e2e-chatbot-app-next

# Move frontend to sibling directory
mv agent-langgraph/e2e-chatbot-app-next ../{project-name}-frontend
cd ..
rm -rf temp-app-templates
```

#### 4.2 Configure Frontend

After checkout, configure the frontend to connect to the agent:

```bash
cd {project-name}-frontend

# Create .env.local with agent endpoint
cat > .env.local << 'EOF'
# Databricks Authentication
DATABRICKS_CONFIG_PROFILE=DEFAULT

# Agent Serving Endpoint (created by deploying the backend agent)
DATABRICKS_SERVING_ENDPOINT={agent-endpoint-name}

# Database (optional - for persistent chat history)
# Uncomment and configure if using Lakebase
# PGUSER=your-databricks-username
# PGHOST=your-lakebase-host
# PGDATABASE=databricks_postgres
# PGPORT=5432
EOF
```

#### 4.3 Frontend Project Structure

The frontend is a production-ready full-stack application:

```
{project-name}-frontend/
├── client/                 # React + Vite frontend
├── server/                 # Express.js backend (BFF)
├── packages/               # Shared libraries
│   ├── core/              # Domain types, errors
│   ├── auth/              # Authentication utilities
│   ├── ai-sdk-providers/  # Databricks AI SDK integration
│   ├── db/                # Database layer (Drizzle ORM)
│   └── utils/             # Shared utilities
├── scripts/
│   ├── quickstart.sh      # Interactive setup wizard
│   └── start-app.sh       # Start development server
├── databricks.yml         # Asset Bundle configuration
└── package.json           # npm workspaces monorepo
```

#### 4.4 Frontend Setup Options

**Option A: Interactive Setup (Recommended)**
```bash
cd {project-name}-frontend
./scripts/quickstart.sh
```

The quickstart script will:
- Install prerequisites (Node.js 20, Databricks CLI)
- Configure authentication
- Set up serving endpoint
- Optionally configure database for persistent chat history
- Deploy to Databricks (optional)

**Option B: Manual Setup**
```bash
cd {project-name}-frontend
npm install
npm run dev  # Starts on localhost:3000 (frontend) and localhost:3001 (backend)
```

#### 4.5 Frontend Deployment

The frontend deploys separately via Databricks Asset Bundle:

```bash
cd {project-name}-frontend

# Update databricks.yml with your endpoint name
# Then deploy:
databricks bundle validate
databricks bundle deploy
databricks bundle run databricks_chatbot
```

#### 4.6 Final Directory Structure

After setup, you'll have two sibling directories:

```
workspace/
├── {project-name}/           # Backend agent (Python/MLflow)
│   ├── agent_server/
│   ├── app.yaml
│   └── pyproject.toml
│
└── {project-name}-frontend/  # Chat UI (TypeScript/React)
    ├── client/
    ├── server/
    ├── databricks.yml
    └── package.json
```

This separation allows:
- Independent deployment cycles
- Different tech stacks (Python vs Node.js)
- Separate scaling and resource management

## Code Generation Rules

### Common Files (All Frameworks)

#### app.yaml
```yaml
command: ["uv", "run", "start-server"]
# For conversational with frontend: ["uv", "run", "start-app"]

env:
  - name: MLFLOW_TRACKING_URI
    value: "databricks"
  - name: MLFLOW_REGISTRY_URI
    value: "databricks-uc"
  - name: MLFLOW_EXPERIMENT_ID
    valueFrom: experiment
```

#### start_server.py
```python
import logging
from dotenv import load_dotenv
from mlflow.genai.agent_server import AgentServer, setup_mlflow_git_based_version_tracking

load_dotenv(dotenv_path=".env.local", override=True)

import agent_server.agent  # noqa: E402

# For conversational agents:
agent_server = AgentServer("ResponsesAgent", enable_chat_proxy=True)
# For non-conversational agents:
# agent_server = AgentServer()

app = agent_server.app

try:
    setup_mlflow_git_based_version_tracking()
except Exception as e:
    logging.warning(f"Git-based version tracking not available: {e}")

def main():
    agent_server.run(app_import_string="agent_server.start_server:app")
```

### Framework-Specific: LangGraph

#### Dependencies (pyproject.toml)
```toml
dependencies = [
    "fastapi>=0.115.12",
    "uvicorn>=0.34.2",
    "databricks-langchain>=0.12.0",
    "mlflow>=3.8.0rc0",
    "langgraph>=1.0.1",
    "langchain-mcp-adapters>=0.1.11",
    "python-dotenv",
]
```

#### agent.py Pattern
```python
from typing import AsyncGenerator
import mlflow
from databricks.sdk import WorkspaceClient
from databricks_langchain import ChatDatabricks, DatabricksMCPServer, DatabricksMultiServerMCPClient
from langchain.agents import create_agent
from mlflow.genai.agent_server import invoke, stream
from mlflow.types.responses import (
    ResponsesAgentRequest, ResponsesAgentResponse, ResponsesAgentStreamEvent,
    to_chat_completions_input,
)
from agent_server.utils import get_databricks_host_from_env, process_agent_astream_events

mlflow.langchain.autolog()

def init_mcp_client(workspace_client: WorkspaceClient) -> DatabricksMultiServerMCPClient:
    host_name = get_databricks_host_from_env()
    return DatabricksMultiServerMCPClient([
        DatabricksMCPServer(
            name="system-ai",
            url=f"{host_name}/api/2.0/mcp/functions/system/ai",
        ),
    ])

async def init_agent(workspace_client=None):
    mcp_client = init_mcp_client(workspace_client or WorkspaceClient())
    tools = await mcp_client.get_tools()
    return create_agent(tools=tools, model=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet"))

@invoke()
async def non_streaming(request: ResponsesAgentRequest) -> ResponsesAgentResponse:
    outputs = [event.item async for event in streaming(request) if event.type == "response.output_item.done"]
    return ResponsesAgentResponse(output=outputs)

@stream()
async def streaming(request: ResponsesAgentRequest) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    agent = await init_agent()
    messages = {"messages": to_chat_completions_input([i.model_dump() for i in request.input])}
    async for event in process_agent_astream_events(agent.astream(input=messages, stream_mode=["updates", "messages"])):
        yield event
```

### Framework-Specific: OpenAI Agents SDK

#### Dependencies (pyproject.toml)
```toml
dependencies = [
    "fastapi>=0.115.12",
    "uvicorn>=0.34.2",
    "databricks-openai>=0.8.0",
    "mlflow>=3.8.0rc0",
    "openai-agents>=0.4.1",
    "python-dotenv",
]
```

#### agent.py Pattern
```python
from typing import AsyncGenerator
import mlflow
from agents import Agent, Runner, set_default_openai_api, set_default_openai_client
from agents.tracing import set_trace_processors
from databricks_openai import AsyncDatabricksOpenAI
from databricks_openai.agents import McpServer
from mlflow.genai.agent_server import invoke, stream
from mlflow.types.responses import (
    ResponsesAgentRequest, ResponsesAgentResponse, ResponsesAgentStreamEvent,
)
from agent_server.utils import get_databricks_host_from_env, process_agent_stream_events

set_default_openai_client(AsyncDatabricksOpenAI())
set_default_openai_api("chat_completions")
set_trace_processors([])
mlflow.openai.autolog()

async def init_mcp_server():
    return McpServer(
        url=f"{get_databricks_host_from_env()}/api/2.0/mcp/functions/system/ai",
        name="system.ai uc function mcp server",
    )

def create_agent(mcp_server: McpServer) -> Agent:
    return Agent(
        name="agent-name",
        instructions="Your agent instructions here",
        model="databricks-claude-3-7-sonnet",
        mcp_servers=[mcp_server],
    )

@invoke()
async def invoke(request: ResponsesAgentRequest) -> ResponsesAgentResponse:
    async with await init_mcp_server() as mcp_server:
        agent = create_agent(mcp_server)
        messages = [i.model_dump() for i in request.input]
        result = await Runner.run(agent, messages)
        return ResponsesAgentResponse(output=[item.to_input_item() for item in result.new_items])

@stream()
async def stream(request: dict) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    async with await init_mcp_server() as mcp_server:
        agent = create_agent(mcp_server)
        messages = [i.model_dump() for i in request.input]
        result = Runner.run_streamed(agent, input=messages)
        async for event in process_agent_stream_events(result.stream_events()):
            yield event
```

### Framework-Specific: Non-Conversational

#### Dependencies (pyproject.toml)
```toml
dependencies = [
    "fastapi>=0.115.12",
    "uvicorn[standard]>=0.34.2",
    "mlflow>=3.7.0",
    "databricks-sdk>=0.63.0",
    "pydantic>=2.11",
    "python-dotenv",
]
```

#### agent.py Pattern
```python
import json
import os
from databricks.sdk import WorkspaceClient
from mlflow.genai.agent_server import invoke
from pydantic import BaseModel, Field

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()

class AgentInput(BaseModel):
    # Define your input schema
    document_text: str = Field(..., description="Input text to process")

class AgentOutput(BaseModel):
    # Define your output schema
    result: str = Field(..., description="Processing result")

@invoke()
async def invoke(data: dict) -> dict:
    input_data = AgentInput(**data)

    # Your processing logic here
    llm_response = openai_client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "databricks-claude-3-7-sonnet"),
        messages=[{"role": "user", "content": input_data.document_text}],
    )

    result = llm_response.choices[0].message.content
    return AgentOutput(result=result).model_dump()
```

## Deployment Guide

### Local Development

```bash
# First-time setup
./scripts/quickstart.sh

# Start server
uv run start-server

# Test API
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

### Deploy to Databricks Apps

```bash
# Option 1: Use deploy.sh script
./scripts/deploy.sh my-app-name --create

# Option 2: Manual steps
databricks apps create my-app-name
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/my-app-name"
databricks apps deploy my-app-name --source-code-path /Workspace/Users/$DATABRICKS_USERNAME/my-app-name
```

### Query Deployed App

```bash
# Get OAuth token (PATs not supported)
databricks auth token

# Query
curl -X POST <app-url>/invocations \
  -H "Authorization: Bearer <oauth-token>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

## Frontend Integration

For conversational agents that need a chat UI, see **Step 4: Setup Frontend (Optional)** above.

**Quick Summary:**
- Source: `https://github.com/databricks/app-templates` → `agent-langgraph/e2e-chatbot-app-next/`
- Tech stack: React + Vite + Express.js + TypeScript + Tailwind CSS
- Requires: Node.js 20+, npm 8+
- Features:
  - Persistent chat history (optional, requires Lakebase)
  - Databricks authentication
  - Streaming responses via Vercel AI SDK
  - Databricks Asset Bundle deployment

**Adding Frontend Later:**

If the user initially chose API-only and wants to add frontend later:

```bash
# Navigate to parent of your agent project
cd /path/to/workspace

# Sparse checkout the frontend
git clone --filter=blob:none --sparse https://github.com/databricks/app-templates.git temp-clone
cd temp-clone
git sparse-checkout set agent-langgraph/e2e-chatbot-app-next
mv agent-langgraph/e2e-chatbot-app-next ../my-agent-frontend
cd .. && rm -rf temp-clone

# Configure and run
cd my-agent-frontend
./scripts/quickstart.sh
```

## Reference Documentation

See the `references/` directory for detailed patterns:
- `mlflow-agent-server.md` - AgentServer setup and decorators
- `langgraph-patterns.md` - LangGraph-specific patterns
- `openai-agents-patterns.md` - OpenAI Agents SDK patterns
- `non-conversational-patterns.md` - Stateless agent patterns
- `deployment-guide.md` - Complete deployment instructions
