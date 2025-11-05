# LangGraph Genie Agent Skill

## Purpose

This skill helps Claude build LangGraph-based tool-calling agents that integrate with Databricks Genie API. It enables creating multi-agent systems where agents can query Genie spaces for data insights, combining the power of LangGraph's orchestration with Genie's natural language data querying.

## When to Activate

This skill should activate when the user requests:
- "Create a LangGraph agent with Genie"
- "Build a multi-agent system using Databricks Genie"
- "Integrate Genie API into my LangGraph workflow"
- "Set up an agent that queries Genie spaces"
- "Create a tool-calling agent with Genie integration"
- "Build a supervisor agent with Genie sub-agents"

## Core Capabilities

### 1. Genie API Integration
- Query Genie spaces via REST API
- Handle conversational context
- Process structured data responses
- Manage API authentication

### 2. LangGraph Agent Architecture
- Build stateful agent graphs
- Implement tool-calling patterns
- Create supervisor-worker architectures
- Handle agent routing and delegation

### 3. Multi-Agent Patterns
- Supervisor agent for routing
- Specialized Genie query agents
- Agent-to-agent communication
- Shared state management

### 4. MLflow Integration
- Trace agent executions
- Log agent interactions
- Deploy agents to Model Serving
- Monitor performance

## Databricks Genie API Overview

### Genie Space Concept

A **Genie Space** is a curated dataset with:
- Natural language interface for querying
- Pre-configured data sources (tables, views)
- Business context and instructions
- SQL generation capabilities

### API Endpoints

#### Start Conversation
```python
POST /api/2.0/genie/spaces/{space_id}/start-conversation
```

**Request:**
```json
{
  "content": "What were the top 5 products by revenue last quarter?"
}
```

**Response:**
```json
{
  "conversation_id": "01ef...",
  "message_id": "01ef...",
  "status": "EXECUTING_QUERY"
}
```

#### Get Message Status
```python
GET /api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}
```

**Response:**
```json
{
  "id": "01ef...",
  "status": "COMPLETED",
  "query_result": {
    "statement_response": {
      "status": {
        "state": "SUCCEEDED"
      },
      "manifest": {
        "schema": {...}
      },
      "result": {
        "data_array": [...]
      }
    }
  }
}
```

### Authentication

Uses Databricks personal access tokens:
```python
headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}
```

## LangGraph Architecture Patterns

### Pattern 1: Single Genie Agent

Simple agent that queries one Genie space:

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated, Sequence
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]
    genie_query: str
    genie_response: dict

def query_genie_node(state: AgentState) -> AgentState:
    """Query Genie space with user question."""
    query = state["messages"][-1].content

    # Call Genie API
    response = genie_client.query(
        space_id="abc123",
        content=query
    )

    return {
        "genie_query": query,
        "genie_response": response,
        "messages": [AIMessage(content=format_genie_response(response))]
    }

# Build graph
graph = StateGraph(AgentState)
graph.add_node("query_genie", query_genie_node)
graph.set_entry_point("query_genie")
graph.add_edge("query_genie", END)

agent = graph.compile()
```

### Pattern 2: Supervisor with Multiple Genie Agents

Multi-agent system with routing:

```python
from langgraph.graph import StateGraph
from langchain_databricks import ChatDatabricks

class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    final_response: str

# Define specialized agents
agents = {
    "sales_agent": {"space_id": "sales_space_123", "description": "Sales data queries"},
    "finance_agent": {"space_id": "finance_space_456", "description": "Financial metrics"},
    "inventory_agent": {"space_id": "inventory_space_789", "description": "Inventory levels"}
}

def supervisor_node(state: SupervisorState) -> SupervisorState:
    """Route to appropriate Genie agent."""
    llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")

    # Determine which agent should handle the query
    routing_prompt = f"""
    Given the user query: {state['messages'][-1].content}

    Available agents:
    {format_agents(agents)}

    Which agent should handle this query? Respond with agent name only.
    """

    response = llm.invoke(routing_prompt)
    next_agent = response.content.strip().lower()

    return {"next_agent": next_agent}

