# LangGraph Unstructured Tool Agent - Quick Reference

## Common Claude Prompts

### Create RAG Agent
```
"Create a simple RAG agent with Vector Search"
"Build a tool-calling RAG agent for my docs index"
"Set up a multi-hop RAG system for complex queries"
```

### Architecture Help
```
"Show me the tool-calling RAG pattern"
"How do I decompose queries for multi-hop retrieval?"
"Create an agent that filters Vector Search results by date"
```

## Vector Search API Quick Reference

### Create Index (Delta Sync)
```python
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# Delta Sync Index (recommended)
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

### Create Index (External)
```python
# External Index (you manage embeddings)
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
```

### Similarity Search
```python
# Get index
index = vsc.get_index(
    endpoint_name="my_endpoint",
    index_name="catalog.schema.docs_index"
)

# Search with query text
results = index.similarity_search(
    query_text="What is RAG?",
    columns=["text", "source", "score"],
    num_results=5
)

# Search with query vector
results = index.similarity_search(
    query_vector=[0.1, 0.2, ...],  # 1024-dim
    columns=["text", "source", "score"],
    num_results=5
)

# Search with filters
results = index.similarity_search(
    query_text="Vector Search",
    columns=["text", "source", "date", "score"],
    filters={"source": {"$eq": "official_docs"}},
    num_results=5
)
```

### Upsert Data (External Index Only)
```python
# Upsert embeddings
index.upsert([
    {
        "id": 1,
        "text": "Databricks Vector Search enables...",
        "embedding": [0.1, 0.2, ...],
        "source": "docs.pdf"
    },
    {
        "id": 2,
        "text": "RAG combines retrieval and generation...",
        "embedding": [0.3, 0.4, ...],
        "source": "guide.pdf"
    }
])
```

## Custom Retriever Usage

### Basic Setup
```python
from vector_search_retriever import DatabricksVectorSearchRetriever

retriever = DatabricksVectorSearchRetriever(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    text_column="text",
    columns=["text", "source"],
    num_results=5
)

# Retrieve documents
documents = retriever.get_relevant_documents("What is RAG?")
```

### With Filters
```python
retriever = DatabricksVectorSearchRetriever(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    filters={
        "source": {"$eq": "official_docs"},
        "date": {"$gte": "2024-01-01"}
    }
)
```

### As LangChain Tool
```python
from vector_search_retriever import create_vector_search_tool

tool = create_vector_search_tool(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint",
    num_results=5,
    tool_name="search_docs",
    tool_description="Search documentation for answers"
)

# Use in agent
tools = [tool]
llm_with_tools = llm.bind_tools(tools)
```

## RAG Agent Patterns

### Pattern 1: Simple RAG
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Sequence
from langchain_core.messages import BaseMessage

class SimpleRAGState(TypedDict):
    messages: Sequence[BaseMessage]
    retrieved_documents: list
    final_answer: str

def retrieve_node(state):
    query = state["messages"][-1].content
    docs = retriever.get_relevant_documents(query)
    return {"retrieved_documents": docs}

def generate_node(state):
    query = state["messages"][-1].content
    docs = state["retrieved_documents"]

    # Format context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Generate answer
    prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    answer = llm.invoke(prompt).content

    return {
        "messages": [AIMessage(content=answer)],
        "final_answer": answer
    }

graph = StateGraph(SimpleRAGState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
agent = graph.compile()
```

### Pattern 2: Tool-Calling RAG
```python
from langgraph.prebuilt import ToolNode

class ToolRAGState(TypedDict):
    messages: Sequence[BaseMessage]

# Create tool
vector_tool = create_vector_search_tool(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint"
)
tools = [vector_tool]

# Bind to LLM
llm_with_tools = llm.bind_tools(tools)

def agent_node(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return "end"

graph = StateGraph(ToolRAGState)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {
    "tools": "tools",
    "end": END
})
graph.add_edge("tools", "agent")
agent = graph.compile()
```

