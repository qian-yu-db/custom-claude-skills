# LangGraph Multi-Agent Supervisor - Quick Reference

## Common Claude Prompts

### Create Supervisor
```
"Create a multi-agent supervisor with Genie and RAG agents"
"Build a supervisor that routes to sales, docs, and support agents"
"Set up agent orchestration with LLM-based routing"
```

### Architecture Help
```
"Show me the hierarchical supervisor pattern"
"How do I create a sequential multi-agent workflow?"
"Build a supervisor with parallel agent execution"
```

## Supervisor Orchestrator Usage

### Basic Setup
```python
from supervisor_orchestrator import SupervisorOrchestrator, AgentConfig

# Define agents
agents = {
    "sales_agent": AgentConfig(
        name="sales_agent",
        type="genie",
        description="Sales data, revenue, customer analytics",
        config={"space_id": "sales_space_123"}
    ),
    "docs_agent": AgentConfig(
        name="docs_agent",
        type="rag",
        description="Technical documentation and guides",
        config={
            "index_name": "catalog.schema.docs_index",
            "endpoint_name": "my_endpoint"
        }
    )
}

# Create orchestrator
orchestrator = SupervisorOrchestrator(
    agents=agents,
    routing_strategy="llm",
    enable_fallback=True,
    verbose=True
)
```

### Register Executors
```python
from supervisor_orchestrator import (
    genie_agent_executor,
    rag_agent_executor,
    llm_agent_executor
)

# Register built-in executors
orchestrator.register_agent_executor("sales_agent", genie_agent_executor)
orchestrator.register_agent_executor("docs_agent", rag_agent_executor)

# Or register custom executor
def custom_executor(config, query):
    # Your logic here
    return result

orchestrator.register_agent_executor("custom_agent", custom_executor)
```

### Build and Execute
```python
# Build graph
orchestrator.build()

# Execute query
result = orchestrator.invoke("What were Q4 sales?")

# Access results
print(result["final_response"])
print(f"Routed to: {result['next_agent']}")
```

## Configuration File Format

### agents_config.json
```json
{
  "agents": {
    "sales_agent": {
      "type": "genie",
      "description": "Sales data, revenue, customer analytics",
      "config": {
        "space_id": "sales_space_123"
      },
      "enabled": true
    },
    "docs_agent": {
      "type": "rag",
      "description": "Technical documentation and guides",
      "config": {
        "index_name": "catalog.schema.docs_index",
        "endpoint_name": "my_endpoint",
        "num_results": 5
      },
      "enabled": true
    },
    "support_agent": {
      "type": "custom",
      "description": "Customer support and ticketing",
      "config": {
        "api_endpoint": "https://support.example.com/api"
      },
      "enabled": true
    },
    "general_agent": {
      "type": "llm",
      "description": "General questions and conversation",
      "config": {
        "model": "databricks-meta-llama-3-1-70b-instruct",
        "temperature": 0.1
      },
      "enabled": true
    }
  },
  "supervisor": {
    "routing_strategy": "llm",
    "enable_fallback": true,
    "default_agent": "general_agent",
    "max_iterations": 10
  }
}
```

### From Config File
```python
orchestrator = SupervisorOrchestrator.from_config_file(
    "agents_config.json",
    verbose=True
)
```

## Supervisor Patterns

### Pattern 1: Simple Supervisor
```python
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    final_response: str

def supervisor_node(state):
    query = state["messages"][-1].content

    # LLM-based routing
    agent_list = "\n".join([f"- {name}: {desc}" for name, desc in agents.items()])

    routing_prompt = f"""Select agent for query: {query}

Available agents:
{agent_list}

Agent name only:"""

    response = llm.invoke(routing_prompt)
    return {"next_agent": response.content.strip()}

def worker_node(agent_name):
    def node(state):
        query = state["messages"][-1].content
        result = execute_agent(agent_name, query)
        return {
            "messages": [AIMessage(content=result)],
            "final_response": result
        }
    return node

# Build graph
graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)

for agent_name in agents.keys():
    graph.add_node(agent_name, worker_node(agent_name))
    graph.add_edge(agent_name, END)

graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", lambda s: s["next_agent"], agents)
agent = graph.compile()
```

