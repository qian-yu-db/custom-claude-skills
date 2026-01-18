# LangGraph Multi-Agent Supervisor Skill

🎯 **Purpose**: Build LangGraph multi-agent systems with a supervisor that intelligently orchestrates specialized worker agents (Genie, RAG, MCP, custom agents).

## 📦 Package Contents

| File | Description |
|------|-------------|
| `langgraph-multi-agent-supervisor/` | **Main skill package** - Add to .claude/skills/ |
| `README.md` | This file - your starting point |
| `QUICK_REFERENCE.md` | Quick reference for supervisor patterns |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `langgraph-multi-agent-supervisor.zip` to Claude
- Activates when you request multi-agent orchestration

### 2. Use the Skill
```
"Create a multi-agent supervisor with Genie and RAG agents"
"Build an agent orchestration system with specialized workers"
"Set up a supervisor that routes to different expert agents"
```

### 3. Get Complete System
Claude will generate:
- Supervisor orchestrator with intelligent routing
- Worker agent configurations
- Agent executor implementations
- MLflow tracing integration

## 🎯 What This Skill Does

### Input
- Worker agent specifications (Genie, RAG, MCP, custom)
- Routing strategy (LLM-based or rule-based)
- Agent descriptions and configurations

### Output
- Complete multi-agent supervisor system
- Intelligent routing logic
- Worker agent implementations
- Configuration files
- Execution scripts

## 🔥 Key Features

### Supervisor Capabilities
- **LLM-based routing**: Semantic understanding of queries
- **Rule-based routing**: Keyword matching for known patterns
- **Sequential execution**: Multi-step workflows
- **Parallel execution**: Concurrent agent execution
- **Fallback handling**: Automatic fallback to default agent

### Supported Agent Types
- **Genie agents**: Query Databricks Genie spaces
- **RAG agents**: Search Vector Search indexes
- **MCP agents**: Call Model Context Protocol tools
- **LLM agents**: Direct LLM conversations
- **Custom agents**: Your own agent logic

### Production Ready
- Flexible orchestrator architecture
- Built-in agent executors
- MLflow tracing
- Error handling and fallback
- Configuration-driven setup

## 💡 Common Use Cases

### Multi-Domain Assistant
```python
# Supervisor with specialized domain agents
agents = {
    "sales_agent": {
        "type": "genie",
        "description": "Sales data and revenue analysis",
        "space_id": "sales_space_123"
    },
    "docs_agent": {
        "type": "rag",
        "description": "Technical documentation search",
        "index_name": "catalog.schema.docs_index"
    },
    "support_agent": {
        "type": "custom",
        "description": "Customer support tickets"
    }
}

# Supervisor automatically routes to appropriate agent
```

### Data + Documentation Assistant
```python
# Combined data querying and document search
orchestrator = SupervisorOrchestrator(agents={
    "data_agent": GenieAgent("finance_space"),
    "docs_agent": RAGAgent("docs_index")
})

# User: "What were Q4 expenses?" → routes to data_agent
# User: "How do I create a dashboard?" → routes to docs_agent
```

### Sequential Workflow
```python
# Multi-step agent execution
# 1. Research agent finds relevant docs
# 2. Analysis agent queries data
# 3. Synthesis agent combines results
# 4. Formatting agent creates report
```

## 📝 Architecture Patterns

### Pattern 1: Simple Supervisor
```
User Query → Supervisor → Select Agent → Execute → Return Result
                ↓
          [Agent 1] [Agent 2] [Agent 3]
```
**Use when**: Single agent selection per query

### Pattern 2: Hierarchical Supervisor
```
User Query → Main Supervisor → Domain Supervisor → Agent
                ↓                    ↓
         [Data Domain]        [Sales Agent]
         [Docs Domain]        [Finance Agent]
         [Support Domain]     [Inventory Agent]
```
**Use when**: Complex domains with sub-categories

### Pattern 3: Sequential Multi-Agent
```
User Query → Planner → Agent 1 → Agent 2 → Agent 3 → Synthesizer
                ↓
          [Planned Sequence]
```
**Use when**: Multi-step workflows where agents build on each other

### Pattern 4: Parallel Multi-Agent
```
User Query → Dispatcher → [Agent 1] → Aggregator → Final Result
                              [Agent 2] ↗
                              [Agent 3] ↗
```
**Use when**: Independent queries that can run concurrently

## 🛠️ What Gets Created

### Supervisor Orchestrator (`supervisor_orchestrator.py`)
```python
from supervisor_orchestrator import SupervisorOrchestrator, AgentConfig

# Define agents
agents = {
    "sales_agent": AgentConfig(
        name="sales_agent",
        type="genie",
        description="Sales data queries",
        config={"space_id": "sales_123"}
    ),
    "docs_agent": AgentConfig(
        name="docs_agent",
        type="rag",
        description="Documentation search",
        config={"index_name": "catalog.schema.docs"}
    )
}

# Create orchestrator
orchestrator = SupervisorOrchestrator(
    agents=agents,
    routing_strategy="llm",
    enable_fallback=True
)

# Register executors
orchestrator.register_agent_executor("sales_agent", genie_executor)
orchestrator.register_agent_executor("docs_agent", rag_executor)

# Build and run
orchestrator.build()
result = orchestrator.invoke("What were Q4 sales?")
```