### Pattern 3: Multi-Hop RAG
```python
class MultiHopState(TypedDict):
    messages: Sequence[BaseMessage]
    sub_questions: List[str]
    retrieved_documents: List[list]
    final_answer: str

def decompose_node(state):
    query = state["messages"][-1].content

    prompt = f"""Break this into 2-4 sub-questions:

{query}

Sub-questions (one per line):"""

    response = llm.invoke(prompt)
    sub_questions = [q.strip() for q in response.content.split("\n") if q.strip()]

    return {"sub_questions": sub_questions}

def retrieve_multi_node(state):
    all_docs = []
    for sub_q in state["sub_questions"]:
        docs = retriever.get_relevant_documents(sub_q)
        all_docs.append(docs)
    return {"retrieved_documents": all_docs}

def synthesize_node(state):
    query = state["messages"][-1].content
    sub_qs = state["sub_questions"]
    all_docs = state["retrieved_documents"]

    # Format all context
    context_parts = []
    for sub_q, docs in zip(sub_qs, all_docs):
        context_parts.append(f"Sub-question: {sub_q}")
        for doc in docs:
            context_parts.append(f"- {doc.page_content}")

    context = "\n".join(context_parts)

    # Synthesize answer
    prompt = f"Context:\n{context}\n\nMain question: {query}\n\nAnswer:"
    answer = llm.invoke(prompt).content

    return {
        "messages": [AIMessage(content=answer)],
        "final_answer": answer
    }

graph = StateGraph(MultiHopState)
graph.add_node("decompose", decompose_node)
graph.add_node("retrieve_multi", retrieve_multi_node)
graph.add_node("synthesize", synthesize_node)
graph.add_edge("decompose", "retrieve_multi")
graph.add_edge("retrieve_multi", "synthesize")
graph.add_edge("synthesize", END)
agent = graph.compile()
```

## Script Usage

### Create RAG Agent
```bash
# Simple RAG
python scripts/create_rag_agent.py my_rag_agent \
  --type simple \
  --index-name catalog.schema.docs_index \
  --endpoint-name my_endpoint \
  --num-results 5 \
  -o ./agents

# Tool-calling RAG
python scripts/create_rag_agent.py my_tool_agent \
  --type tool-calling \
  --index-name catalog.schema.docs_index \
  --endpoint-name my_endpoint

# Multi-hop RAG
python scripts/create_rag_agent.py my_multihop_agent \
  --type multi-hop \
  --index-name catalog.schema.docs_index \
  --endpoint-name my_endpoint
```

### Test Retriever
```bash
python scripts/vector_search_retriever.py \
  my_endpoint \
  catalog.schema.docs_index \
  "What is Vector Search?"
```

## Filter Syntax

### Equality
```python
filters = {"source": {"$eq": "official_docs"}}
```

### Comparison
```python
filters = {"score": {"$gte": 0.8}}
filters = {"date": {"$lt": "2024-12-31"}}
```

### Multiple Conditions (AND)
```python
filters = {
    "$and": [
        {"source": {"$eq": "official_docs"}},
        {"date": {"$gte": "2024-01-01"}}
    ]
}
```

### Multiple Conditions (OR)
```python
filters = {
    "$or": [
        {"source": {"$eq": "docs"}},
        {"source": {"$eq": "guides"}}
    ]
}
```

### In List
```python
filters = {"category": {"$in": ["tutorial", "guide", "reference"]}}
```

## Environment Setup

### Required Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
```

### Install Dependencies
```bash
uv add langgraph langchain-core databricks-langchain databricks-vectorsearch mlflow
```

## MLflow Integration

### Enable Tracing
```python
import mlflow

# Auto-log LangChain traces
mlflow.langchain.autolog()

with mlflow.start_run():
    result = agent.invoke(initial_state)

    # Log custom metrics
    mlflow.log_param("index_name", index_name)
    mlflow.log_param("num_results", num_results)
    mlflow.log_metric("num_retrieved", len(result["retrieved_documents"]))
```

### Log Retrieval Quality
```python
with mlflow.start_run():
    result = agent.invoke(state)

    # Log retrieval metrics
    docs = result["retrieved_documents"]
    avg_score = sum(d.metadata.get("score", 0) for d in docs) / len(docs)

    mlflow.log_metric("avg_retrieval_score", avg_score)
    mlflow.log_metric("num_docs_retrieved", len(docs))
