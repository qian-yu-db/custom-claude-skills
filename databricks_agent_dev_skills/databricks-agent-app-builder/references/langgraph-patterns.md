# LangGraph Agent Patterns

Reference for building agents with LangGraph on Databricks.

## Core Dependencies

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

## LLM Configuration

### ChatDatabricks

```python
from databricks_langchain import ChatDatabricks

# Basic usage
llm = ChatDatabricks(
    endpoint="databricks-claude-3-7-sonnet",  # or databricks-meta-llama-3-1-70b-instruct
    temperature=0,
    max_tokens=500,
)

# For Responses API agents
llm = ChatDatabricks(endpoint="my-agent-endpoint", use_responses_api=True)
```

## MCP Integration

### DatabricksMultiServerMCPClient

```python
from databricks_langchain import DatabricksMCPServer, DatabricksMultiServerMCPClient

def init_mcp_client(host: str) -> DatabricksMultiServerMCPClient:
    return DatabricksMultiServerMCPClient([
        DatabricksMCPServer(
            name="system-ai",
            url=f"{host}/api/2.0/mcp/functions/system/ai",
        ),
    ])

# Get tools
mcp_client = init_mcp_client(host)
tools = await mcp_client.get_tools()
```

### Unity Catalog Functions

```python
# Expose a specific function
server = DatabricksMCPServer.from_uc_function(
    catalog="main",
    schema="tools",
    function_name="send_email",
    name="email-server",
    timeout=30.0,
    handle_tool_error=True,
)

# Expose all functions in schema
server = DatabricksMCPServer.from_uc_function(
    catalog="main",
    schema="tools",
    name="tools-server",
)
```

### Vector Search

```python
# Expose a specific index
server = DatabricksMCPServer.from_vector_search(
    catalog="main",
    schema="embeddings",
    index_name="product_docs",
    name="docs-search",
    timeout=30.0,
)

# Expose all indexes in schema
server = DatabricksMCPServer.from_vector_search(
    catalog="main",
    schema="embeddings",
    name="embeddings-server",
)
```

### Genie Space

```python
# Get genie_space_id from UI URL:
# https://workspace.databricks.com/genie/rooms/01f0515f...?o=12345
# genie_space_id = "01f0515f..."

server = DatabricksMCPServer(
    name="genie",
    url=f"{host}/api/2.0/mcp/genie/{genie_space_id}",
)
```

### External MCP Server

```python
from databricks_langchain import MCPServer

server = MCPServer(
    name="external-server",
    url="https://other-server.com/mcp",
    headers={"X-API-Key": "secret"},
    timeout=15.0,
)
```

## Agent Creation

### Using create_agent

```python
from langchain.agents import create_agent
from databricks_langchain import ChatDatabricks

async def init_agent():
    mcp_client = init_mcp_client(host)
    tools = await mcp_client.get_tools()

    return create_agent(
        tools=tools,
        model=ChatDatabricks(endpoint="databricks-claude-3-7-sonnet")
    )
```

## Streaming Implementation

### Process Agent Stream Events

```python
from typing import AsyncGenerator, AsyncIterator, Any
from langchain.messages import AIMessageChunk, ToolMessage
from databricks_langchain.chat_models import json
from mlflow.types.responses import (
    ResponsesAgentStreamEvent,
    create_text_delta,
    output_to_responses_items_stream,
)

async def process_agent_astream_events(
    async_stream: AsyncIterator[Any],
) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    async for event in async_stream:
        if event[0] == "updates":
            for node_data in event[1].values():
                if len(node_data.get("messages", [])) > 0:
                    for msg in node_data["messages"]:
                        if isinstance(msg, ToolMessage) and not isinstance(msg.content, str):
                            msg.content = json.dumps(msg.content)
                    for item in output_to_responses_items_stream(node_data["messages"]):
                        yield item
        elif event[0] == "messages":
            chunk = event[1][0]
            if isinstance(chunk, AIMessageChunk) and (content := chunk.content):
                yield ResponsesAgentStreamEvent(
                    **create_text_delta(delta=content, item_id=chunk.id)
                )
```

### Stream Agent

```python
from mlflow.types.responses import to_chat_completions_input

@stream()
async def streaming(request: ResponsesAgentRequest) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    agent = await init_agent()
    messages = {"messages": to_chat_completions_input([i.model_dump() for i in request.input])}

    async for event in process_agent_astream_events(
        agent.astream(input=messages, stream_mode=["updates", "messages"])
    ):
        yield event
```

## Stateful Agents

### Using Lakebase for State

```bash
# Install memory support
uv add "databricks-langchain[memory]"
```

```python
# Add to .env.local
LAKEBASE_INSTANCE_NAME=<your-lakebase-name>
```

Check `databricks_langchain/checkpoints.py` and `databricks_langchain/store.py` for implementation details.

## Embeddings

```python
from databricks_langchain import DatabricksEmbeddings

embeddings = DatabricksEmbeddings(endpoint="databricks-bge-large-en")
vector = embeddings.embed_query("The meaning of life is 42")
vectors = embeddings.embed_documents(["doc1", "doc2"])
```

## Vector Search

```python
from databricks_langchain import DatabricksVectorSearch

# Delta-sync index with Databricks-managed embeddings
vs = DatabricksVectorSearch(index_name="catalog.schema.index_name")

# Direct-access or self-managed embeddings
vs = DatabricksVectorSearch(
    index_name="catalog.schema.index_name",
    embedding=embeddings,
    text_column="content",
)

docs = vs.similarity_search("query", k=5)
```

## Complete Agent Example

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

mlflow.langchain.autolog()
sp_workspace_client = WorkspaceClient()

def get_databricks_host():
    return WorkspaceClient().config.host

def init_mcp_client():
    host = get_databricks_host()
    return DatabricksMultiServerMCPClient([
        DatabricksMCPServer(name="system-ai", url=f"{host}/api/2.0/mcp/functions/system/ai"),
    ])

async def init_agent():
    mcp_client = init_mcp_client()
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

## Additional Resources

- LangGraph documentation: https://docs.langchain.com/oss/python/langgraph/overview
- Databricks Agent Framework: https://docs.databricks.com/aws/en/generative-ai/agent-framework/
- Agent Tools: https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-tool
- databricks-langchain SDK: https://github.com/databricks/databricks-ai-bridge/tree/main/integrations/langchain
