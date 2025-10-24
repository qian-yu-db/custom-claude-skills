# LangGraph Genie Agent - Quick Reference

## Common Claude Prompts

### Create Agent
```
"Create a LangGraph agent that queries Genie space abc123"
"Build a multi-agent system with Genie for sales and finance"
"Set up a conversational agent with Genie integration"
```

### Architecture Help
```
"Show me the supervisor pattern with Genie agents"
"How do I maintain conversation context with Genie?"
"Create an agent that routes to different Genie spaces"
```

## Genie API Quick Reference

### Start Conversation
```python
POST /api/2.0/genie/spaces/{space_id}/start-conversation

# Request
{"content": "What were Q4 sales?"}

# Response
{
  "conversation_id": "01ef...",
  "message_id": "01ef...",
  "status": "EXECUTING_QUERY"
}
```

### Continue Conversation
```python
POST /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages

# Request
{"content": "What about Q3?"}
```

### Get Message Status
```python
GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}

# Response when complete
{
  "status": "COMPLETED",
  "query_result": {
    "statement_response": {
      "result": {"data_array": [...]}
    }
  }
}
```

## GenieClient Usage

### Initialize
```python
from genie_client import GenieClient

client = GenieClient(
    host="https://workspace.cloud.databricks.com",
    token="dapi...",
    timeout=60
)
```

### Query Space
```python
# Start new conversation
message = client.start_conversation(
    space_id="abc123",
    content="Show top 10 customers by revenue"
)

# Continue conversation
follow_up = client.continue_conversation(
    space_id="abc123",
    conversation_id=conv_id,
    content="What about last quarter?"
)
```

### Extract Data
```python
# Get structured data
data = client.extract_data(message)
# Returns: {
#   "columns": ["customer_name", "revenue"],
#   "data": [{"customer_name": "Acme", "revenue": 50000}, ...],
#   "row_count": 10
# }

# Format as markdown table
from genie_client import format_as_markdown_table
table = format_as_markdown_table(data)
```

### Get History
```python
messages = client.get_conversation_history(
    space_id="abc123",
    conversation_id=conv_id
)
```

## LangGraph Patterns

### Simple Agent
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    genie_space_id: str

def query_node(state):
    message = genie_client.start_conversation(
        state["genie_space_id"],
        state["messages"][-1].content
    )
    data = genie_client.extract_data(message)
    return {"messages": [AIMessage(content=format_data(data))]}

graph = StateGraph(AgentState)
graph.add_node("query", query_node)
graph.set_entry_point("query")
graph.add_edge("query", END)
agent = graph.compile()
```

### Multi-Agent Supervisor
```python
class SupervisorState(TypedDict):
    messages: Sequence[BaseMessage]
    next_agent: str

def supervisor_node(state):
    # Route to appropriate agent
    query = state["messages"][-1].content
    agent = determine_agent(query)  # LLM call
    return {"next_agent": agent}

def sales_agent_node(state):
    # Query sales Genie space
    return query_genie("sales_space_123", state)

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("sales_agent", sales_agent_node)
graph.add_node("finance_agent", finance_agent_node)

graph.add_conditional_edges(
    "supervisor",
    lambda s: s["next_agent"],
    {"sales": "sales_agent", "finance": "finance_agent"}
)
```

### Conversational Agent
```python
class ConversationalState(TypedDict):
    messages: Sequence[BaseMessage]
    conversation_id: Optional[str]

def conversational_node(state):
    query = state["messages"][-1].content
    conv_id = state.get("conversation_id")

    if conv_id:
        message = genie_client.continue_conversation(
            "space_123", conv_id, query
        )
    else:
        message = genie_client.start_conversation(
            "space_123", query
        )
        conv_id = extract_conv_id(message)

    return {
        "conversation_id": conv_id,
        "messages": [AIMessage(content=format_response(message))]
    }
```

## Environment Setup

### Required Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"

# Optional: Specific space IDs
export GENIE_SALES_SPACE="space_123"
export GENIE_FINANCE_SPACE="space_456"
```

### Install Dependencies
```bash
uv add langgraph langchain-core databricks-langchain mlflow requests
```

