# LangGraph Unstructured Tool Agent Skill

## Purpose

This skill helps Claude build LangGraph agents with unstructured retrieval tools using Databricks Vector Search. It enables creating RAG (Retrieval Augmented Generation) agents that can search vector indexes, retrieve relevant documents, and generate grounded responses.

## When to Activate

This skill should activate when the user requests:
- "Create a RAG agent with Databricks Vector Search"
- "Build a LangGraph agent with retrieval tools"
- "Set up a tool-calling agent with vector search"
- "Create an agent that searches documents using embeddings"
- "Build an unstructured retrieval agent with LangGraph"
- "Integrate Vector Search index into my agent"

## Core Capabilities

### 1. Vector Search Integration
- Connect to Databricks Vector Search indexes
- Perform similarity search with embeddings
- Retrieve relevant documents with metadata
- Handle external and delta sync indexes

### 2. RAG Agent Patterns
- Query understanding and decomposition
- Context retrieval from vector indexes
- Response generation with retrieved context
- Multi-hop reasoning with multiple retrievals

### 3. Tool-Calling Architecture
- Vector search as LangChain tool
- Custom retriever tools
- Tool result processing
- Multi-tool coordination

### 4. LangGraph Orchestration
- Stateful agent workflows
- Conditional retrieval logic
- Response evaluation and refinement
- Error handling and fallbacks

## Databricks Vector Search Overview

### Vector Search Index Types

#### 1. Delta Sync Index
Automatically syncs from a Delta table:
```python
from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

index = vsc.create_delta_sync_index(
    endpoint_name="vs_endpoint",
    index_name="catalog.schema.docs_index",
    source_table_name="catalog.schema.documents",
    pipeline_type="TRIGGERED",
    primary_key="doc_id",
    embedding_source_column="text",
    embedding_model_endpoint_name="databricks-bge-large-en"
)
```

#### 2. External Index
Manually manage embeddings:
```python
index = vsc.create_direct_access_index(
    endpoint_name="vs_endpoint",
    index_name="catalog.schema.external_index",
    primary_key="id",
    embedding_dimension=1024,
    embedding_vector_column="embedding",
    schema={
        "id": "string",
        "text": "string",
        "embedding": "array<float>"
    }
)
```

### Searching Indexes

```python
results = index.similarity_search(
    query_text="What is machine learning?",
    columns=["id", "text", "url"],
    num_results=5
)

# Results structure
{
    "manifest": {"column_count": 3},
    "result": {
        "row_count": 5,
        "data_array": [
            ["doc1", "Machine learning is...", "http://...", 0.92],
            ["doc2", "ML algorithms...", "http://...", 0.88],
            ...
        ]
    }
}
```

## LangChain Tool Integration

### Vector Search as Tool

```python
from langchain.tools import Tool
from langchain.agents import AgentExecutor
from databricks.vector_search.client import VectorSearchClient

def create_vector_search_tool(index_name: str, endpoint_name: str):
    """Create a vector search tool for LangChain."""

    vsc = VectorSearchClient()
    index = vsc.get_index(endpoint_name, index_name)

    def search_documents(query: str) -> str:
        """Search for relevant documents."""
        results = index.similarity_search(
            query_text=query,
            columns=["text", "source", "score"],
            num_results=5
        )

        # Format results
        docs = extract_documents(results)
        return format_context(docs)

    return Tool(
        name="vector_search",
        description="Search documentation for relevant information. Input should be a search query.",
        func=search_documents
    )
```

### Custom Retriever

```python
from langchain.schema import Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.retrievers import BaseRetriever
from typing import List

class DatabricksVectorSearchRetriever(BaseRetriever):
    """Custom retriever for Databricks Vector Search."""

    index_name: str
    endpoint_name: str
    num_results: int = 5
    columns: List[str] = ["text", "source"]

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Retrieve documents from Vector Search."""
        vsc = VectorSearchClient()
        index = vsc.get_index(self.endpoint_name, self.index_name)

        results = index.similarity_search(
            query_text=query,
            columns=self.columns + ["score"],
            num_results=self.num_results
        )

        # Convert to LangChain Documents
        documents = []
        for row in extract_rows(results):
            doc = Document(
                page_content=row.get("text", ""),
                metadata={
                    "source": row.get("source", ""),
                    "score": row.get("score", 0.0)
                }
            )
            documents.append(doc)

        return documents
```