### Pattern 2: Sequential Execution
```python
class SequentialState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agent_sequence: list
    current_index: int
    agent_results: dict

def planner_node(state):
    # Plan agent sequence
    sequence = plan_agents(state["messages"][-1].content)
    return {"agent_sequence": sequence, "current_index": 0}

def execute_node(state):
    idx = state["current_index"]
    agent = state["agent_sequence"][idx]

    result = execute_agent(agent, state["messages"][-1].content)
    results = state["agent_results"]
    results[agent] = result

    return {
        "agent_results": results,
        "current_index": idx + 1
    }

def should_continue(state):
    return "execute" if state["current_index"] < len(state["agent_sequence"]) else "finalize"

graph = StateGraph(SequentialState)
graph.add_node("planner", planner_node)
graph.add_node("execute", execute_node)
graph.add_node("finalize", finalize_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "execute")
graph.add_conditional_edges("execute", should_continue, {
    "execute": "execute",
    "finalize": "finalize"
})
agent = graph.compile()
```

### Pattern 3: Parallel Execution
```python
class ParallelState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agents_to_execute: list
    agent_results: dict

def dispatcher_node(state):
    # Select agents to run in parallel
    agents = select_agents(state["messages"][-1].content)
    return {"agents_to_execute": agents}

def parallel_executor_node(state):
    import concurrent.futures

    agents = state["agents_to_execute"]
    query = state["messages"][-1].content

    def run_agent(agent_name):
        return agent_name, execute_agent(agent_name, query)

    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_agent, a) for a in agents]
        for future in concurrent.futures.as_completed(futures):
            name, result = future.result()
            results[name] = result

    return {"agent_results": results}

graph = StateGraph(ParallelState)
graph.add_node("dispatcher", dispatcher_node)
graph.add_node("executor", parallel_executor_node)
graph.add_node("aggregator", aggregator_node)

graph.set_entry_point("dispatcher")
graph.add_edge("dispatcher", "executor")
graph.add_edge("executor", "aggregator")
agent = graph.compile()
```

## Built-in Agent Executors

### Genie Agent
```python
from supervisor_orchestrator import genie_agent_executor

config = {"space_id": "sales_space_123"}
result = genie_agent_executor(config, "What were Q4 sales?")
```

### RAG Agent
```python
from supervisor_orchestrator import rag_agent_executor

config = {
    "index_name": "catalog.schema.docs_index",
    "endpoint_name": "my_endpoint",
    "num_results": 5
}
result = rag_agent_executor(config, "How do I create a dashboard?")
```

### LLM Agent
```python
from supervisor_orchestrator import llm_agent_executor

config = {
    "model": "databricks-meta-llama-3-1-70b-instruct",
    "temperature": 0.1,
    "system_message": "You are a helpful assistant."
}
result = llm_agent_executor(config, "What is machine learning?")
```

### Custom Agent
```python
def my_custom_executor(config: dict, query: str) -> str:
    api_endpoint = config["api_endpoint"]

    # Your custom logic
    response = call_api(api_endpoint, query)
    return format_response(response)

orchestrator.register_agent_executor("my_agent", my_custom_executor)
```

## Script Usage

### Generate Supervisor
```bash
# From agent definitions
python scripts/create_supervisor.py my_supervisor \
  --config example_agents.json \
  --routing llm \
  -o ./supervisors

# Creates:
#   supervisors/my_supervisor.py
#   supervisors/my_supervisor_config.json
#   supervisors/custom_executors.py (if custom agents)
```

### Run Supervisor
```bash
# With configuration file
python scripts/supervisor_orchestrator.py \
  agents_config.json \
  "What were Q4 sales?"

# With generated supervisor
python supervisors/my_supervisor.py "What were Q4 sales?"
```

## Routing Strategies

### LLM-Based Routing
```python
routing_strategy="llm"

# Pros:
# - Understands semantic meaning
# - Flexible and adaptable
# - Handles complex queries

# Cons:
# - Slower (LLM call for routing)
# - Requires good agent descriptions
```

### Rule-Based Routing
```python
routing_strategy="rules"

# Agents have keywords
config["agents"]["sales_agent"]["config"]["keywords"] = [
    "sales", "revenue", "customers"
]

# Pros:
# - Fast (keyword matching)
# - Deterministic
# - No LLM call needed

# Cons:
# - Less flexible
# - Requires careful keyword selection
```

## Agent Definitions Format

### For create_supervisor.py
```json
{
  "agents": [
    {
      "name": "agent_name",
      "type": "genie|rag|mcp|llm|custom",
      "description": "What this agent does",
      "config": {
        "agent-specific": "configuration"
      },
      "keywords": ["optional", "for", "rules"],
      "enabled": true
    }
  ]
}
```

## MLflow Integration

