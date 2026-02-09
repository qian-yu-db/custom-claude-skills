---
name: langgraph-structured-unstructured-tool
description: Set up Databricks retrieval tools for AI agents using VectorSearchRetrieverTool (unstructured/RAG) and GenieAgent (structured/SQL). Tool configuration only - no agent implementation. Use when setting up Vector Search retrieval tools, creating Genie tools, configuring unstructured/RAG retrieval, setting up structured data tools, adding retrieval tools to agents, or configuring SQL query tools.
---

# LangGraph Structured & Unstructured Tool Skill

## Purpose

Set up retrieval tools for AI agents using official `databricks_langchain` classes. This skill focuses on **TOOL CONFIGURATION**, not agent implementation.

## When to Use

- Setting up Vector Search retrieval for RAG
- Configuring Genie tools for structured data queries
- Combining multiple retrieval tools for agents
- Adding UCFunctionToolkit for governance and tracing

## Prerequisites

- Python 3.10+
- `databricks-langchain>=0.13.0`
- Databricks workspace with Vector Search and/or Genie spaces configured

## Installation

```bash
pip install "databricks-langchain>=0.13.0"
```

Or with uv:
```bash
uv add "databricks-langchain>=0.13.0"
```

## Tool Types Overview

| Tool | Purpose | Data Type |
|------|---------|-----------|
| `VectorSearchRetrieverTool` | Semantic search, RAG | Unstructured (docs, text) |
| `GenieAgent` | SQL queries on tables | Structured (tables, metrics) |
| `UCFunctionToolkit` | Wrap UC functions as tools | Any (with MLflow tracing) |
| `DatabricksFunctionClient` | Create/execute UC functions | Custom |

---

## Pattern 1: VectorSearchRetrieverTool (Basic)

Basic semantic search over a Vector Search index.

```python
from databricks_langchain import VectorSearchRetrieverTool

vs_tool = VectorSearchRetrieverTool(
    index_name="catalog.schema.docs_index",
    name="search_docs",
    description="Search documentation for relevant information about the product",
    num_results=5,
    columns=["text", "source", "title"]
)

# Use as a tool
result = vs_tool.invoke("How do I configure authentication?")
print(result)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `index_name` | str | Full path: `catalog.schema.index_name` |
| `name` | str | Tool name for agent binding |
| `description` | str | Description for LLM tool selection |
| `num_results` | int | Number of results to return (default: 5) |
| `columns` | list[str] | Columns to return from the index |

---

## Pattern 2: VectorSearchRetrieverTool (With Filters)

Add filters and hybrid search for more precise retrieval.

```python
from databricks_langchain import VectorSearchRetrieverTool

# Filtered retrieval
python_docs_tool = VectorSearchRetrieverTool(
    index_name="catalog.schema.docs_index",
    name="search_python_docs",
    description="Search Python-specific documentation",
    num_results=5,
    columns=["text", "source", "title", "language"],
    filters={"language": "python"}
)

# Hybrid search (combines keyword + semantic)
hybrid_tool = VectorSearchRetrieverTool(
    index_name="catalog.schema.docs_index",
    name="hybrid_search",
    description="Search documentation using hybrid retrieval",
    num_results=10,
    query_type="HYBRID"  # Options: "ANN" (default), "HYBRID"
)
```

### Filter Examples

```python
# Single value filter
filters={"category": "api"}

# Multiple values (OR)
filters={"category": ["api", "sdk"]}

# Multiple fields (AND)
filters={"category": "api", "language": "python"}
```

---

## Pattern 3: GenieAgent (Structured Queries)

Query structured data via Databricks Genie spaces.

```python
from databricks_langchain import GenieAgent

genie_tool = GenieAgent(
    genie_space_id="your_genie_space_id",
    genie_agent_name="sales_analyst",
    description="Analyzes sales data, revenue trends, and customer metrics. Use for questions about sales numbers, quarterly reports, and business KPIs.",
    include_context=True
)

# Query structured data
result = genie_tool.invoke("What was total revenue last quarter?")
print(result)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `genie_space_id` | str | ID of the Genie space |
| `genie_agent_name` | str | Name for the tool |
| `description` | str | Description for LLM tool selection |
| `include_context` | bool | Include conversation context (default: True) |

### Finding Genie Space ID

```python
# From the Genie UI URL:
# https://<workspace>.databricks.com/genie/rooms/<SPACE_ID>
genie_space_id = "01xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

---

## Pattern 4: Multiple Genie Spaces

Configure multiple Genie tools for different data domains.

```python
from databricks_langchain import GenieAgent

# Sales data
sales_tool = GenieAgent(
    genie_space_id="sales_space_id",
    genie_agent_name="sales_data",
    description="Query sales metrics, revenue, and customer transactions"
)

# Product data
product_tool = GenieAgent(
    genie_space_id="product_space_id",
    genie_agent_name="product_data",
    description="Query product catalog, inventory, and pricing information"
)

# HR data
hr_tool = GenieAgent(
    genie_space_id="hr_space_id",
    genie_agent_name="hr_data",
    description="Query employee data, headcount, and organizational metrics"
)

# Combine all tools
genie_tools = [sales_tool, product_tool, hr_tool]
```

---

## Pattern 5: Combined Tools for Agents

Combine unstructured and structured retrieval tools and bind to an LLM.

```python
from databricks_langchain import (
    VectorSearchRetrieverTool,
    GenieAgent,
    ChatDatabricks
)

# Unstructured retrieval (documentation, knowledge base)
docs_tool = VectorSearchRetrieverTool(
    index_name="catalog.schema.docs_index",
    name="search_docs",
    description="Search product documentation and knowledge base articles"
)

