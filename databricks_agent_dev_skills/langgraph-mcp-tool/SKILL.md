---
name: langgraph-mcp-tool
description: Create LangChain-compatible tools from Databricks MCP servers (managed and external) for use in any AI agent framework. Use when connecting to Databricks managed MCP (Vector Search, Genie, UC Functions, DBSQL), integrating external MCP servers, or creating tools from Unity Catalog functions for LangGraph/LangChain agents.
---

# LangGraph MCP Tool Skill

## Purpose

This skill helps create LangChain-compatible tools from Databricks MCP (Model Context Protocol) servers. These tools can be used with any AI agent framework (LangGraph, LangChain, custom agents). The focus is on **tool creation**, not agent implementation.

## When to Activate

This skill should activate when the user requests:
- "Create MCP tools for my agent"
- "Connect to Databricks managed MCP"
- "Get tools from Vector Search MCP"
- "Use Genie Space as tools"
- "Connect to external MCP server as LangChain tools"
- "Set up MCP tools from Unity Catalog functions"

## Prerequisites

- Python 3.12+
- Databricks CLI authenticated (`databricks auth login`)
- Serverless compute enabled in workspace
- Unity Catalog enabled

## Installation

```bash
pip install "databricks-mcp>=0.6.0" "databricks-langchain>=0.13.0" "mcp>=1.9" langchain-mcp-adapters
```

## Core Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `databricks-mcp` | >=0.6.0 | Main Databricks MCP client |
| `databricks-langchain` | >=0.13.0 | LangChain integration |
| `mcp` | >=1.9 | MCP protocol |
| `langchain-mcp-adapters` | latest | External MCP server adapters |

## Key Classes

| Class | Package | Purpose |
|-------|---------|---------|
| `DatabricksMCPClient` | `databricks_mcp` | Connect to single Databricks managed MCP |
| `DatabricksMultiServerMCPClient` | `databricks_mcp` | Connect to multiple Databricks MCP servers |
| `DatabricksMCPServer` | `databricks_mcp` | Server configuration object |
| `MultiServerMCPClient` | `langchain_mcp_adapters` | External MCP server adapter |

## Available Managed MCP Servers

| Server | URL Pattern | Purpose |
|--------|-------------|---------|
| Vector Search | `/api/2.0/mcp/vector-search/{catalog}/{schema}` | Query vector indices |
| Genie Space | `/api/2.0/mcp/genie/{genie_space_id}` | Natural language data analysis |
| UC Functions | `/api/2.0/mcp/functions/{catalog}/{schema}` | Run Unity Catalog functions |
| DBSQL | `/api/2.0/mcp/sql` | AI-generated SQL queries |
| External | `/api/2.0/mcp/external/{connection_name}` | Third-party MCP servers via proxy |

---

## Pattern 1: Single Managed MCP Server

Connect to one Databricks managed MCP server and get LangChain tools.

```python
from databricks_mcp import DatabricksMCPClient

async def get_vector_search_tools():
    """Get tools from Vector Search MCP server."""
    async with DatabricksMCPClient(
        server_url="/api/2.0/mcp/vector-search/my_catalog/my_schema"
    ) as client:
        # Get all tools as LangChain-compatible tools
        tools = await client.get_tools()
        return tools

# Usage
import asyncio
tools = asyncio.run(get_vector_search_tools())
# tools can now be used with any LangChain-compatible agent
```

---

## Pattern 2: Multi-Server MCP Client

Connect to multiple Databricks MCP servers and aggregate tools.

```python
from databricks_mcp import DatabricksMultiServerMCPClient, DatabricksMCPServer

async def get_multi_server_tools():
    """Get tools from multiple MCP servers."""
    servers = [
        DatabricksMCPServer(
            name="vector_search",
            server_url="/api/2.0/mcp/vector-search/catalog/schema"
        ),
        DatabricksMCPServer(
            name="genie",
            server_url="/api/2.0/mcp/genie/my_genie_space_id"
        ),
        DatabricksMCPServer(
            name="uc_functions",
            server_url="/api/2.0/mcp/functions/catalog/schema"
        ),
    ]

    async with DatabricksMultiServerMCPClient(servers=servers) as client:
        # Get all tools from all servers
        tools = await client.get_tools()
        return tools

# Usage
import asyncio
tools = asyncio.run(get_multi_server_tools())
```

---

## Pattern 3: Vector Search with Meta Parameters

Fine-tune Vector Search queries using `_meta` parameters.

```python
from databricks_mcp import DatabricksMCPClient

async def get_vector_search_tools_with_meta():
    """Get Vector Search tools with meta parameter configuration."""
    async with DatabricksMCPClient(
        server_url="/api/2.0/mcp/vector-search/my_catalog/my_schema"
    ) as client:
        tools = await client.get_tools()
        return tools

# When calling the tool, include _meta parameters:
# tool_input = {
#     "query": "machine learning best practices",
#     "_meta": {
#         "num_results": 10,                    # Number of results (default: 5)
#         "filters": {"category": "ML"},        # Filter conditions
#         "query_type": "hybrid",               # "ann" | "hybrid"
#         "score_threshold": 0.7,               # Minimum similarity score
#         "columns": ["title", "content"],      # Columns to return
#     }
# }
```

