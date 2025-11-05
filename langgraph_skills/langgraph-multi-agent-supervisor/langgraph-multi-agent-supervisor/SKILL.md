# LangGraph Multi-Agent Supervisor Skill

## Purpose

This skill helps Claude build LangGraph multi-agent systems with a supervisor that orchestrates specialized worker agents. The supervisor intelligently routes user queries to the appropriate agent (Genie agents, RAG agents, MCP tool agents, etc.) and manages the overall conversation flow.

## When to Activate

This skill should activate when the user requests:
- "Create a multi-agent system with a supervisor"
- "Build a LangGraph supervisor that routes to different agents"
- "Set up agent orchestration with Genie and RAG agents"
- "Create a supervisor pattern with specialized worker agents"
- "Build a multi-agent system that routes queries to appropriate experts"
- "Orchestrate multiple agents with a central supervisor"

## Core Capabilities

### 1. Supervisor Architecture
- Centralized routing logic
- LLM-powered agent selection
- State management across agents
- Result aggregation and formatting

### 2. Worker Agent Integration
- Genie API agents (data queries)
- RAG agents (document retrieval)
- MCP tool agents (external tools)
- Custom function agents
- Hybrid agent combinations

### 3. Routing Strategies
- LLM-based routing (semantic understanding)
- Rule-based routing (keywords/patterns)
- Sequential routing (multi-step workflows)
- Parallel routing (concurrent execution)

### 4. State Management
- Shared state across agents
- Agent-specific state
- Conversation history
- Result caching

## Supervisor Patterns

### Pattern 1: Simple Supervisor

Basic supervisor that routes to one agent at a time:

```python
from typing import TypedDict, Annotated, Sequence, Literal
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from databricks_langchain import ChatDatabricks
import mlflow


# Supervisor State
class SupervisorState(TypedDict):
    """State for supervisor and all worker agents."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str  # Which agent to route to
    agent_results: dict  # Results from each agent
    final_response: str


# Define worker agents
WORKER_AGENTS = {
    "sales_agent": {
        "description": "Handles sales data queries, revenue reports, and customer analytics",
        "type": "genie",
        "space_id": "sales_space_123"
    },
    "docs_agent": {
        "description": "Searches documentation, tutorials, and technical guides",
        "type": "rag",
        "index_name": "catalog.schema.docs_index"
    },
    "support_agent": {
        "description": "Handles customer support, tickets, and issue tracking",
        "type": "mcp",
        "tools": ["get_ticket", "create_ticket", "update_ticket"]
    }
}


# Initialize LLM
llm = ChatDatabricks(
    endpoint=os.getenv("DATABRICKS_LLM_ENDPOINT", "databricks-meta-llama-3-1-70b-instruct"),
    temperature=0.1
)


def supervisor_node(state: SupervisorState) -> SupervisorState:
    """
    Supervisor analyzes query and routes to appropriate worker agent.
    """
    user_query = state["messages"][-1].content

    # Format agent descriptions for LLM
    agent_list = "\n".join([
        f"- {name}: {info['description']}"
        for name, info in WORKER_AGENTS.items()
    ])

    routing_prompt = f"""You are a supervisor coordinating specialized agents.

Available agents:
{agent_list}

User query: {user_query}

Which agent should handle this query? Respond with ONLY the agent name.
If no agent is appropriate, respond with "general".
"""

    response = llm.invoke(routing_prompt)
    selected_agent = response.content.strip().lower()

    # Validate selection
    if selected_agent not in WORKER_AGENTS and selected_agent != "general":
        selected_agent = "general"

    print(f"Supervisor routing to: {selected_agent}")

    return {"next_agent": selected_agent}


def create_worker_node(agent_name: str, agent_config: dict):
    """
    Factory function to create worker agent nodes.
    """
    def worker_node(state: SupervisorState) -> SupervisorState:
        """Worker agent processes the query."""
        user_query = state["messages"][-1].content

        try:
            # Route based on agent type
            if agent_config["type"] == "genie":
                result = query_genie_agent(agent_config["space_id"], user_query)
            elif agent_config["type"] == "rag":
                result = query_rag_agent(agent_config["index_name"], user_query)
            elif agent_config["type"] == "mcp":
                result = query_mcp_agent(agent_config["tools"], user_query)
            else:
                result = f"Unknown agent type: {agent_config['type']}"

            # Store result
            agent_results = state.get("agent_results", {})
            agent_results[agent_name] = result

            return {
                "messages": [AIMessage(content=result)],
                "agent_results": agent_results,
                "final_response": result
            }

        except Exception as e:
            error_msg = f"Error in {agent_name}: {str(e)}"
            return {
                "messages": [AIMessage(content=error_msg)],
                "final_response": error_msg
            }

    return worker_node


def general_node(state: SupervisorState) -> SupervisorState:
    """Handle general queries without routing to specialized agents."""
    user_query = state["messages"][-1].content

    response = llm.invoke(f"Answer this general question: {user_query}")

    return {
        "messages": [AIMessage(content=response.content)],
        "final_response": response.content
    }


def create_supervisor_agent():
    """Build the supervisor multi-agent system."""

    # Create graph
    graph = StateGraph(SupervisorState)

    # Add supervisor
    graph.add_node("supervisor", supervisor_node)

    # Add worker agents
    for agent_name, agent_config in WORKER_AGENTS.items():
        worker_fn = create_worker_node(agent_name, agent_config)
        graph.add_node(agent_name, worker_fn)
        graph.add_edge(agent_name, END)  # Workers end after execution

    # Add general agent
    graph.add_node("general", general_node)
    graph.add_edge("general", END)

    # Routing function
    def route_to_agent(state: SupervisorState) -> str:
        """Route to the selected agent."""
        return state["next_agent"]

    # Set up conditional routing
    routes = {name: name for name in WORKER_AGENTS.keys()}
    routes["general"] = "general"

    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", route_to_agent, routes)

    # Compile
    return graph.compile()
```

