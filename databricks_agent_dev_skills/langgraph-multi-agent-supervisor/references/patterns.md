# Supervisor Patterns - Implementation Reference

## Pattern 1: Simple Supervisor

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
    """Supervisor analyzes query and routes to appropriate worker agent."""
    user_query = state["messages"][-1].content

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

    if selected_agent not in WORKER_AGENTS and selected_agent != "general":
        selected_agent = "general"

    return {"next_agent": selected_agent}


def create_worker_node(agent_name: str, agent_config: dict):
    """Factory function to create worker agent nodes."""
    def worker_node(state: SupervisorState) -> SupervisorState:
        user_query = state["messages"][-1].content
        try:
            if agent_config["type"] == "genie":
                result = query_genie_agent(agent_config["space_id"], user_query)
            elif agent_config["type"] == "rag":
                result = query_rag_agent(agent_config["index_name"], user_query)
            elif agent_config["type"] == "mcp":
                result = query_mcp_agent(agent_config["tools"], user_query)
            else:
                result = f"Unknown agent type: {agent_config['type']}"

            agent_results = state.get("agent_results", {})
            agent_results[agent_name] = result
            return {
                "messages": [AIMessage(content=result)],
                "agent_results": agent_results,
                "final_response": result
            }
        except Exception as e:
            error_msg = f"Error in {agent_name}: {str(e)}"
            return {"messages": [AIMessage(content=error_msg)], "final_response": error_msg}

    return worker_node


def create_supervisor_agent():
    """Build the supervisor multi-agent system."""
    graph = StateGraph(SupervisorState)
    graph.add_node("supervisor", supervisor_node)

    for agent_name, agent_config in WORKER_AGENTS.items():
        worker_fn = create_worker_node(agent_name, agent_config)
        graph.add_node(agent_name, worker_fn)
        graph.add_edge(agent_name, END)

    graph.add_node("general", general_node)
    graph.add_edge("general", END)

    def route_to_agent(state: SupervisorState) -> str:
        return state["next_agent"]

    routes = {name: name for name in WORKER_AGENTS.keys()}
    routes["general"] = "general"

    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", route_to_agent, routes)

    return graph.compile()
```

## Pattern 2: Hierarchical Supervisor

Supervisor with sub-supervisors for complex domains:

```python
class HierarchicalState(TypedDict):
    """State for hierarchical multi-agent system."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_domain: str
    current_agent: str
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
    return {"current_domain": response.content.strip().lower()}


def data_supervisor_node(state: HierarchicalState) -> HierarchicalState:
    """Data domain supervisor routes to data agents."""
    user_query = state["messages"][-1].content
    agent_prompt = f"""Which data agent should handle this?
Query: {user_query}
Agents: sales, finance, inventory
Agent name only:"""
    response = llm.invoke(agent_prompt)
    return {"current_agent": f"data_{response.content.strip().lower()}"}


def create_hierarchical_supervisor():
    graph = StateGraph(HierarchicalState)
    graph.add_node("main_supervisor", main_supervisor_node)
    graph.add_node("data_supervisor", data_supervisor_node)
    graph.add_node("docs_supervisor", docs_supervisor_node)
    graph.add_node("support_supervisor", support_supervisor_node)
    # Add worker agents for each domain...

    def route_from_main(state):
        return f"{state['current_domain']}_supervisor"

    graph.set_entry_point("main_supervisor")
    graph.add_conditional_edges("main_supervisor", route_from_main)
    return graph.compile()
```

## Pattern 3: Sequential Multi-Agent

Agents execute in sequence, each building on previous results:

```python
class SequentialState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agent_sequence: list
    current_index: int
    agent_results: dict
    final_response: str


def planner_node(state: SequentialState) -> SequentialState:
    """Plan which agents to execute and in what order."""
    user_query = state["messages"][-1].content
    planning_prompt = f"""Plan which agents to use for this complex task:
Query: {user_query}
Available agents: research_agent, analysis_agent, synthesis_agent, formatting_agent
Return agent names in order, one per line:"""

    response = llm.invoke(planning_prompt)
    agent_sequence = [a.strip() for a in response.content.split("\n") if a.strip()]
    return {"agent_sequence": agent_sequence, "current_index": 0}


def execute_agent_node(state: SequentialState) -> SequentialState:
    """Execute the current agent in the sequence."""
    current_index = state["current_index"]
    if current_index >= len(state["agent_sequence"]):
        return state

    agent_name = state["agent_sequence"][current_index]
    context = "\n".join([f"{name}: {result}" for name, result in state.get("agent_results", {}).items()])
    result = execute_agent(agent_name, state["messages"][-1].content, context)

    previous_results = state.get("agent_results", {})
    previous_results[agent_name] = result
    return {"agent_results": previous_results, "current_index": current_index + 1}


def should_continue(state: SequentialState) -> str:
    if state["current_index"] >= len(state["agent_sequence"]):
        return "finalize"
    return "execute_agent"


def create_sequential_supervisor():
    graph = StateGraph(SequentialState)
    graph.add_node("planner", planner_node)
    graph.add_node("execute_agent", execute_agent_node)
    graph.add_node("finalize", finalize_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "execute_agent")
    graph.add_conditional_edges("execute_agent", should_continue, {
        "execute_agent": "execute_agent", "finalize": "finalize"
    })
    graph.add_edge("finalize", END)
    return graph.compile()
```

## Pattern 4: Parallel Multi-Agent

Execute multiple agents concurrently and aggregate results:

```python
class ParallelState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    agents_to_execute: list
    agent_results: dict
    aggregated_response: str


def dispatch_node(state: ParallelState) -> ParallelState:
    """Determine which agents should execute in parallel."""
    user_query = state["messages"][-1].content
    dispatch_prompt = f"""Which agents should work on this query? Select all that apply.
Query: {user_query}
Agents: sales_agent, marketing_agent, customer_agent
Return agent names (comma-separated):"""
    response = llm.invoke(dispatch_prompt)
    agents = [a.strip() for a in response.content.split(",")]
    return {"agents_to_execute": agents}


def parallel_executor_node(state: ParallelState) -> ParallelState:
    """Execute all agents in parallel."""
    import concurrent.futures
    agents = state["agents_to_execute"]
    user_query = state["messages"][-1].content

    def execute_single_agent(agent_name):
        try:
            return agent_name, execute_agent(agent_name, user_query)
        except Exception as e:
            return agent_name, f"Error: {str(e)}"

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = [executor.submit(execute_single_agent, agent) for agent in agents]
        for future in concurrent.futures.as_completed(futures):
            agent_name, result = future.result()
            results[agent_name] = result
    return {"agent_results": results}


def aggregator_node(state: ParallelState) -> ParallelState:
    """Aggregate results from all parallel agents."""
    formatted_results = "\n\n".join([
        f"**{name.upper()}**:\n{result}"
        for name, result in state["agent_results"].items()
    ])
    synthesis_prompt = f"""Synthesize these results into a coherent answer.
Original question: {state["messages"][-1].content}
Agent results:
{formatted_results}"""
    response = llm.invoke(synthesis_prompt)
    return {"messages": [AIMessage(content=response.content)], "aggregated_response": response.content}


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