def create_genie_agent_node(agent_name: str, space_id: str):
    """Factory for Genie agent nodes."""
    def agent_node(state: SupervisorState) -> SupervisorState:
        query = state["messages"][-1].content

        # Query specific Genie space
        genie_response = genie_client.query(space_id=space_id, content=query)

        # Format response
        formatted = format_genie_results(genie_response)

        return {
            "messages": [AIMessage(content=formatted)],
            "final_response": formatted
        }

    return agent_node

# Build supervisor graph
graph = StateGraph(SupervisorState)

# Add supervisor
graph.add_node("supervisor", supervisor_node)

# Add specialized Genie agents
for agent_name, config in agents.items():
    node_func = create_genie_agent_node(agent_name, config["space_id"])
    graph.add_node(agent_name, node_func)
    graph.add_edge(agent_name, END)

# Routing logic
def route_to_agent(state: SupervisorState) -> str:
    return state["next_agent"]

graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {name: name for name in agents.keys()}
)

graph.set_entry_point("supervisor")
agent = graph.compile()
```

### Pattern 3: Conversational Genie Agent

Agent that maintains conversation context:

```python
class ConversationalState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_id: str
    conversation_history: list

def conversational_genie_node(state: ConversationalState) -> ConversationalState:
    """Handle multi-turn conversations with Genie."""
    query = state["messages"][-1].content
    conversation_id = state.get("conversation_id")

    if conversation_id:
        # Continue existing conversation
        response = genie_client.continue_conversation(
            space_id="abc123",
            conversation_id=conversation_id,
            content=query
        )
    else:
        # Start new conversation
        response = genie_client.start_conversation(
            space_id="abc123",
            content=query
        )
        conversation_id = response["conversation_id"]

    return {
        "conversation_id": conversation_id,
        "conversation_history": state.get("conversation_history", []) + [response],
        "messages": [AIMessage(content=format_response(response))]
    }
```

## Implementation Guide

### Step 1: Set Up Genie API Client

Create `genie_client.py`:

```python
import requests
import time
from typing import Optional, Dict, Any

class GenieClient:
    """Client for Databricks Genie API."""

    def __init__(self, host: str, token: str):
        self.host = host.rstrip("/")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def start_conversation(self, space_id: str, content: str) -> Dict[str, Any]:
        """Start a new conversation with Genie space."""
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/start-conversation"

        payload = {"content": content}

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()

        # Wait for query to complete
        return self._wait_for_completion(
            space_id=space_id,
            conversation_id=data["conversation_id"],
            message_id=data["message_id"]
        )

    def continue_conversation(
        self,
        space_id: str,
        conversation_id: str,
        content: str
    ) -> Dict[str, Any]:
        """Continue an existing conversation."""
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages"

        payload = {"content": content}

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()

        return self._wait_for_completion(
            space_id=space_id,
            conversation_id=conversation_id,
            message_id=data["id"]
        )

    def _wait_for_completion(
        self,
        space_id: str,
        conversation_id: str,
        message_id: str,
        max_wait: int = 60
    ) -> Dict[str, Any]:
        """Poll for query completion."""
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}"

        start_time = time.time()

        while time.time() - start_time < max_wait:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            status = data.get("status")

            if status == "COMPLETED":
                return data
            elif status == "FAILED":
                raise Exception(f"Genie query failed: {data.get('error')}")

            time.sleep(2)

        raise TimeoutError("Genie query timed out")

    def get_conversation_history(
        self,
        space_id: str,
        conversation_id: str
    ) -> list:
        """Get full conversation history."""
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json().get("messages", [])
```

### Step 2: Create Agent State Schema

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class GenieAgentState(TypedDict):
    """State for Genie-powered agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    genie_space_id: str
    conversation_id: Optional[str]
    query_results: list
    next_action: str
```

### Step 3: Implement Agent Nodes

