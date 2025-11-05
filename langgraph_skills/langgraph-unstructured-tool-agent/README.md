# LangGraph Unstructured Tool Agent Skill

🎯 **Purpose**: Build LangGraph RAG agents with Databricks Vector Search for semantic document retrieval and question answering.

## 📦 Package Contents

| File | Description |
|------|-------------|
| `langgraph-unstructured-tool-agent/` | **Main skill package** - Add to .claude/skills/ |
| `README.md` | This file - your starting point |
| `QUICK_REFERENCE.md` | Quick reference for Vector Search and RAG patterns |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `langgraph-unstructured-tool-agent.zip` to Claude
- Activates when you request RAG or Vector Search integration

### 2. Use the Skill
```
"Create a RAG agent using Databricks Vector Search"
"Build a tool-calling agent with Vector Search retrieval"
"Set up a multi-hop RAG system for complex questions"
```

### 3. Get Complete Agent
Claude will generate:
- LangGraph RAG agent with Vector Search
- Custom retriever implementation
- Tool-calling integration
- MLflow tracing setup

## 🎯 What This Skill Does

### Input
- Vector Search index details (catalog.schema.index)
- Vector Search endpoint name
- RAG pattern preference (simple, tool-calling, multi-hop)

### Output
- Complete LangGraph RAG agent
- Custom Vector Search retriever
- State management
- Error handling
- MLflow integration

## 🔥 Key Features

### Vector Search Integration
- Delta Sync Index support
- External Index support
- Similarity search with filters
- Metadata extraction
- Score-based ranking

### RAG Patterns
- **Simple RAG**: Retrieve → Generate (always retrieves)
- **Tool-calling RAG**: LLM decides when to retrieve
- **Multi-hop RAG**: Query decomposition → Multiple retrievals → Synthesis
- **Self-query RAG**: LLM extracts filters from natural language queries

### Production Ready
- Custom LangChain retriever
- Tool wrapper for agent integration
- MLflow tracing built-in
- Comprehensive error handling

## 💡 Common Use Cases

### Simple RAG Agent
```python
# Retrieves documents and generates answer
agent = create_simple_rag_agent(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint"
)

result = agent.invoke({
    "messages": [HumanMessage("What is RAG?")],
    "retrieved_documents": [],
    "final_answer": ""
})
```

### Tool-Calling RAG Agent
```python
# LLM decides whether to use Vector Search
vector_search_tool = create_vector_search_tool(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    tool_name="search_docs",
    tool_description="Search documentation for answers"
)

agent = create_tool_calling_agent(tools=[vector_search_tool])
```

### Multi-Hop RAG Agent
```python
# Complex questions decomposed into sub-questions
agent = create_multi_hop_agent(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint"
)

result = agent.invoke({
    "messages": [HumanMessage("Compare X and Y features")],
    "sub_questions": [],
    "retrieved_documents": [],
    "final_answer": ""
})
```

### Self-Query RAG Agent
```python
from langchain.chains.query_constructor.base import AttributeInfo

# Define metadata fields for filtering
metadata_field_info = [
    AttributeInfo(name="source", description="Source document", type="string"),
    AttributeInfo(name="category", description="Category (tutorial/guide/api)", type="string"),
    AttributeInfo(name="date", description="Date (YYYY-MM-DD)", type="string")
]

# LLM automatically extracts filters from natural language
agent = create_self_query_agent(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    metadata_field_info=metadata_field_info
)

# Example: "Show me Python tutorials from after 2024-01-01"
# → Automatically extracts: category='tutorial' AND date >= '2024-01-01'
result = agent.invoke({
    "messages": [HumanMessage("Show me Python tutorials from the user guide")],
    "retrieved_documents": [],
    "final_response": ""
})
```

## 📝 Architecture Patterns

### Pattern 1: Simple RAG
```
User Query → Retrieve Docs → Generate Answer → End
```
**Use when**: Always need to retrieve context

### Pattern 2: Tool-Calling RAG
```
User Query → LLM Decision → Retrieve (if needed) → Generate → End
                ↓
           Direct Answer (if no retrieval needed)
```
**Use when**: Some queries don't need retrieval

### Pattern 3: Multi-Hop RAG
```
User Query → Decompose → Retrieve for Q1 → Retrieve for Q2 → ... → Synthesize → End
```
**Use when**: Complex questions need multiple retrievals

### Pattern 4: Self-Query RAG
```
User Query → Extract Filters → Filtered Similarity Search → Generate → End
              (via LLM)         (with metadata filters)
```
**Use when**: Need to filter by metadata (source, category, date, etc.)

## 🛠️ What Gets Created

### Vector Search Retriever (`vector_search_retriever.py`)
```python
# Custom retriever for Databricks Vector Search
retriever = DatabricksVectorSearchRetriever(
    index_name="catalog.schema.my_index",
    endpoint_name="my_endpoint",
    text_column="text",
    columns=["text", "source", "date"],
    num_results=5
)

# Use with LangChain
documents = retriever.get_relevant_documents("What is RAG?")

# Or as a tool
tool = DatabricksVectorSearchTool(retriever).as_langchain_tool()
```