# Structured retrieval (business data)
sales_tool = GenieAgent(
    genie_space_id="sales_space_id",
    genie_agent_name="sales_data",
    description="Query sales data, revenue metrics, and customer analytics"
)

# Bind tools to LLM
llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
llm_with_tools = llm.bind_tools([docs_tool, sales_tool])

# Now use in your agent
response = llm_with_tools.invoke("What's our Q3 revenue and what docs explain our pricing model?")
```

---

## Pattern 6: UCFunctionToolkit (With MLflow Tracing)

Wrap Unity Catalog functions as tools with automatic MLflow RETRIEVER span tracing.

```python
from databricks_langchain import UCFunctionToolkit

# Create toolkit from existing UC functions
toolkit = UCFunctionToolkit(
    function_names=[
        "catalog.schema.search_docs",
        "catalog.schema.query_sales",
        "catalog.schema.lookup_customer"
    ]
)

# Get tools (automatically traced)
tools = toolkit.tools

# Bind to LLM
from databricks_langchain import ChatDatabricks

llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
llm_with_tools = llm.bind_tools(tools)
```

### Benefits of UCFunctionToolkit

- **Automatic MLflow tracing**: All invocations logged with RETRIEVER spans
- **Governance**: Functions governed by Unity Catalog permissions
- **Versioning**: Functions can be versioned and managed
- **Shared**: Functions reusable across agents

---

## Pattern 7: Custom UC Function Tool

Create a custom UC function and use it as a tool.

```python
from databricks_langchain import DatabricksFunctionClient, UCFunctionToolkit

# Initialize client
client = DatabricksFunctionClient()

# Define function
def lookup_customer(customer_id: str) -> str:
    """Look up customer information by ID.

    Args:
        customer_id: The unique customer identifier

    Returns:
        Customer details as a formatted string
    """
    # Your implementation here
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
    # Query customer data...
    return f"Customer {customer_id}: Premium tier, Active since 2023"

# Create UC function
client.create_python_function(
    func=lookup_customer,
    catalog="main",
    schema="tools"
)

# Use with UCFunctionToolkit
toolkit = UCFunctionToolkit(
    function_names=["main.tools.lookup_customer"]
)

tools = toolkit.tools
```

---

## Pattern 8: Full Tool Setup Example

Complete example combining all tool types.

```python
from databricks_langchain import (
    VectorSearchRetrieverTool,
    GenieAgent,
    UCFunctionToolkit,
    ChatDatabricks
)

# === UNSTRUCTURED TOOLS ===

# Product documentation
product_docs = VectorSearchRetrieverTool(
    index_name="main.docs.product_index",
    name="search_product_docs",
    description="Search product documentation, user guides, and FAQs",
    num_results=5,
    columns=["content", "title", "url"]
)

# Technical documentation with filters
api_docs = VectorSearchRetrieverTool(
    index_name="main.docs.technical_index",
    name="search_api_docs",
    description="Search API documentation and code examples",
    num_results=5,
    columns=["content", "endpoint", "example"],
    filters={"type": "api"},
    query_type="HYBRID"
)

# === STRUCTURED TOOLS ===

# Sales analytics
sales_genie = GenieAgent(
    genie_space_id="sales_genie_space_id",
    genie_agent_name="sales_analytics",
    description="Query sales metrics, revenue data, and customer transactions"
)

# Product analytics
product_genie = GenieAgent(
    genie_space_id="product_genie_space_id",
    genie_agent_name="product_analytics",
    description="Query product usage, feature adoption, and engagement metrics"
)

# === UC FUNCTION TOOLS ===

uc_toolkit = UCFunctionToolkit(
    function_names=[
        "main.tools.lookup_customer",
        "main.tools.get_subscription_status"
    ]
)

# === COMBINE ALL TOOLS ===

all_tools = [
    product_docs,
    api_docs,
    sales_genie,
    product_genie,
    *uc_toolkit.tools
]

# === BIND TO LLM ===

llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
llm_with_tools = llm.bind_tools(all_tools)

# Ready to use in your agent!
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `VectorSearchRetrieverTool` not found | Upgrade: `pip install -U databricks-langchain>=0.13.0` |
| Permission denied on index | Check UC permissions on the Vector Search index |
| Genie space not found | Verify `genie_space_id` from the Genie UI URL |
| UC function not found | Ensure function exists and user has EXECUTE permission |

### Verifying Setup

```python
# Check databricks-langchain version
import databricks_langchain
print(databricks_langchain.__version__)  # Should be >= 0.13.0

# Test Vector Search connection
from databricks_langchain import VectorSearchRetrieverTool
try:
    tool = VectorSearchRetrieverTool(
        index_name="catalog.schema.index",
        name="test",
        description="test"
    )
    print("VectorSearchRetrieverTool: OK")
except Exception as e:
    print(f"Error: {e}")

# Test Genie connection
from databricks_langchain import GenieAgent
try:
    tool = GenieAgent(
        genie_space_id="your_space_id",
        genie_agent_name="test",
        description="test"
    )
    print("GenieAgent: OK")
except Exception as e:
    print(f"Error: {e}")
```

---

## References

- [Databricks Agent Tools Overview](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-tool)
- [Unstructured Retrieval Tools](https://docs.databricks.com/aws/en/generative-ai/agent-framework/unstructured-retrieval-tools)
- [Custom Tools](https://docs.databricks.com/aws/en/generative-ai/agent-framework/create-custom-tool)
- [databricks-langchain API Reference](https://api-docs.databricks.com/python/databricks-ai-bridge/latest/databricks_langchain.html)
- [Genie Spaces](https://docs.databricks.com/aws/en/genie/index.html)
