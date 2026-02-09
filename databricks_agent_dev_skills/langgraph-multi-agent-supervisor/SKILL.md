---
name: langgraph-multi-agent-supervisor
description: Build LangGraph multi-agent systems with intelligent supervisor orchestration of specialized worker agents (Genie, RAG, MCP, LLM, custom). Use when creating multi-agent systems, implementing supervisor patterns, routing queries to specialized agents, or building hierarchical/sequential/parallel agent workflows.
---

# LangGraph Multi-Agent Supervisor Skill

Build LangGraph multi-agent systems with a supervisor that orchestrates specialized worker agents. The supervisor intelligently routes user queries to the appropriate agent and manages the overall conversation flow.

## Core Architecture

- **Supervisor node**: LLM-powered routing that selects the best worker agent for each query
- **Worker agents**: Specialized agents (Genie, RAG, MCP, custom) that handle domain-specific tasks
- **State management**: Shared state across agents with result aggregation
- **Routing strategies**: LLM-based (semantic), rule-based (keywords), sequential, or parallel

## Supervisor Patterns

Choose the right pattern based on your use case:

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Simple | Single agent selection per query | Easy to implement | No multi-step workflows |
| Hierarchical | Complex domains with sub-domains | Scalable organization | More complex setup |
| Sequential | Multi-step workflows | Results build on each other | Slower execution |
| Parallel | Independent queries needing multiple agents | Faster execution | More complex aggregation |

See [references/patterns.md](references/patterns.md) for complete implementation code for all 4 patterns.

## Worker Agent Types

| Type | Description | Key Config |
|------|-------------|------------|
| Genie | Natural language queries against Databricks Genie spaces | `space_id` |
| RAG | Document retrieval via Vector Search | `index_name`, `endpoint_name` |
| MCP | External tool execution via MCP protocol | `tools` list |
| LLM | General-purpose LLM responses | `model` endpoint |
| Custom | Any custom function | User-defined |

See [references/worker-agents.md](references/worker-agents.md) for implementation code and configuration-driven agent creation.

## Quick Start

### 1. Define State and Workers

```python
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, END
from databricks_langchain import ChatDatabricks

class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    agent_results: dict
    final_response: str

WORKER_AGENTS = {
    "sales_agent": {"description": "Sales data queries", "type": "genie", "space_id": "..."},
    "docs_agent": {"description": "Documentation search", "type": "rag", "index_name": "..."},
}
```

### 2. Build Graph

```python
graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
for name, config in WORKER_AGENTS.items():
    graph.add_node(name, create_worker_node(name, config))
    graph.add_edge(name, END)

graph.set_entry_point("supervisor")
graph.add_conditional_edges("supervisor", route_to_agent, routes)
agent = graph.compile()
```

### 3. Enable MLflow Tracking

```python
import mlflow
mlflow.langchain.autolog()
supervisor = create_supervisor_agent()
```

## Best Practices

1. **Agent design**: Keep agents focused and specialized with clear descriptions for routing
2. **Routing**: Use semantic routing (LLM) for flexibility, add rule-based for known patterns
3. **State**: Keep shared state minimal, use agent-specific state for details
4. **Performance**: Cache results, use parallel execution when possible, implement timeouts
5. **Observability**: Enable MLflow tracing, log routing decisions, track execution time

## References

- [references/patterns.md](references/patterns.md) - Complete implementations of all 4 supervisor patterns
- [references/worker-agents.md](references/worker-agents.md) - Worker agent implementations and config-driven creation
- [examples/example_agents.json](examples/example_agents.json) - Example agent configurations
- Databricks Multi-Agent Framework: https://docs.databricks.com/generative-ai/agent-framework/multi-agent-genie
- LangGraph Supervisor: https://github.com/langchain-ai/langgraph-supervisor-py