### Pattern 2: Hierarchical Supervisor

Supervisor with sub-supervisors for complex domains:

```python
class HierarchicalState(TypedDict):
    """State for hierarchical multi-agent system."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_domain: str  # High-level domain (data/docs/support)
    current_agent: str   # Specific agent
    agent_results: dict
    final_response: str


def main_supervisor_node(state: HierarchicalState) -> HierarchicalState:
    """Top-level supervisor routes to domain supervisors."""
    user_query = state["messages"][-1].content

    domain_prompt = f"""Categorize this query into a domain:

Query: {user_query}

Domains:
- data: Sales, revenue, analytics, metrics
- docs: Documentation, tutorials, guides
- support: Customer issues, tickets, troubleshooting

Respond with domain name only."""

    response = llm.invoke(domain_prompt)
    domain = response.content.strip().lower()

    return {"current_domain": domain}


def data_supervisor_node(state: HierarchicalState) -> HierarchicalState:
    """Data domain supervisor routes to data agents."""
    user_query = state["messages"][-1].content

    # Route to specific data agent (sales/finance/inventory)
    agent_prompt = f"""Which data agent should handle this?

Query: {user_query}

Agents:
- sales: Revenue, customers, deals
- finance: Budgets, expenses, forecasts
- inventory: Stock levels, orders

Agent name only:"""

    response = llm.invoke(agent_prompt)
    agent = response.content.strip().lower()

    return {"current_agent": f"data_{agent}"}


def docs_supervisor_node(state: HierarchicalState) -> HierarchicalState:
    """Docs domain supervisor routes to doc agents."""
    user_query = state["messages"][-1].content

    # Route to specific docs agent (api/tutorials/guides)
    # Implementation similar to data_supervisor_node
    ...


# Build hierarchical graph
def create_hierarchical_supervisor():
    graph = StateGraph(HierarchicalState)

    # Add main supervisor
    graph.add_node("main_supervisor", main_supervisor_node)

    # Add domain supervisors
    graph.add_node("data_supervisor", data_supervisor_node)
    graph.add_node("docs_supervisor", docs_supervisor_node)
    graph.add_node("support_supervisor", support_supervisor_node)

    # Add worker agents for each domain
    # data_sales_agent, data_finance_agent, etc.
    ...

    # Complex routing logic
    def route_from_main(state):
        return f"{state['current_domain']}_supervisor"

    def route_from_domain(state):
        return state["current_agent"]

    graph.set_entry_point("main_supervisor")
    graph.add_conditional_edges("main_supervisor", route_from_main)
    # Add more edges...

    return graph.compile()
```

### Pattern 3: Sequential Multi-Agent

Agents execute in sequence, each building on previous results:

```python
class SequentialState(TypedDict):
    """State for sequential agent execution."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agent_sequence: list  # Ordered list of agents to execute
    current_index: int    # Current position in sequence
    agent_results: dict   # Results from each agent
    final_response: str


def planner_node(state: SequentialState) -> SequentialState:
    """Plan which agents to execute and in what order."""
    user_query = state["messages"][-1].content

    planning_prompt = f"""Plan which agents to use for this complex task:

Query: {user_query}

Available agents:
- research_agent: Searches documentation
- analysis_agent: Analyzes data from Genie
- synthesis_agent: Combines information
- formatting_agent: Formats final response

Return agent names in order, one per line:"""

    response = llm.invoke(planning_prompt)
    agent_sequence = [a.strip() for a in response.content.split("\n") if a.strip()]

    print(f"Planned sequence: {agent_sequence}")

    return {
        "agent_sequence": agent_sequence,
        "current_index": 0
    }


def execute_agent_node(state: SequentialState) -> SequentialState:
    """Execute the current agent in the sequence."""
    current_index = state["current_index"]
    agent_sequence = state["agent_sequence"]

    if current_index >= len(agent_sequence):
        # Sequence complete
        return state

    agent_name = agent_sequence[current_index]
    user_query = state["messages"][-1].content
    previous_results = state.get("agent_results", {})

    # Build context from previous agents
    context = "\n".join([
        f"{name}: {result}"
        for name, result in previous_results.items()
    ])

    # Execute agent with context
    result = execute_agent(agent_name, user_query, context)

    # Store result
    previous_results[agent_name] = result

    return {
        "agent_results": previous_results,
        "current_index": current_index + 1
    }


def should_continue(state: SequentialState) -> str:
    """Determine if more agents should execute."""
    if state["current_index"] >= len(state["agent_sequence"]):
        return "finalize"
    return "execute_agent"


def finalize_node(state: SequentialState) -> SequentialState:
    """Synthesize results from all agents."""
    agent_results = state["agent_results"]

    # Combine all results
    combined = "\n\n".join([
        f"**{name}**:\n{result}"
        for name, result in agent_results.items()
    ])

    return {
        "messages": [AIMessage(content=combined)],
        "final_response": combined
    }


# Build sequential graph
def create_sequential_supervisor():
    graph = StateGraph(SequentialState)

    graph.add_node("planner", planner_node)
    graph.add_node("execute_agent", execute_agent_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "execute_agent")
    graph.add_conditional_edges("execute_agent", should_continue, {
        "execute_agent": "execute_agent",
        "finalize": "finalize"
    })
    graph.add_edge("finalize", END)

    return graph.compile()
```

### Pattern 4: Parallel Multi-Agent

Execute multiple agents concurrently and aggregate results:

```python
class ParallelState(TypedDict):
    """State for parallel agent execution."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agents_to_execute: list  # Agents to run in parallel
    agent_results: dict      # Results from each agent
    aggregated_response: str


def dispatch_node(state: ParallelState) -> ParallelState:
    """Determine which agents should execute in parallel."""
    user_query = state["messages"][-1].content

    dispatch_prompt = f"""Which agents should work on this query? Select all that apply.

Query: {user_query}

Agents:
- sales_agent: Sales data
- marketing_agent: Marketing metrics
- customer_agent: Customer data

Return agent names (comma-separated):"""

    response = llm.invoke(dispatch_prompt)
    agents = [a.strip() for a in response.content.split(",")]

    print(f"Dispatching to agents: {agents}")

    return {"agents_to_execute": agents}


def parallel_executor_node(state: ParallelState) -> ParallelState:
    """Execute all agents in parallel."""
    import concurrent.futures

    agents = state["agents_to_execute"]
    user_query = state["messages"][-1].content

    def execute_single_agent(agent_name):
        """Execute one agent."""
        try:
            return agent_name, execute_agent(agent_name, user_query)
        except Exception as e:
            return agent_name, f"Error: {str(e)}"

    # Execute in parallel
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = [executor.submit(execute_single_agent, agent) for agent in agents]
        for future in concurrent.futures.as_completed(futures):
            agent_name, result = future.result()
            results[agent_name] = result

    return {"agent_results": results}


def aggregator_node(state: ParallelState) -> ParallelState:
    """Aggregate results from all parallel agents."""
    agent_results = state["agent_results"]
    user_query = state["messages"][-1].content

    # Format all results
    formatted_results = "\n\n".join([
        f"**{name.upper()}**:\n{result}"
        for name, result in agent_results.items()
    ])

    # Use LLM to synthesize
    synthesis_prompt = f"""Synthesize these results into a coherent answer.

Original question: {user_query}

Agent results:
{formatted_results}

Synthesized answer:"""

    response = llm.invoke(synthesis_prompt)

    return {
        "messages": [AIMessage(content=response.content)],
        "aggregated_response": response.content
    }


# Build parallel graph
def create_parallel_supervisor():
    graph = StateGraph(ParallelState)

    graph.add_node("dispatch", dispatch_node)
    graph.add_node("parallel_executor", parallel_executor_node)
    graph.add_node("aggregator", aggregator_node)

    graph.set_entry_point("dispatch")
    graph.add_edge("dispatch", "parallel_executor")
    graph.add_edge("parallel_executor", "aggregator")
    graph.add_edge("aggregator", END)

    return graph.compile()
```