```python
from langchain_databricks import ChatDatabricks
from langchain_core.messages import HumanMessage, AIMessage

def analyze_query_node(state: GenieAgentState) -> GenieAgentState:
    """Analyze user query and determine if Genie should be called."""
    llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")

    user_query = state["messages"][-1].content

    analysis_prompt = f"""
    Analyze this query: {user_query}

    Does this require querying a data warehouse? Answer YES or NO only.
    """

    response = llm.invoke(analysis_prompt)
    needs_genie = "YES" in response.content.upper()

    return {
        "next_action": "query_genie" if needs_genie else "respond_directly"
    }

def query_genie_node(state: GenieAgentState) -> GenieAgentState:
    """Query Genie space."""
    genie_client = GenieClient(
        host=os.getenv("DATABRICKS_HOST"),
        token=os.getenv("DATABRICKS_TOKEN")
    )

    query = state["messages"][-1].content
    space_id = state["genie_space_id"]
    conversation_id = state.get("conversation_id")

    if conversation_id:
        result = genie_client.continue_conversation(
            space_id=space_id,
            conversation_id=conversation_id,
            content=query
        )
    else:
        result = genie_client.start_conversation(
            space_id=space_id,
            content=query
        )
        conversation_id = result["conversation_id"]

    # Extract results
    query_result = result.get("query_result", {})
    data = extract_data_from_result(query_result)

    return {
        "conversation_id": conversation_id,
        "query_results": state.get("query_results", []) + [data],
        "next_action": "format_response"
    }

def format_response_node(state: GenieAgentState) -> GenieAgentState:
    """Format Genie results into natural language."""
    llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")

    latest_result = state["query_results"][-1]
    user_query = state["messages"][-1].content

    format_prompt = f"""
    User asked: {user_query}

    Query results: {latest_result}

    Provide a natural language response with the key insights.
    """

    response = llm.invoke(format_prompt)

    return {
        "messages": [AIMessage(content=response.content)],
        "next_action": "end"
    }
```

### Step 4: Build the Graph

```python
from langgraph.graph import StateGraph, END

# Create graph
graph = StateGraph(GenieAgentState)

# Add nodes
graph.add_node("analyze_query", analyze_query_node)
graph.add_node("query_genie", query_genie_node)
graph.add_node("format_response", format_response_node)
graph.add_node("respond_directly", respond_directly_node)

# Define routing
def route_after_analysis(state: GenieAgentState) -> str:
    return state["next_action"]

# Add edges
graph.set_entry_point("analyze_query")
graph.add_conditional_edges(
    "analyze_query",
    route_after_analysis,
    {
        "query_genie": "query_genie",
        "respond_directly": "respond_directly"
    }
)
graph.add_edge("query_genie", "format_response")
graph.add_edge("format_response", END)
graph.add_edge("respond_directly", END)

# Compile
agent = graph.compile()
```

### Step 5: Add MLflow Tracing

```python
import mlflow

# Enable tracing
mlflow.langchain.autolog()

# Use agent with tracing
with mlflow.start_run():
    result = agent.invoke({
        "messages": [HumanMessage(content="What were total sales last month?")],
        "genie_space_id": "your_space_id",
        "conversation_id": None,
        "query_results": [],
        "next_action": ""
    })

    # Log results
    mlflow.log_param("genie_space_id", "your_space_id")
    mlflow.log_metric("messages_exchanged", len(result["messages"]))
```

## Helper Functions

### Extract Data from Genie Response

```python
def extract_data_from_result(query_result: dict) -> dict:
    """Extract structured data from Genie query result."""
    try:
        statement_response = query_result.get("statement_response", {})

        # Get schema
        manifest = statement_response.get("manifest", {})
        schema = manifest.get("schema", {})
        columns = [col["name"] for col in schema.get("columns", [])]

        # Get data
        result = statement_response.get("result", {})
        data_array = result.get("data_array", [])

        # Convert to list of dicts
        records = []
        for row in data_array:
            record = dict(zip(columns, row))
            records.append(record)

        return {
            "columns": columns,
            "data": records,
            "row_count": len(records)
        }
    except Exception as e:
        return {"error": str(e), "raw_response": query_result}
```