```

## Common Patterns

### Rerank Results
```python
def rerank_node(state):
    docs = state["retrieved_documents"]
    query = state["messages"][-1].content

    # Use LLM to rerank
    rerank_prompt = f"""Rank these documents by relevance to: {query}

Documents:
{format_docs(docs)}

Ranked order (indices):"""

    response = llm.invoke(rerank_prompt)
    # Parse and reorder docs
    ...
```

### Hybrid Search (Keyword + Semantic)
```python
def hybrid_retrieve_node(state):
    query = state["messages"][-1].content

    # Semantic search
    semantic_docs = retriever.get_relevant_documents(query)

    # Keyword search (implement with SQL)
    keyword_docs = keyword_search(query)

    # Combine and deduplicate
    combined = merge_results(semantic_docs, keyword_docs)

    return {"retrieved_documents": combined}
```

### Context Compression
```python
def compress_context_node(state):
    docs = state["retrieved_documents"]
    query = state["messages"][-1].content

    # Extract only relevant sentences
    compressed = []
    for doc in docs:
        relevant_parts = extract_relevant_sentences(doc.page_content, query)
        compressed.append(Document(
            page_content=relevant_parts,
            metadata=doc.metadata
        ))

    return {"retrieved_documents": compressed}
```

### Self-Querying
```python
def self_query_node(state):
    query = state["messages"][-1].content

    # Extract filter criteria from query
    extract_prompt = f"""Extract filter criteria from this query:

{query}

Return JSON with filters."""

    response = llm.invoke(extract_prompt)
    filters = parse_filters(response.content)

    # Create retriever with filters
    filtered_retriever = DatabricksVectorSearchRetriever(
        index_name=index_name,
        endpoint_name=endpoint_name,
        filters=filters
    )

    docs = filtered_retriever.get_relevant_documents(query)
    return {"retrieved_documents": docs}
```

## Error Handling

### Handle No Results
```python
def generate_node(state):
    docs = state["retrieved_documents"]

    if not docs:
        return {
            "messages": [AIMessage(content="I couldn't find relevant information.")],
            "final_answer": "No results found"
        }

    # Normal generation
    ...
```

### Handle Retrieval Errors
```python
def retrieve_node(state):
    try:
        docs = retriever.get_relevant_documents(query)
        return {"retrieved_documents": docs}
    except Exception as e:
        print(f"Retrieval error: {e}")
        return {"retrieved_documents": []}
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def retrieve_with_retry(query):
    return retriever.get_relevant_documents(query)
```

## Performance Tips

1. **Optimize num_results**: Start with 3-5, increase only if needed
2. **Use filters**: Narrow search space before similarity search
3. **Cache results**: Use `@lru_cache` for repeated queries
4. **Column selection**: Only retrieve needed columns
5. **Batch queries**: For multi-hop, batch sub-question retrievals
6. **Index optimization**: Use Delta Sync for automatic updates
7. **Embedding dimension**: Balance quality vs speed (768 or 1024)

## Troubleshooting

### Index Not Found
```python
# List all indexes
vsc = VectorSearchClient()
indexes = vsc.list_indexes(endpoint_name="my_endpoint")
print(indexes)
```

### No Results
```python
# Check index status
index = vsc.get_index(endpoint_name="my_endpoint", index_name="catalog.schema.docs_index")
print(index.describe())

# Verify data exists
results = index.similarity_search(query_text="*", num_results=10)
```

### Authentication Errors
```bash
# Verify credentials
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN

# Test API connection
curl -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  $DATABRICKS_HOST/api/2.0/vector-search/endpoints
```

## Best Practices

1. **Always use filters** when possible to improve relevance
2. **Monitor retrieval scores** to ensure quality
3. **Enable MLflow tracing** for debugging
4. **Use Delta Sync indexes** for automatic updates
5. **Implement reranking** for better results
6. **Cache frequent queries** to reduce latency
7. **Format context clearly** for the LLM
8. **Include source metadata** in responses
9. **Handle no-results gracefully**
10. **Log retrieval metrics** for optimization

## Resources

- Vector Search: https://docs.databricks.com/en/generative-ai/vector-search.html
- LangGraph: https://langchain-ai.github.io/langgraph/
- LangChain Retrievers: https://python.langchain.com/docs/modules/data_connection/retrievers/
- MLflow: https://mlflow.org/docs/latest/index.html