## Script Usage

### Create Agent
```bash
# Single agent
python scripts/create_genie_agent.py my_agent \
  --type single \
  --space-id abc123 \
  -o ./agents

# Multi-agent
python scripts/create_genie_agent.py my_multi_agent \
  --type multi \
  --spaces spaces_config.json \
  -o ./agents
```

### Test Genie Connection
```bash
python scripts/genie_client.py <space_id> "What were Q4 sales?"
```

## Common Patterns

### Query with Retry
```python
def query_with_retry(space_id, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.start_conversation(space_id, query)
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Cache Results
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(space_id: str, query: str):
    return client.start_conversation(space_id, query)
```

### Format Response
```python
def format_for_user(genie_data):
    table = format_as_markdown_table(genie_data)

    summary = llm.invoke(f"Summarize: {genie_data}")

    return f"{summary}\n\n{table}"
```

## MLflow Integration

### Enable Tracing
```python
import mlflow

mlflow.langchain.autolog()

with mlflow.start_run():
    result = agent.invoke(initial_state)

    mlflow.log_param("space_id", space_id)
    mlflow.log_metric("query_time", elapsed)
```

### Log Conversation
```python
with mlflow.start_run():
    for turn in conversation:
        result = agent.invoke(turn)
        mlflow.log_metric("turn", turn_number)
```

## Error Handling

### Handle Timeouts
```python
try:
    message = client.start_conversation(space_id, query)
except TimeoutError:
    # Retry or return cached result
    message = handle_timeout(space_id, query)
```

### Handle Failed Queries
```python
if message.status == "FAILED":
    error = message.error or "Unknown error"
    return AIMessage(content=f"Query failed: {error}")
```

### Handle API Errors
```python
try:
    message = client.start_conversation(space_id, query)
except requests.HTTPError as e:
    if e.response.status_code == 404:
        return "Genie space not found"
    elif e.response.status_code == 401:
        return "Authentication failed"
    else:
        raise
```

## Configuration Files

### spaces_config.json (Multi-Agent)
```json
{
  "sales_agent": {
    "space_id": "sales_space_123",
    "description": "Sales data, revenue, customers"
  },
  "finance_agent": {
    "space_id": "finance_space_456",
    "description": "Financial metrics, budgets, forecasts"
  },
  "inventory_agent": {
    "space_id": "inventory_space_789",
    "description": "Inventory levels, stock management"
  }
}
```

### agent_config.yaml
```yaml
databricks:
  host: ${DATABRICKS_HOST}
  token: ${DATABRICKS_TOKEN}

genie:
  default_space: ${GENIE_SPACE_ID}
  timeout: 60
  max_retries: 3

llm:
  endpoint: ${DATABRICKS_LLM_ENDPOINT}
  temperature: 0.1
  max_tokens: 2000

agent:
  enable_tracing: true
  cache_results: true
  max_conversation_turns: 10
```

## Troubleshooting

### Timeout Issues
```python
# Increase timeout
client = GenieClient(timeout=120)

# Or poll manually
message = client.start_conversation(space_id, query, wait_for_completion=False)
while message.status != "COMPLETED":
    time.sleep(5)
    message = client.get_message(space_id, conv_id, msg_id)
```

### No Results
```python
data = client.extract_data(message)
if data.get("row_count", 0) == 0:
    return "No results found for your query"
```

### Authentication Errors
```bash
# Verify token
echo $DATABRICKS_TOKEN

# Test connection
curl -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  $DATABRICKS_HOST/api/2.0/genie/spaces
```

## Best Practices

1. **Always use conversation IDs** for follow-up questions
2. **Cache Genie results** to avoid redundant queries
3. **Handle timeouts gracefully** with retries
4. **Enable MLflow tracing** for debugging
5. **Format results** as markdown tables
6. **Validate space IDs** before querying
7. **Use supervisor pattern** for multiple spaces
8. **Include error messages** in responses

## Resources

- Genie API: https://docs.databricks.com/genie/conversation-api.html
- LangGraph: https://langchain-ai.github.io/langgraph/
- MLflow: https://mlflow.org/docs/latest/index.html