### Configuration File (`agents_config.json`)
```json
{
  "agents": {
    "sales_agent": {
      "type": "genie",
      "description": "Sales data, revenue, customer analytics",
      "config": {
        "space_id": "sales_space_123"
      }
    },
    "docs_agent": {
      "type": "rag",
      "description": "Technical documentation and guides",
      "config": {
        "index_name": "catalog.schema.docs_index",
        "endpoint_name": "my_endpoint"
      }
    }
  },
  "supervisor": {
    "routing_strategy": "llm",
    "enable_fallback": true,
    "default_agent": "general_agent"
  }
}
```

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| Quick commands | `QUICK_REFERENCE.md` |
| Supervisor patterns | `references/supervisor-patterns.md` (in package) |
| Agent integration | `references/agent-integration.md` (in package) |
| Configuration guide | `references/configuration-guide.md` (in package) |

## ⚙️ Prerequisites

### Required
- Databricks workspace
- At least one data source (Genie space, Vector Search index, etc.)
- Personal access token
- Python 3.10+

### Python Packages
```bash
uv add langgraph langchain-core databricks-langchain mlflow
```

### For Genie Agents
```bash
# Requires genie_client.py from langgraph-genie-agent skill
```

### For RAG Agents
```bash
# Requires vector_search_retriever.py from langgraph-unstructured-tool-agent skill
```

### Environment Variables
```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_LLM_ENDPOINT="databricks-meta-llama-3-1-70b-instruct"
```

## 🎯 Creating a Supervisor System

### Step 1: Define Agents
Create `agents.json`:
```json
{
  "agents": [
    {
      "name": "sales_agent",
      "type": "genie",
      "description": "Sales data queries",
      "config": {"space_id": "sales_space_123"},
      "keywords": ["sales", "revenue", "customers"]
    },
    {
      "name": "docs_agent",
      "type": "rag",
      "description": "Documentation search",
      "config": {
        "index_name": "catalog.schema.docs_index",
        "endpoint_name": "my_endpoint"
      },
      "keywords": ["docs", "documentation", "guide"]
    }
  ]
}
```

### Step 2: Generate Supervisor
```bash
python scripts/create_supervisor.py my_supervisor \
  --config agents.json \
  --routing llm \
  -o ./supervisors
```

### Step 3: Run Supervisor
```bash
python supervisors/my_supervisor.py "What were Q4 sales?"
```

## 🎉 Benefits

- ⚡ **Smart routing**: LLM understands user intent
- 🎯 **Specialized agents**: Each agent is an expert in its domain
- 🔧 **Flexible**: Easy to add/remove agents
- 📊 **Observable**: MLflow tracing built-in
- 🚀 **Production-ready**: Error handling and fallback logic
- 🔌 **Extensible**: Custom agent types supported

## 📊 Example Workflows

### Workflow 1: Sales + Documentation
```
1. User: "How do I analyze Q4 sales?"
2. Supervisor analyzes query → Two parts: data query + documentation
3. Routes to sales_agent: Gets Q4 sales data
4. Routes to docs_agent: Finds analysis guides
5. Combines results: "Q4 sales were $5M. Here's how to analyze..."
```

### Workflow 2: Multi-Domain Query
```
1. User: "Compare our sales to industry benchmarks"
2. Supervisor routes to sales_agent: Gets internal sales data
3. Supervisor routes to research_agent: Gets industry benchmarks
4. Synthesizes: "Your sales: $5M. Industry average: $4.2M (+19%)"
```

### Workflow 3: Sequential Analysis
```
1. User: "Analyze customer churn"
2. Planner creates sequence:
   - data_agent: Get churn data
   - analysis_agent: Calculate metrics
   - insight_agent: Identify patterns
   - recommendation_agent: Suggest actions
3. Executes in order, each building on previous results
4. Returns comprehensive analysis with recommendations
```

## 🔍 Routing Strategies

### LLM-Based Routing (Recommended)
```python
# Supervisor uses LLM to understand query semantics
routing_strategy="llm"

# User: "What were sales last quarter?"
# LLM understands: "sales" → routes to sales_agent

# User: "How do I create a dashboard?"
# LLM understands: documentation question → routes to docs_agent
```

### Rule-Based Routing
```python
# Supervisor uses keyword matching
routing_strategy="rules"

# Agents have keyword lists
sales_agent.keywords = ["sales", "revenue", "customers"]
docs_agent.keywords = ["documentation", "tutorial", "guide"]

# Fast but less flexible
```

## 🔧 Custom Agent Integration

### Creating a Custom Agent
```python
def my_custom_executor(config: Dict[str, Any], query: str) -> str:
    """Custom agent implementation."""
    # Your logic here
    # - Call external APIs
    # - Query databases
    # - Use ML models
    # - Combine multiple sources

    api_endpoint = config["api_endpoint"]
    result = call_external_api(api_endpoint, query)
    return format_result(result)

# Register with orchestrator
orchestrator.register_agent_executor("my_agent", my_custom_executor)
```

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check LangGraph supervisor documentation
- Review Databricks multi-agent docs

---

**Ready to get started?** Upload `langgraph-multi-agent-supervisor.zip` to Claude and start building multi-agent systems!