### Enable Tracing
```python
import mlflow

mlflow.langchain.autolog()

with mlflow.start_run():
    result = orchestrator.invoke(query)

    mlflow.log_param("selected_agent", result["next_agent"])
    mlflow.log_metric("response_length", len(result["final_response"]))
```

## Advanced Features

### Fallback Handling
```python
orchestrator = SupervisorOrchestrator(
    agents=agents,
    enable_fallback=True,
    default_agent="general_agent"
)

# If primary agent fails, falls back to default
```

### Agent Health Checks
```python
def health_check_wrapper(executor_fn):
    def wrapper(config, query):
        if not is_healthy(config):
            raise RuntimeError("Agent unhealthy")
        return executor_fn(config, query)
    return wrapper

orchestrator.register_agent_executor(
    "my_agent",
    health_check_wrapper(my_executor)
)
```

### Result Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_executor(agent_name: str, query: str) -> str:
    config = get_agent_config(agent_name)
    executor = get_executor(agent_name)
    return executor(config, query)
```

### Custom State Management
```python
class CustomState(SupervisorState):
    conversation_history: list
    user_preferences: dict
    context: dict

orchestrator = SupervisorOrchestrator(
    agents=agents,
    state_class=CustomState
)
```

## Environment Setup

### Required Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
```

### Optional Variables
```bash
export VS_ENDPOINT="my_vector_search_endpoint"
export GENIE_TIMEOUT="60"
export DEFAULT_NUM_RESULTS="5"
```

### Install Dependencies
```bash
uv add langgraph langchain-core databricks-langchain mlflow
```

## Common Patterns

### Add New Agent at Runtime
```python
# Add new agent
new_agent = AgentConfig(
    name="new_agent",
    type="custom",
    description="New functionality",
    config={"key": "value"}
)

orchestrator.agents["new_agent"] = new_agent
orchestrator.register_agent_executor("new_agent", new_executor)

# Rebuild graph
orchestrator.build()
```

### Conditional Routing
```python
def smart_routing(state):
    query = state["messages"][-1].content

    # Check query complexity
    if is_complex(query):
        return "expert_agent"
    elif is_simple(query):
        return "general_agent"
    else:
        return "llm_routing"  # Fall back to LLM
```

### Multi-Turn Conversations
```python
conversation_history = []

for user_input in conversation:
    conversation_history.append(HumanMessage(content=user_input))

    result = orchestrator.invoke(
        user_input,
        conversation_history=conversation_history
    )

    conversation_history.append(AIMessage(content=result["final_response"]))
```

## Error Handling

### Graceful Degradation
```python
try:
    result = orchestrator.invoke(query)
except Exception as e:
    # Log error
    mlflow.log_param("error", str(e))

    # Fall back to simple LLM
    result = llm.invoke(query)
```

### Agent Timeouts
```python
import signal

def with_timeout(executor_fn, timeout=30):
    def wrapper(config, query):
        def handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)

        try:
            return executor_fn(config, query)
        finally:
            signal.alarm(0)

    return wrapper
```

## Best Practices

1. **Agent Design**:
   - Keep agents focused and specialized
   - Write clear, specific descriptions
   - Test agents independently first

2. **Routing**:
   - Use LLM routing for flexibility
   - Add rule-based fallback for performance
   - Log routing decisions

3. **Error Handling**:
   - Always enable fallback
   - Implement timeouts
   - Log errors to MLflow

4. **Configuration**:
   - Use configuration files
   - Version control configs
   - Separate dev/prod configs

5. **Testing**:
   - Test each agent independently
   - Test routing logic
   - Test error scenarios

## Troubleshooting

### Agent Not Routing
```python
# Enable verbose mode
orchestrator.verbose = True

# Check routing decision
result = orchestrator.invoke(query)
print(f"Selected: {result['next_agent']}")
```

### Agent Execution Fails
```python
# Test executor directly
config = agents["my_agent"].config
result = my_executor(config, "test query")
```

### LLM Routing Incorrect
```python
# Improve agent descriptions
agents["sales_agent"].description = "Handles ALL sales-related queries including revenue, customers, deals, pipeline, and forecasts"

# Add keywords for rule-based fallback
agents["sales_agent"].config["keywords"] = ["sales", "revenue", "customer"]
```

## Resources

- Databricks Multi-Agent: https://docs.databricks.com/generative-ai/agent-framework/multi-agent-genie
- LangGraph Supervisor: https://github.com/langchain-ai/langgraph-supervisor-py
- LangChain Docs: https://docs.langchain.com/oss/python/langchain/supervisor