## RAG Agent Patterns

### Pattern 1: Simple RAG Agent

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from databricks_langchain import ChatDatabricks
from typing import TypedDict, Sequence, Annotated
import operator

class RAGAgentState(TypedDict):
    """State for RAG agent."""
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]
    retrieved_context: str
    final_response: str

# Initialize components
llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
retriever = DatabricksVectorSearchRetriever(
    index_name="catalog.schema.docs_index",
    endpoint_name="vs_endpoint"
)

def retrieve_node(state: RAGAgentState) -> RAGAgentState:
    """Retrieve relevant documents."""
    query = state["messages"][-1].content

    # Retrieve documents
    docs = retriever.get_relevant_documents(query)

    # Format context
    context = "\n\n".join([
        f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
        for doc in docs
    ])

    return {"retrieved_context": context}

def generate_node(state: RAGAgentState) -> RAGAgentState:
    """Generate response with retrieved context."""
    query = state["messages"][-1].content
    context = state["retrieved_context"]

    prompt = f"""
    Answer the following question using the provided context. If the context doesn't contain
    relevant information, say so.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    response = llm.invoke(prompt)

    return {
        "messages": [AIMessage(content=response.content)],
        "final_response": response.content
    }

# Build graph
graph = StateGraph(RAGAgentState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

rag_agent = graph.compile()
```

### Pattern 2: Multi-Hop RAG Agent

Agent that performs multiple retrieval rounds:

```python
class MultiHopRAGState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    original_query: str
    sub_queries: List[str]
    retrieved_contexts: List[str]
    iteration: int
    max_iterations: int

def decompose_query_node(state: MultiHopRAGState) -> MultiHopRAGState:
    """Break down complex query into sub-queries."""
    query = state["messages"][-1].content

    decompose_prompt = f"""
    Break down this complex question into 2-3 simpler sub-questions that can be
    answered independently:

    Question: {query}

    Sub-questions (one per line):
    """

    response = llm.invoke(decompose_prompt)
    sub_queries = [q.strip() for q in response.content.split("\n") if q.strip()]

    return {
        "original_query": query,
        "sub_queries": sub_queries,
        "iteration": 0
    }

def retrieve_for_subquery_node(state: MultiHopRAGState) -> MultiHopRAGState:
    """Retrieve for current sub-query."""
    iteration = state["iteration"]
    sub_queries = state["sub_queries"]

    if iteration >= len(sub_queries):
        return state

    current_query = sub_queries[iteration]

    # Retrieve
    docs = retriever.get_relevant_documents(current_query)
    context = format_documents(docs)

    return {
        "retrieved_contexts": state.get("retrieved_contexts", []) + [context],
        "iteration": iteration + 1
    }

def synthesize_node(state: MultiHopRAGState) -> MultiHopRAGState:
    """Synthesize final answer from all contexts."""
    original_query = state["original_query"]
    contexts = state["retrieved_contexts"]

    combined_context = "\n\n---\n\n".join(contexts)

    prompt = f"""
    Using the following information from multiple sources, answer the original question:

    {combined_context}

    Original Question: {original_query}

    Comprehensive Answer:
    """

    response = llm.invoke(prompt)

    return {
        "messages": [AIMessage(content=response.content)]
    }

# Build multi-hop graph
graph = StateGraph(MultiHopRAGState)
graph.add_node("decompose", decompose_query_node)
graph.add_node("retrieve_subquery", retrieve_for_subquery_node)
graph.add_node("synthesize", synthesize_node)

def should_continue_retrieval(state: MultiHopRAGState) -> str:
    if state["iteration"] < len(state["sub_queries"]):
        return "retrieve_subquery"
    return "synthesize"

graph.set_entry_point("decompose")
graph.add_edge("decompose", "retrieve_subquery")
graph.add_conditional_edges(
    "retrieve_subquery",
    should_continue_retrieval,
    {
        "retrieve_subquery": "retrieve_subquery",
        "synthesize": "synthesize"
    }
)
graph.add_edge("synthesize", END)

multi_hop_agent = graph.compile()
```

### Pattern 3: Tool-Calling RAG Agent

Agent that decides when to use retrieval tool:

```python
from langchain.tools import Tool

class ToolCallingRAGState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_calls: List[dict]
    tool_results: List[str]

# Create vector search tool
vector_search_tool = Tool(
    name="search_documentation",
    description="Search technical documentation for information about features, APIs, and best practices.",
    func=lambda q: retriever.get_relevant_documents(q)
)

def agent_node(state: ToolCallingRAGState) -> ToolCallingRAGState:
    """LLM decides whether to use tools."""
    query = state["messages"][-1].content

    # LLM with tool-calling
    llm_with_tools = llm.bind_tools([vector_search_tool])

    response = llm_with_tools.invoke(query)

    # Check if tool was called
    if response.tool_calls:
        return {
            "tool_calls": response.tool_calls,
            "messages": [response]
        }
    else:
        # Direct response without tools
        return {
            "messages": [AIMessage(content=response.content)]
        }

def tool_node(state: ToolCallingRAGState) -> ToolCallingRAGState:
    """Execute tools."""
    tool_calls = state["tool_calls"]
    results = []

    for call in tool_calls:
        if call["name"] == "search_documentation":
            docs = vector_search_tool.func(call["args"]["query"])
            result = format_documents(docs)
            results.append(result)

    return {"tool_results": results}

def should_continue(state: ToolCallingRAGState) -> str:
    if state.get("tool_calls"):
        return "tools"
    return END

# Build graph
graph = StateGraph(ToolCallingRAGState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")  # Loop back for final response

tool_calling_agent = graph.compile()
```

## Advanced Patterns

### Hybrid Search (Vector + Keyword)

```python
def hybrid_search(query: str, alpha: float = 0.5):
    """Combine vector similarity and keyword search."""

    # Vector search
    vector_results = index.similarity_search(query_text=query, num_results=10)

    # Keyword search (via Delta table)
    keyword_query = f"""
    SELECT id, text, source
    FROM catalog.schema.documents
    WHERE text LIKE '%{query}%'
    LIMIT 10
    """
    keyword_results = spark.sql(keyword_query).collect()

    # Merge and re-rank
    combined = merge_and_rank(vector_results, keyword_results, alpha)

    return combined[:5]
```

### Self-Querying Retriever

```python
def self_query_node(state):
    """Generate optimized search query from user question."""

    user_query = state["messages"][-1].content

    optimization_prompt = f"""
    Convert this natural language question into an optimized search query:

    Question: {user_query}

    Search Query (keywords and key phrases only):
    """

    optimized = llm.invoke(optimization_prompt)
    search_query = optimized.content.strip()

    # Use optimized query for retrieval
    docs = retriever.get_relevant_documents(search_query)

    return {"retrieved_context": format_documents(docs)}
```

### Response Grading

```python
def grade_response_node(state):
    """Check if response is grounded in retrieved context."""

    response = state["messages"][-1].content
    context = state["retrieved_context"]

    grading_prompt = f"""
    Context: {context}

    Response: {response}

    Is the response fully supported by the context? Answer YES or NO only.
    """

    grade = llm.invoke(grading_prompt)

    if "NO" in grade.content:
        # Need to retrieve more or clarify
        return {"needs_refinement": True}

    return {"needs_refinement": False}
```

## Helper Functions

### Extract Documents from Results

```python
def extract_documents(results: dict) -> List[dict]:
    """Extract documents from Vector Search results."""
    try:
        data_array = results["result"]["data_array"]
        columns = results["manifest"]["columns"]

        documents = []
        for row in data_array:
            doc = dict(zip(columns, row))
            documents.append(doc)

        return documents

    except (KeyError, TypeError) as e:
        print(f"Error extracting documents: {e}")
        return []
```

### Format Context for LLM

```python
def format_context(documents: List[dict]) -> str:
    """Format retrieved documents as context string."""
    if not documents:
        return "No relevant documents found."

    context_parts = []
    for i, doc in enumerate(documents, 1):
        text = doc.get("text", "")
        source = doc.get("source", "Unknown")
        score = doc.get("score", 0.0)

        context_parts.append(
            f"[Document {i}] (Relevance: {score:.2f})\n"
            f"Source: {source}\n"
            f"{text}\n"
        )

    return "\n".join(context_parts)
```

### Chunk Text for Indexing

```python
def chunk_documents(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
```

## MLflow Integration

### Log RAG Agent

```python
import mlflow

# Enable tracing
mlflow.langchain.autolog()

# Log agent
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("index_name", index_name)
    mlflow.log_param("num_retrieval_results", num_results)
    mlflow.log_param("llm_endpoint", llm_endpoint)

    # Run agent
    result = rag_agent.invoke(initial_state)

    # Log metrics
    mlflow.log_metric("num_retrieved_docs", len(result["retrieved_contexts"]))
    mlflow.log_metric("response_length", len(result["final_response"]))

    # Log agent
    mlflow.langchain.log_model(rag_agent, "rag_agent")
```

## Configuration

### Environment Variables

```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
export VECTOR_SEARCH_ENDPOINT="vs_endpoint"
export VECTOR_SEARCH_INDEX="catalog.schema.docs_index"
```

### Agent Config

```yaml
# config/rag_agent.yaml
vector_search:
  endpoint_name: ${VECTOR_SEARCH_ENDPOINT}
  index_name: ${VECTOR_SEARCH_INDEX}
  num_results: 5
  score_threshold: 0.7

retrieval:
  chunk_size: 512
  chunk_overlap: 50
  columns: ["text", "source", "metadata"]

llm:
  endpoint: ${DATABRICKS_LLM_ENDPOINT}
  temperature: 0.1
  max_tokens: 2000

agent:
  max_iterations: 3
  enable_multi_hop: true
  enable_grading: true
```

## Best Practices

### 1. Optimize Retrieval

```python
# Use appropriate num_results
results = index.similarity_search(
    query_text=query,
    num_results=5,  # Balance between context and relevance
    columns=["text", "source"]  # Only retrieve needed columns
)

# Filter by score threshold
filtered_docs = [doc for doc in docs if doc.metadata["score"] > 0.7]
```

### 2. Handle No Results

```python
def retrieve_with_fallback(query: str):
    docs = retriever.get_relevant_documents(query)

    if not docs:
        # Fallback: reformulate query or use broader search
        reformulated = reformulate_query(query)
        docs = retriever.get_relevant_documents(reformulated)

    return docs
```

### 3. Chunk Management

```python
# Optimal chunk size depends on use case
# Technical docs: 256-512 tokens
# Articles/blogs: 512-1024 tokens
# Books: 1024-2048 tokens

def smart_chunking(text: str, doc_type: str):
    if doc_type == "technical":
        return chunk_documents(text, chunk_size=256, overlap=50)
    elif doc_type == "article":
        return chunk_documents(text, chunk_size=512, overlap=100)
    else:
        return chunk_documents(text, chunk_size=1024, overlap=200)
```

### 4. Citation Tracking

```python
def generate_with_citations(context: str, query: str):
    """Generate response with source citations."""

    prompt = f"""
    Answer the question using the provided context. Include [Source N] citations
    after each fact.

    Context:
    {context}

    Question: {query}

    Answer with citations:
    """

    response = llm.invoke(prompt)
    return response.content
```

## Reference Files

The skill includes:
- `references/vector-search-guide.md` - Vector Search API and patterns
- `references/rag-patterns.md` - RAG architecture patterns
- `references/tool-calling-guide.md` - LangChain tool integration
- `references/evaluation-guide.md` - RAG evaluation methods

## Scripts

### scripts/vector_search_retriever.py
Complete retriever implementation with Vector Search.

### scripts/create_rag_agent.py
Generate RAG agent from template.

### scripts/index_documents.py
Helper to index documents into Vector Search.

## Tips for Claude

- Always retrieve before generating responses
- Use appropriate num_results (typically 3-5)
- Format context clearly with source citations
- Handle cases with no relevant documents
- Enable MLflow tracing for debugging
- Test with various query types
- Consider multi-hop for complex questions
- Grade responses for hallucination prevention