### Available Meta Parameters for Vector Search

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_results` | int | Number of results to return (default: 5) |
| `filters` | dict | Filter conditions for the query |
| `query_type` | str | "ann" (approximate) or "hybrid" |
| `score_threshold` | float | Minimum similarity score threshold |
| `columns` | list | Specific columns to return |

---

## Pattern 4: External MCP Servers via Proxy

Connect to external MCP servers through Databricks proxy.

```python
from databricks_mcp import DatabricksMCPClient

async def get_external_mcp_tools():
    """Get tools from external MCP server via Databricks proxy."""
    # External servers are accessed via Unity Catalog connections
    async with DatabricksMCPClient(
        server_url="/api/2.0/mcp/external/my_github_connection"
    ) as client:
        tools = await client.get_tools()
        return tools

import asyncio
tools = asyncio.run(get_external_mcp_tools())
```

---

## Pattern 5: External MCP Servers (Direct)

Connect directly to external MCP servers using langchain-mcp-adapters.

```python
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_external_tools_direct():
    """Connect directly to external MCP servers."""
    async with MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
            },
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"],
            },
        }
    ) as client:
        tools = client.get_tools()
        return tools

import asyncio
tools = asyncio.run(get_external_tools_direct())
```

---

## Pattern 6: OAuth Authentication

Use OAuth for authentication instead of PAT tokens.

```python
import os
from databricks_mcp import DatabricksMCPClient
from databricks_mcp.auth import OAuthProvider

async def get_tools_with_oauth():
    """Get MCP tools using OAuth authentication."""
    # OAuth provider handles token refresh automatically
    auth_provider = OAuthProvider(
        client_id=os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
        # Or use service principal authentication
    )

    async with DatabricksMCPClient(
        server_url="/api/2.0/mcp/vector-search/catalog/schema",
        auth_provider=auth_provider
    ) as client:
        tools = await client.get_tools()
        return tools
```

---

## Pattern 7: Get Resources for Deployment

Get Databricks resources required for model serving deployment.

```python
from databricks_mcp import DatabricksMultiServerMCPClient, DatabricksMCPServer

async def get_deployment_resources():
    """Get Databricks resources for deployment configuration."""
    servers = [
        DatabricksMCPServer(
            name="vector_search",
            server_url="/api/2.0/mcp/vector-search/catalog/schema"
        ),
    ]

    async with DatabricksMultiServerMCPClient(servers=servers) as client:
        # Get resources needed for Model Serving deployment
        resources = client.get_databricks_resources()
        # Returns: {"vector_search_indexes": [...], "genie_spaces": [...], etc.}
        return resources
```

### Using Resources in Model Serving

```python
import mlflow
from mlflow.models.resources import DatabricksVectorSearchIndex

# Get resources from MCP client
resources = get_deployment_resources()

# Log model with resources for deployment
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=my_agent,
        resources=[
            DatabricksVectorSearchIndex(index_name=idx)
            for idx in resources.get("vector_search_indexes", [])
        ],
    )
```

---

## Complete Example: Create Tools for Any Agent

```python
"""
Create MCP tools that can be used with any agent framework.
"""
import asyncio
import os
from databricks_mcp import DatabricksMultiServerMCPClient, DatabricksMCPServer


async def create_mcp_tools():
    """Create LangChain-compatible tools from Databricks MCP servers."""

    # Define MCP servers to connect to
    servers = [
        # Vector Search for document retrieval
        DatabricksMCPServer(
            name="docs_search",
            server_url="/api/2.0/mcp/vector-search/main/docs"
        ),
        # Genie Space for data analysis
        DatabricksMCPServer(
            name="analytics",
            server_url="/api/2.0/mcp/genie/my_analytics_space"
        ),
        # UC Functions for custom operations
        DatabricksMCPServer(
            name="custom_functions",
            server_url="/api/2.0/mcp/functions/main/tools"
        ),
    ]

    async with DatabricksMultiServerMCPClient(servers=servers) as client:
        # Get all tools
        tools = await client.get_tools()

        # Get resources for deployment
        resources = client.get_databricks_resources()

        return tools, resources


def main():
    """Main function to create and display tools."""
    tools, resources = asyncio.run(create_mcp_tools())

    print(f"Created {len(tools)} MCP tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:50]}...")

    print(f"\nDatabricks resources for deployment:")
    for resource_type, items in resources.items():
        print(f"  - {resource_type}: {items}")

    # Tools are now ready to use with any agent framework:
    # - LangGraph: graph.add_node("tools", ToolNode(tools))
    # - LangChain: agent = create_react_agent(llm, tools)
    # - Custom: for tool in tools: tool.invoke(input)

    return tools


if __name__ == "__main__":
    main()
```

---

## Best Practices

1. **Use Async Context Managers**: Always use `async with` to ensure proper cleanup
2. **Aggregate Tools Once**: Create tools at startup, not per-request
3. **Include Resources for Deployment**: Use `get_databricks_resources()` when deploying to Model Serving
4. **Use Meta Parameters**: Fine-tune Vector Search with `_meta` for better results
5. **OAuth for Production**: Use OAuth authentication for service principals

## References

- Databricks MCP Documentation: https://docs.databricks.com/aws/en/generative-ai/mcp
- databricks-mcp Package: https://pypi.org/project/databricks-mcp/
- databricks-langchain Package: https://pypi.org/project/databricks-langchain/
- langchain-mcp-adapters: https://pypi.org/project/langchain-mcp-adapters/
- MCP Protocol: https://modelcontextprotocol.io
