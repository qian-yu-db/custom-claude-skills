# MLflow AgentServer Patterns

Reference for MLflow's GenAI AgentServer used across all agent frameworks.

## AgentServer Setup

### Conversational Agents (LangGraph / OpenAI Agents SDK)

```python
from mlflow.genai.agent_server import AgentServer, setup_mlflow_git_based_version_tracking

# Enable chat proxy for frontend integration
agent_server = AgentServer("ResponsesAgent", enable_chat_proxy=True)

app = agent_server.app  # FastAPI app for additional routes

def main():
    agent_server.run(app_import_string="agent_server.start_server:app")
```

### Non-Conversational Agents

```python
from mlflow.genai.agent_server import AgentServer

# Default agent_type=None for stateless processing
agent_server = AgentServer()

app = agent_server.app

def main():
    agent_server.run(app_import_string="agent_server.start_server:app")
```

## MLflow Decorators

### @invoke() Decorator

Registers a function for non-streaming inference and MLflow evaluation.

```python
from mlflow.genai.agent_server import invoke
from mlflow.types.responses import ResponsesAgentRequest, ResponsesAgentResponse

@invoke()
async def non_streaming(request: ResponsesAgentRequest) -> ResponsesAgentResponse:
    # Process request and return response
    outputs = [...]
    return ResponsesAgentResponse(output=outputs)
```

### @stream() Decorator

Registers a function for streaming inference.

```python
from typing import AsyncGenerator
from mlflow.genai.agent_server import stream
from mlflow.types.responses import ResponsesAgentRequest, ResponsesAgentStreamEvent

@stream()
async def streaming(request: ResponsesAgentRequest) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    # Yield stream events
    async for event in agent_stream:
        yield event
```

## Responses API Types

### Request/Response Types

```python
from mlflow.types.responses import (
    ResponsesAgentRequest,       # Input: list of messages
    ResponsesAgentResponse,      # Output: list of output items
    ResponsesAgentStreamEvent,   # Streaming: individual events
    to_chat_completions_input,   # Convert to chat format
    output_to_responses_items_stream,  # Convert output to stream
    create_text_delta,           # Create text delta event
)
```

### Request Structure

```python
# ResponsesAgentRequest
{
    "input": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "What's 2+2?"}
    ]
}
```

### Response Structure

```python
# ResponsesAgentResponse
{
    "output": [
        {"type": "message", "role": "assistant", "content": "2+2 equals 4"},
        {"type": "function_call", ...}
    ]
}
```

## Git-Based Version Tracking

```python
from mlflow.genai.agent_server import setup_mlflow_git_based_version_tracking

try:
    setup_mlflow_git_based_version_tracking()
except Exception as e:
    logging.warning(f"Git-based version tracking not available: {e}")
```

This tracks agent versions by git commit hash in MLflow.

## Request Headers Access

```python
from mlflow.genai.agent_server import get_request_headers

def get_user_workspace_client():
    # Access forwarded headers from Databricks Apps
    token = get_request_headers().get("x-forwarded-access-token")
    return WorkspaceClient(token=token, auth_type="pat")
```

Available headers in Databricks Apps:
- `x-forwarded-access-token` - User's OAuth token for OBO auth
- `X-Forwarded-User` - User ID
- `X-Forwarded-Email` - User email
- `X-Forwarded-Preferred-Username` - Display name

## Auto-Tracing

### LangGraph

```python
import mlflow
mlflow.langchain.autolog()  # Trace all LangChain/LangGraph calls
```

### OpenAI Agents SDK

```python
import mlflow
from agents.tracing import set_trace_processors

set_trace_processors([])  # Disable built-in tracing, use MLflow only
mlflow.openai.autolog()   # Trace all OpenAI calls
```

## MLflow Evaluation

```python
import mlflow
from mlflow.genai.agent_server import get_invoke_function
from mlflow.genai.scorers import RelevanceToQuery, Safety

# Get the registered @invoke() function
invoke_fn = get_invoke_function()

# Create evaluation dataset
eval_dataset = [
    {
        "inputs": {"request": {"input": [{"role": "user", "content": "..."}]}},
        "expected_response": "...",
    }
]

# Run evaluation
mlflow.genai.evaluate(
    data=eval_dataset,
    predict_fn=invoke_fn,
    scorers=[RelevanceToQuery(), Safety()],
)
```

## Server Configuration

### CLI Options

```bash
uv run start-server                    # Default (port 8000)
uv run start-server --reload           # Hot-reload for development
uv run start-server --port 8001        # Custom port
uv run start-server --workers 4        # Multiple workers
uv run start-server --host 0.0.0.0     # Bind to all interfaces
```

### Environment Variables

```bash
MLFLOW_TRACKING_URI="databricks"       # Required for tracing
MLFLOW_REGISTRY_URI="databricks-uc"    # Unity Catalog registry
MLFLOW_EXPERIMENT_ID=<id>              # Target experiment
```

## Chat Proxy

When `enable_chat_proxy=True`, AgentServer adds:
- `/chat` endpoint for frontend integration
- Automatic request/response format conversion
- Streaming support for real-time UI updates

```yaml
# app.yaml
env:
  - name: API_PROXY
    value: "http://localhost:8000/invocations"
  - name: CHAT_PROXY_TIMEOUT_SECONDS
    value: "300"
```