## Worker Agent Implementations

### Genie Agent Integration

```python
from genie_client import GenieClient, format_as_markdown_table

genie_client = GenieClient()

def query_genie_agent(space_id: str, query: str) -> str:
    """Execute query against Genie space."""
    try:
        # Query Genie
        message = genie_client.start_conversation(space_id, query)

        # Extract and format data
        data = genie_client.extract_data(message)
        table = format_as_markdown_table(data)

        # Generate summary
        summary_prompt = f"""Summarize these results:

{table}

Summary:"""
        summary = llm.invoke(summary_prompt).content

        return f"{summary}\n\n**Detailed Results:**\n{table}"

    except Exception as e:
        return f"Genie agent error: {str(e)}"
```

### RAG Agent Integration

```python
from vector_search_retriever import create_retriever

def query_rag_agent(index_name: str, query: str) -> str:
    """Execute RAG query against Vector Search index."""
    try:
        # Create retriever
        retriever = create_retriever(
            index_name=index_name,
            endpoint_name=os.getenv("VS_ENDPOINT"),
            num_results=5
        )

        # Retrieve documents
        docs = retriever.get_relevant_documents(query)

        # Format context
        context = "\n\n".join([
            f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])

        # Generate answer
        rag_prompt = f"""Answer using these documents:

Context:
{context}

Question: {query}

Answer:"""

        answer = llm.invoke(rag_prompt).content
        return answer

    except Exception as e:
        return f"RAG agent error: {str(e)}"
```

### MCP Tool Agent Integration

```python
def query_mcp_agent(tools: list, query: str) -> str:
    """Execute query using MCP tools."""
    try:
        # Bind tools to LLM
        tool_instances = [get_tool(tool_name) for tool_name in tools]
        llm_with_tools = llm.bind_tools(tool_instances)

        # LLM decides which tools to use
        response = llm_with_tools.invoke(query)

        # Execute tool calls
        if hasattr(response, "tool_calls") and response.tool_calls:
            results = []
            for tool_call in response.tool_calls:
                tool_result = execute_tool(tool_call)
                results.append(tool_result)

            # Format results
            return "\n".join(results)
        else:
            return response.content

    except Exception as e:
        return f"MCP agent error: {str(e)}"
```

## Configuration Management

### Agent Configuration File

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
    },
    "support_agent": {
      "type": "mcp",
      "description": "Customer support and ticketing",
      "config": {
        "tools": ["get_ticket", "create_ticket", "update_ticket"]
      }
    },
    "general_agent": {
      "type": "llm",
      "description": "General questions and conversation",
      "config": {
        "model": "databricks-meta-llama-3-1-70b-instruct"
      }
    }
  },
  "supervisor": {
    "routing_strategy": "llm",  # or "rules", "sequential", "parallel"
    "enable_fallback": true,
    "default_agent": "general_agent",
    "max_iterations": 10
  }
}
```

### Loading Configuration

```python
import json