### Format Response for Display

```python
def format_genie_response(genie_data: dict) -> str:
    """Format Genie data for user display."""
    if "error" in genie_data:
        return f"Error processing query: {genie_data['error']}"

    columns = genie_data.get("columns", [])
    data = genie_data.get("data", [])
    row_count = genie_data.get("row_count", 0)

    if row_count == 0:
        return "No results found."

    # Create markdown table
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []
    for record in data[:10]:  # Limit to first 10 rows
        row = "| " + " | ".join(str(record.get(col, "")) for col in columns) + " |"
        rows.append(row)

    table = "\n".join([header, separator] + rows)

    if row_count > 10:
        table += f"\n\n_Showing 10 of {row_count} rows_"

    return table
```

## Configuration

### Environment Variables

```bash
# Databricks connection
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."

# Genie space IDs
export GENIE_SALES_SPACE="space_id_123"
export GENIE_FINANCE_SPACE="space_id_456"

# LLM endpoint
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
```

### Configuration File

```yaml
# config/genie_agent.yaml
databricks:
  host: ${DATABRICKS_HOST}
  token: ${DATABRICKS_TOKEN}

genie_spaces:
  sales:
    space_id: ${GENIE_SALES_SPACE}
    description: "Sales data, revenue, customer information"
  finance:
    space_id: ${GENIE_FINANCE_SPACE}
    description: "Financial metrics, budgets, forecasts"

llm:
  endpoint: ${DATABRICKS_LLM_ENDPOINT}
  temperature: 0.1
  max_tokens: 2000

agent:
  max_conversation_turns: 10
  genie_timeout: 60
  enable_tracing: true
```

## Best Practices

### 1. Error Handling

```python
def query_genie_with_retry(
    genie_client: GenieClient,
    space_id: str,
    content: str,
    max_retries: int = 3
) -> dict:
    """Query Genie with retry logic."""
    for attempt in range(max_retries):
        try:
            return genie_client.start_conversation(space_id, content)
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

### 2. Conversation Context

Maintain conversation IDs for follow-up questions:

```python
class ConversationManager:
    """Manage Genie conversation contexts."""

    def __init__(self):
        self.conversations = {}

    def get_or_create(self, session_id: str, space_id: str) -> str:
        """Get existing or create new conversation."""
        key = f"{session_id}:{space_id}"
        return self.conversations.get(key)

    def update(self, session_id: str, space_id: str, conversation_id: str):
        """Update conversation mapping."""
        key = f"{session_id}:{space_id}"
        self.conversations[key] = conversation_id
```

### 3. Result Caching

Cache recent Genie results to avoid redundant queries:

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_genie_query(space_id: str, query: str) -> dict:
    """Cache Genie query results."""
    query_hash = hashlib.md5(f"{space_id}:{query}".encode()).hexdigest()
    # Query Genie and cache result
    return genie_client.start_conversation(space_id, query)
```

## Reference Files

The skill includes these reference documents:

- `references/genie-api-guide.md` - Complete Genie API documentation
- `references/langgraph-patterns.md` - LangGraph architecture patterns
- `references/multi-agent-examples.md` - Multi-agent system examples
- `references/deployment-guide.md` - MLflow deployment guide

## Scripts

### scripts/create_genie_agent.py
Generates complete agent implementation from template.

### scripts/test_genie_connection.py
Tests Genie API connectivity and space access.

### scripts/deploy_agent.py
Deploys agent to Databricks Model Serving.

## Tips for Claude

- Always include MLflow tracing for debugging
- Use conversation IDs for multi-turn interactions
- Handle Genie timeouts gracefully
- Format results as markdown tables for readability
- Validate Genie space IDs before querying
- Include error handling for API failures
- Cache conversation contexts per session
- Use supervisor pattern for multiple Genie spaces
