# OpenAI Agents SDK Patterns

Reference for building agents with OpenAI Agents SDK on Databricks.

## Core Dependencies

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

## SDK Setup

### Databricks OpenAI Client

```python
from databricks_openai import AsyncDatabricksOpenAI, DatabricksOpenAI
from agents import set_default_openai_api, set_default_openai_client

# Async client (recommended for agent servers)
set_default_openai_client(AsyncDatabricksOpenAI())
set_default_openai_api("chat_completions")

# Sync client (for scripts)
client = DatabricksOpenAI()
```

**Note:** Works for all Databricks models except GPT-OSS, which uses a slightly different API.

### Tracing Configuration

```python
import mlflow
from agents.tracing import set_trace_processors

# Disable built-in OpenAI tracing, use MLflow only
set_trace_processors([])
mlflow.openai.autolog()
```

## MCP Integration

### McpServer

```python
from databricks_openai.agents import McpServer

async def init_mcp_server(host: str):
    return McpServer(
        url=f"{host}/api/2.0/mcp/functions/system/ai",
        name="system.ai uc function mcp server",
    )
```

### Using MCP Server with Context Manager

```python
async with await init_mcp_server() as mcp_server:
    agent = create_agent(mcp_server)
    result = await Runner.run(agent, messages)
```

## Agent Creation

### Basic Agent

```python
from agents import Agent

def create_agent(mcp_server: McpServer) -> Agent:
    return Agent(
        name="my-agent",
        instructions="You are a helpful assistant.",
        model="databricks-claude-3-7-sonnet",
        mcp_servers=[mcp_server],
    )
```

### Agent with Custom Instructions

```python
def create_coding_agent(mcp_server: McpServer) -> Agent:
    return Agent(
        name="code execution agent",
        instructions="""You are a code execution agent.
        You can execute Python code and return the results.
        Always explain your code before executing it.""",
        model="databricks-claude-3-7-sonnet",
        mcp_servers=[mcp_server],
    )
```

## Running Agents

### Non-Streaming

```python
from agents import Runner

async with await init_mcp_server() as mcp_server:
    agent = create_agent(mcp_server)
    messages = [{"role": "user", "content": "Hello"}]
    result = await Runner.run(agent, messages)
    # Access result.new_items for output
```

### Streaming

```python
from agents import Runner

async with await init_mcp_server() as mcp_server:
    agent = create_agent(mcp_server)
    messages = [{"role": "user", "content": "Hello"}]
    result = Runner.run_streamed(agent, input=messages)

    async for event in result.stream_events():
        # Process stream events
        pass
```

## Stream Event Processing

```python
from typing import AsyncGenerator, AsyncIterator
from uuid import uuid4
from agents.result import StreamEvent
from mlflow.types.responses import ResponsesAgentStreamEvent

async def process_agent_stream_events(
    async_stream: AsyncIterator[StreamEvent],
) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    curr_item_id = str(uuid4())

    async for event in async_stream:
        if event.type == "raw_response_event":
            event_data = event.data.model_dump()

            if event_data["type"] == "response.output_item.added":
                curr_item_id = str(uuid4())
                event_data["item"]["id"] = curr_item_id
            elif event_data.get("item") is not None and event_data["item"].get("id") is not None:
                event_data["item"]["id"] = curr_item_id
            elif event_data.get("item_id") is not None:
                event_data["item_id"] = curr_item_id

            yield event_data

        elif event.type == "run_item_stream_event" and event.item.type == "tool_call_output_item":
            yield ResponsesAgentStreamEvent(
                type="response.output_item.done",
                item=event.item.to_input_item(),
            )
```

## MLflow Integration

### Decorators

```python
from mlflow.genai.agent_server import invoke, stream
from mlflow.types.responses import (
    ResponsesAgentRequest,
    ResponsesAgentResponse,
    ResponsesAgentStreamEvent,
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

## Utility Functions

### Get Databricks Host

```python
from databricks.sdk import WorkspaceClient

def get_databricks_host_from_env():
    try:
        w = WorkspaceClient()
        return w.config.host
    except Exception:
        return None
```

### Get User Workspace Client (OBO Auth)

```python
from databricks.sdk import WorkspaceClient
from mlflow.genai.agent_server import get_request_headers

def get_user_workspace_client() -> WorkspaceClient:
    token = get_request_headers().get("x-forwarded-access-token")
    return WorkspaceClient(token=token, auth_type="pat")
```

## Complete Agent Example

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

# Setup
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
        name="assistant",
        instructions="You are a helpful assistant.",
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

## Comparison with LangGraph

| Aspect | OpenAI Agents SDK | LangGraph |
|--------|-------------------|-----------|
| Complexity | Simple, direct | Graph-based, flexible |
| MCP | `McpServer` in Agent | `DatabricksMultiServerMCPClient` |
| Execution | `Runner.run()` | `agent.astream()` |
| State | Built-in | Full state machine |
| Best For | Simple agents | Complex workflows |

## When to Use OpenAI Agents SDK

- Simple conversational agents
- MCP is the primary tool source
- Minimal custom orchestration needed
- Direct OpenAI SDK familiarity

## Additional Resources

- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents-sdk
- databricks-openai SDK: https://github.com/databricks/databricks-ai-bridge/tree/main/integrations/openai
- Databricks Agent Framework: https://docs.databricks.com/aws/en/generative-ai/agent-framework/