### RAG Agent Implementation
```python
# Agent state schema
class RAGAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    retrieved_documents: list
    final_answer: str

# Agent nodes
def retrieve_node(state): ...
def generate_node(state): ...

# Build graph
graph = StateGraph(RAGAgentState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)
agent = graph.compile()
```

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| Quick commands | `QUICK_REFERENCE.md` |
| Vector Search API | `references/vector-search-guide.md` (in package) |
| RAG patterns | `references/rag-patterns.md` (in package) |
| Advanced techniques | `references/advanced-rag.md` (in package) |
| Index creation | `references/index-setup.md` (in package) |

## ⚙️ Prerequisites

### Required
- Databricks workspace
- Vector Search endpoint created
- Vector Search index created and populated
- Personal access token
- Python 3.10+

### Python Packages
```bash
uv add langgraph langchain-core databricks-langchain databricks-vectorsearch mlflow
```

### Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
```

## 🎯 Vector Search Index Setup

### Option 1: Delta Sync Index (Recommended)
```sql
-- Create Delta table with embeddings
CREATE TABLE catalog.schema.docs (
  id BIGINT GENERATED ALWAYS AS IDENTITY,
  text STRING,
  embedding ARRAY<FLOAT>,
  source STRING,
  created_date TIMESTAMP
);

-- Insert data
INSERT INTO catalog.schema.docs (text, embedding, source, created_date)
VALUES (...);
```

```python
# Create Delta Sync Index
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()
index = vsc.create_delta_sync_index(
    endpoint_name="my_endpoint",
    source_table_name="catalog.schema.docs",
    index_name="catalog.schema.docs_index",
    pipeline_type="TRIGGERED",
    primary_key="id",
    embedding_dimension=1024,
    embedding_vector_column="embedding"
)
```

### Option 2: External Index
```python
# Create external index (you manage embeddings)
index = vsc.create_direct_access_index(
    endpoint_name="my_endpoint",
    index_name="catalog.schema.external_index",
    primary_key="id",
    embedding_dimension=1024,
    embedding_vector_column="embedding",
    schema={
        "id": "long",
        "text": "string",
        "embedding": "array<float>",
        "source": "string"
    }
)

# Upsert embeddings
index.upsert([
    {"id": 1, "text": "...", "embedding": [...], "source": "doc1.pdf"},
    {"id": 2, "text": "...", "embedding": [...], "source": "doc2.pdf"}
])
```

## 🎉 Benefits

- ⚡ **Fast**: Native Databricks Vector Search integration
- 🎯 **Smart**: LLM-powered retrieval and generation
- 🔧 **Flexible**: Multiple RAG patterns (simple, tool-calling, multi-hop)
- 📊 **Observable**: MLflow tracing built-in
- 🚀 **Production-ready**: Error handling and retry logic

## 📊 Example Workflows

### Workflow 1: Documentation Q&A
```
1. User asks: "How do I create a Vector Search index?"
2. Retrieve: Find relevant docs from index
3. Generate: Answer with context from docs
4. Return: Answer + sources
```

### Workflow 2: Complex Analysis
```
1. User asks: "Compare performance of Delta Sync vs External indexes"
2. Decompose:
   - "What is Delta Sync index performance?"
   - "What is External index performance?"
3. Retrieve: Get docs for each sub-question
4. Synthesize: Compare and generate comprehensive answer
5. Return: Detailed comparison with sources
```

### Workflow 3: Conversational RAG
```
1. User: "What is RAG?"
   - Retrieve docs about RAG
   - Generate: "RAG is Retrieval Augmented Generation..."

2. User: "How does it work with Vector Search?"
   - Context: Previous conversation + new retrieval
   - Generate: "Building on RAG, Vector Search enables..."

3. User: "Show me an example"
   - Retrieve: Code examples
   - Generate: Python code with explanation
```

## 🔍 Retrieval Optimization

### 1. Number of Results
```python
# Fewer results = faster, more focused
retriever = create_retriever(num_results=3)  # Top 3

# More results = broader context, slower
retriever = create_retriever(num_results=10)  # Top 10
```

### 2. Metadata Filtering
```python
# Filter by source
retriever = DatabricksVectorSearchRetriever(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    filters={"source": {"$eq": "official_docs"}}
)

# Filter by date
retriever = DatabricksVectorSearchRetriever(
    filters={"created_date": {"$gte": "2024-01-01"}}
)
```

### 3. Column Selection
```python
# Retrieve only needed columns
retriever = create_retriever(
    text_column="text",
    columns=["text", "source", "date"]  # Don't retrieve embeddings
)
```

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check Databricks Vector Search docs
- Review LangGraph documentation

---

**Ready to get started?** Upload `langgraph-unstructured-tool-agent.zip` to Claude and start building RAG agents!
