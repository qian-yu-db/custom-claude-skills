# Worker Agent Implementations

## Genie Agent Integration

```python
from genie_client import GenieClient, format_as_markdown_table

genie_client = GenieClient()

def query_genie_agent(space_id: str, query: str) -> str:
    """Execute query against Genie space."""
    try:
        message = genie_client.start_conversation(space_id, query)
        data = genie_client.extract_data(message)
        table = format_as_markdown_table(data)

        summary_prompt = f"""Summarize these results:\n{table}\nSummary:"""
        summary = llm.invoke(summary_prompt).content
        return f"{summary}\n\n**Detailed Results:**\n{table}"
    except Exception as e:
        return f"Genie agent error: {str(e)}"
```

## RAG Agent Integration

```python
from vector_search_retriever import create_retriever

def query_rag_agent(index_name: str, query: str) -> str:
    """Execute RAG query against Vector Search index."""
    try:
        retriever = create_retriever(
            index_name=index_name,
            endpoint_name=os.getenv("VS_ENDPOINT"),
            num_results=5
        )
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([
            f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])

        rag_prompt = f"""Answer using these documents:\nContext:\n{context}\nQuestion: {query}\nAnswer:"""
        return llm.invoke(rag_prompt).content
    except Exception as e:
        return f"RAG agent error: {str(e)}"
```

## MCP Tool Agent Integration

```python
def query_mcp_agent(tools: list, query: str) -> str:
    """Execute query using MCP tools."""
    try:
        tool_instances = [get_tool(tool_name) for tool_name in tools]
        llm_with_tools = llm.bind_tools(tool_instances)
        response = llm_with_tools.invoke(query)

        if hasattr(response, "tool_calls") and response.tool_calls:
            results = []
            for tool_call in response.tool_calls:
                tool_result = execute_tool(tool_call)
                results.append(tool_result)
            return "\n".join(results)
        else:
            return response.content
    except Exception as e:
        return f"MCP agent error: {str(e)}"
```

## Configuration-Driven Agent Creation

```json
{
  "agents": {
    "sales_agent": {
      "type": "genie",
      "description": "Sales data, revenue, customer analytics",
      "config": { "space_id": "sales_space_123" }
    },
    "docs_agent": {
      "type": "rag",
      "description": "Technical documentation and guides",
      "config": { "index_name": "catalog.schema.docs_index", "endpoint_name": "my_endpoint" }
    },
    "support_agent": {
      "type": "mcp",
      "description": "Customer support and ticketing",
      "config": { "tools": ["get_ticket", "create_ticket", "update_ticket"] }
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

```python
import json

def load_agent_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return json.load(f)

def create_agents_from_config(config: dict) -> dict:
    agents = {}
    for agent_name, agent_spec in config["agents"].items():
        agent_type = agent_spec["type"]
        agent_config = agent_spec["config"]
        if agent_type == "genie":
            agent_fn = lambda state, cfg=agent_config: query_genie_agent(cfg["space_id"], state["messages"][-1].content)
        elif agent_type == "rag":
            agent_fn = lambda state, cfg=agent_config: query_rag_agent(cfg["index_name"], state["messages"][-1].content)
        elif agent_type == "mcp":
            agent_fn = lambda state, cfg=agent_config: query_mcp_agent(cfg["tools"], state["messages"][-1].content)
        else:
            agent_fn = lambda state: "Unknown agent type"
        agents[agent_name] = agent_fn
    return agents
```