def load_agent_config(config_path: str) -> dict:
    """Load agent configuration from JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def create_agents_from_config(config: dict) -> dict:
    """Create agent nodes from configuration."""
    agents = {}

    for agent_name, agent_spec in config["agents"].items():
        agent_type = agent_spec["type"]
        agent_config = agent_spec["config"]

        # Create appropriate agent
        if agent_type == "genie":
            agent_fn = lambda state: query_genie_agent(
                agent_config["space_id"],
                state["messages"][-1].content
            )
        elif agent_type == "rag":
            agent_fn = lambda state: query_rag_agent(
                agent_config["index_name"],
                state["messages"][-1].content
            )
        elif agent_type == "mcp":
            agent_fn = lambda state: query_mcp_agent(
                agent_config["tools"],
                state["messages"][-1].content
            )
        else:
            agent_fn = lambda state: "Unknown agent type"

        agents[agent_name] = agent_fn

    return agents
```

## Advanced Features

### Result Caching

```python
from functools import lru_cache
import hashlib

def cache_key(agent_name: str, query: str) -> str:
    """Generate cache key."""
    return hashlib.md5(f"{agent_name}:{query}".encode()).hexdigest()

@lru_cache(maxsize=100)
def cached_agent_execution(agent_name: str, query: str) -> str:
    """Execute agent with caching."""
    return execute_agent(agent_name, query)
```

### Agent Health Monitoring

```python
def health_check_node(state: SupervisorState) -> SupervisorState:
    """Check health of all agents before routing."""
    healthy_agents = []

    for agent_name in WORKER_AGENTS.keys():
        if is_agent_healthy(agent_name):
            healthy_agents.append(agent_name)
        else:
            print(f"Agent {agent_name} is unhealthy, skipping")

    state["healthy_agents"] = healthy_agents
    return state
```

### Fallback Handling

```python
def supervisor_with_fallback(state: SupervisorState) -> SupervisorState:
    """Supervisor with fallback if primary agent fails."""
    primary_agent = select_agent(state["messages"][-1].content)

    state["next_agent"] = primary_agent
    state["fallback_agents"] = get_fallback_agents(primary_agent)

    return state

def execute_with_fallback(state: SupervisorState) -> SupervisorState:
    """Execute agent with fallback logic."""
    try:
        result = execute_agent(state["next_agent"], state["messages"][-1].content)
        return {"final_response": result}
    except Exception as e:
        # Try fallback agents
        for fallback_agent in state.get("fallback_agents", []):
            try:
                result = execute_agent(fallback_agent, state["messages"][-1].content)
                return {"final_response": result}
            except:
                continue

        return {"final_response": "All agents failed"}
```

## MLflow Integration

```python
import mlflow

def create_supervisor_with_tracking():
    """Create supervisor with MLflow tracking."""

    # Enable auto-logging
    mlflow.langchain.autolog()

    supervisor = create_supervisor_agent()

    def tracked_invoke(initial_state):
        with mlflow.start_run():
            # Log configuration
            mlflow.log_param("num_agents", len(WORKER_AGENTS))
            mlflow.log_param("routing_strategy", "llm")

            # Execute
            result = supervisor.invoke(initial_state)

            # Log results
            mlflow.log_metric("num_messages", len(result["messages"]))
            mlflow.log_param("selected_agent", result.get("next_agent", "unknown"))

            return result

    supervisor.invoke = tracked_invoke
    return supervisor
```

## Best Practices

1. **Agent Design**:
   - Keep agents focused and specialized
   - Clear agent descriptions for routing
   - Handle errors gracefully
   - Return consistent result format

2. **Routing Logic**:
   - Use semantic routing (LLM) for flexibility
   - Add rule-based routing for known patterns
   - Implement fallback routing
   - Log routing decisions

3. **State Management**:
   - Keep shared state minimal
   - Use agent-specific state for details
   - Clear state between conversations
   - Handle concurrent access

4. **Performance**:
   - Cache agent results
   - Use parallel execution when possible
   - Implement timeouts
   - Monitor agent health

5. **Observability**:
   - Enable MLflow tracing
   - Log routing decisions
   - Track agent execution time
   - Monitor error rates

## Common Patterns Summary

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Simple Supervisor | Single agent selection | Easy to implement | No multi-step workflows |
| Hierarchical | Complex domains | Scalable organization | More complex setup |
| Sequential | Multi-step workflows | Results build on each other | Slower execution |
| Parallel | Independent queries | Faster execution | More complex aggregation |

## References

- Databricks Multi-Agent Framework: https://docs.databricks.com/generative-ai/agent-framework/multi-agent-genie
- LangGraph Supervisor: https://github.com/langchain-ai/langgraph-supervisor-py
- LangChain Supervisor Docs: https://docs.langchain.com/oss/python/langchain/supervisor
