# LangGraph Genie Agent Skill

🎯 **Purpose**: Build LangGraph tool-calling agents that integrate with Databricks Genie API for natural language data querying.

## 📦 Package Contents

| File | Description |
|------|-------------|
| `langgraph-genie-agent/` | **Main skill package** - Add to .claude/skills/ |
| `README.md` | This file - your starting point |
| `QUICK_REFERENCE.md` | Quick reference for Genie API and LangGraph patterns |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `langgraph-genie-agent.zip` to Claude
- Activates when you request Genie + LangGraph integration

### 2. Use the Skill
```
"Create a LangGraph agent that queries my Genie space"
"Build a multi-agent system with Genie for sales and finance data"
"Set up an agent with Databricks Genie API integration"
```

### 3. Get Complete Agent
Claude will generate:
- LangGraph agent with Genie integration
- Genie API client code
- MLflow tracing setup
- Complete examples

## 🎯 What This Skill Does

### Input
- Genie space ID(s)
- Agent requirements (single vs multi-agent)
- Query patterns

### Output
- Complete LangGraph agent implementation
- Genie API client
- State management
- Error handling
- MLflow integration

## 🔥 Key Features

### Genie API Integration
- Start and continue conversations
- Wait for query completion
- Extract structured results
- Handle errors gracefully

### LangGraph Patterns
- **Single Agent**: Query one Genie space
- **Multi-Agent**: Supervisor routing to specialized agents
- **Conversational**: Multi-turn with context
- **Tool-calling**: Genie as LLM tool

### Production Ready
- MLflow tracing built-in
- Comprehensive error handling
- Conversation state management
- Result caching support

## 💡 Common Use Cases

### Single Genie Agent
```python
# Agent that queries sales Genie space
agent = create_agent(space_id="sales_space_123")
result = agent.invoke({
    "messages": [HumanMessage("What were Q4 sales?")],
    "genie_space_id": "sales_space_123"
})
```

### Multi-Agent System
```python
# Supervisor routes to sales, finance, or inventory agents
agents = {
    "sales_agent": {"space_id": "sales_123", "description": "Sales data"},
    "finance_agent": {"space_id": "finance_456", "description": "Financial metrics"}
}
multi_agent = create_multi_agent(agents)
```

### Conversational Agent
```python
# Maintains conversation context for follow-ups
result1 = agent.invoke({"messages": [HumanMessage("Show top products")]})
result2 = agent.invoke({"messages": [HumanMessage("What about last quarter?")]})
# Genie understands "last quarter" refers to previous query
```

## 📝 Architecture Patterns

### Pattern 1: Simple Genie Query
```
User Query → Analyze → Query Genie → Format Response → End
```

### Pattern 2: Supervisor + Workers
```
User Query → Supervisor → Route to Agent → Query Genie → Format → End
                ↓
            [Sales Agent]
            [Finance Agent]
            [Inventory Agent]
```

### Pattern 3: Agentic Decision Making
```
User Query → Analyze → Needs Data? → Yes → Query Genie → Format
                           ↓
                          No → Respond Directly → End
```

## 🛠️ What Gets Created

### Genie API Client (`genie_client.py`)
```python
client = GenieClient(host, token)

# Start conversation
message = client.start_conversation(space_id, "What were total sales?")

# Continue conversation
follow_up = client.continue_conversation(
    space_id, conversation_id, "What about last month?"
)

# Extract data
data = client.extract_data(message)
# Returns: {"columns": [...], "data": [...], "row_count": N}
```

### Agent Implementation
```python
# State schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    genie_space_id: str
    conversation_id: Optional[str]
    query_results: list

# Agent nodes
def query_genie_node(state): ...
def format_response_node(state): ...

# Build graph
graph = StateGraph(AgentState)
graph.add_node("query_genie", query_genie_node)
# ... add more nodes and edges
agent = graph.compile()
```

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| Quick commands | `QUICK_REFERENCE.md` |
| Genie API details | `references/genie-api-guide.md` (in package) |
| LangGraph patterns | `references/langgraph-patterns.md` (in package) |
| Multi-agent examples | `references/multi-agent-examples.md` (in package) |
| Deployment guide | `references/deployment-guide.md` (in package) |

## ⚙️ Prerequisites

### Required
- Databricks workspace with Genie
- Genie space(s) created
- Personal access token
- Python 3.10+

### Python Packages
```bash
uv add langgraph langchain-core databricks-langchain mlflow requests
```

### Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
export GENIE_SPACE_ID="your_space_id"
```

## 🎉 Benefits

- ⚡ **Fast**: Direct Genie API integration
- 🎯 **Smart**: LLM-powered routing and formatting
- 🔧 **Flexible**: Single or multi-agent architectures
- 📊 **Observable**: MLflow tracing built-in
- 🚀 **Production-ready**: Error handling and retry logic

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check Databricks Genie API docs
- Review LangGraph documentation

---

**Ready to get started?** Upload `langgraph-genie-agent.zip` to Claude and start building!
