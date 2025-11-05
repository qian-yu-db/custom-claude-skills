#!/usr/bin/env python3
"""
Multi-Agent Supervisor Orchestrator

This module provides a flexible supervisor that can orchestrate multiple
specialized worker agents (Genie, RAG, MCP, etc.).
"""

import os
import json
from typing import TypedDict, Annotated, Sequence, Literal, Dict, Any, Callable, Optional
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from databricks_langchain import ChatDatabricks
from pydantic import BaseModel


class SupervisorState(TypedDict):
    """State shared across supervisor and all worker agents."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str  # Which agent to route to
    agent_results: Dict[str, Any]  # Results from each agent
    final_response: str
    metadata: Dict[str, Any]  # Additional metadata


class AgentConfig(BaseModel):
    """Configuration for a worker agent."""
    name: str
    type: str  # "genie", "rag", "mcp", "llm", "custom"
    description: str
    config: Dict[str, Any]
    enabled: bool = True


class SupervisorOrchestrator:
    """
    Main orchestrator for multi-agent systems.

    This class manages agent registration, routing, and execution.
    """

    def __init__(
        self,
        agents: Dict[str, AgentConfig],
        routing_strategy: str = "llm",
        llm_endpoint: Optional[str] = None,
        enable_fallback: bool = True,
        default_agent: str = "general",
        verbose: bool = False
    ):
        """
        Initialize the supervisor orchestrator.

        Args:
            agents: Dictionary of agent configurations
            routing_strategy: "llm", "rules", "sequential", or "parallel"
            llm_endpoint: Databricks LLM endpoint name
            enable_fallback: Enable fallback to default agent on errors
            default_agent: Default agent for fallback
            verbose: Enable verbose logging
        """
        self.agents = agents
        self.routing_strategy = routing_strategy
        self.enable_fallback = enable_fallback
        self.default_agent = default_agent
        self.verbose = verbose

        # Initialize LLM
        self.llm = ChatDatabricks(
            endpoint=llm_endpoint or os.getenv(
                "DATABRICKS_LLM_ENDPOINT",
                "databricks-meta-llama-3-1-70b-instruct"
            ),
            temperature=0.1
        )

        # Agent executor functions
        self.agent_executors: Dict[str, Callable] = {}

        # Build the graph
        self.graph = None

    def register_agent_executor(self, agent_name: str, executor_fn: Callable):
        """
        Register an executor function for an agent.

        Args:
            agent_name: Name of the agent
            executor_fn: Function to execute the agent
                         Signature: executor_fn(config: dict, query: str) -> str
        """
        self.agent_executors[agent_name] = executor_fn

        if self.verbose:
            print(f"Registered executor for agent: {agent_name}")

    def _supervisor_node(self, state: SupervisorState) -> SupervisorState:
        """
        Supervisor node that routes to appropriate worker agent.
        """
        user_query = state["messages"][-1].content

        if self.routing_strategy == "llm":
            return self._llm_routing(user_query, state)
        elif self.routing_strategy == "rules":
            return self._rule_based_routing(user_query, state)
        else:
            raise ValueError(f"Unknown routing strategy: {self.routing_strategy}")

    def _llm_routing(self, query: str, state: SupervisorState) -> SupervisorState:
        """Use LLM to select appropriate agent."""

        # Filter enabled agents
        enabled_agents = {
            name: agent for name, agent in self.agents.items()
            if agent.enabled
        }

        # Format agent descriptions
        agent_list = "\n".join([
            f"- {name}: {agent.description}"
            for name, agent in enabled_agents.items()
        ])

        routing_prompt = f"""You are a supervisor coordinating specialized agents.

Available agents:
{agent_list}

User query: {query}

Instructions:
1. Analyze the user's query carefully
2. Select the MOST appropriate agent
3. Respond with ONLY the agent name
4. If no agent is appropriate, respond with "{self.default_agent}"

Agent name:"""

        response = self.llm.invoke(routing_prompt)
        selected_agent = response.content.strip().lower()

        # Validate selection
        if selected_agent not in enabled_agents:
            if self.verbose:
                print(f"Invalid agent '{selected_agent}', using default")
            selected_agent = self.default_agent

        if self.verbose:
            print(f"Supervisor routing to: {selected_agent}")

        return {"next_agent": selected_agent}

    def _rule_based_routing(self, query: str, state: SupervisorState) -> SupervisorState:
        """Use keyword rules to select agent."""
        query_lower = query.lower()

        # Simple keyword matching
        for agent_name, agent in self.agents.items():
            if not agent.enabled:
                continue

            keywords = agent.config.get("keywords", [])
            if any(keyword.lower() in query_lower for keyword in keywords):
                if self.verbose:
                    print(f"Rule-based routing to: {agent_name}")
                return {"next_agent": agent_name}

        # No match, use default
        if self.verbose:
            print(f"No rule match, using default: {self.default_agent}")
        return {"next_agent": self.default_agent}

    def _create_worker_node(self, agent_name: str, agent: AgentConfig):
        """
        Factory function to create worker agent nodes.
        """
        def worker_node(state: SupervisorState) -> SupervisorState:
            """Execute the worker agent."""
            user_query = state["messages"][-1].content

            try:
                # Get executor function
                if agent_name not in self.agent_executors:
                    raise ValueError(f"No executor registered for agent: {agent_name}")

                executor_fn = self.agent_executors[agent_name]

                # Execute agent
                if self.verbose:
                    print(f"Executing agent: {agent_name}")

                result = executor_fn(agent.config, user_query)

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

                if self.verbose:
                    print(error_msg)

                # Try fallback if enabled
                if self.enable_fallback and agent_name != self.default_agent:
                    if self.verbose:
                        print(f"Trying fallback to: {self.default_agent}")

                    try:
                        fallback_agent = self.agents[self.default_agent]
                        fallback_executor = self.agent_executors[self.default_agent]
                        result = fallback_executor(fallback_agent.config, user_query)

                        return {
                            "messages": [AIMessage(content=result)],
                            "final_response": result
                        }
                    except:
                        pass

                return {
                    "messages": [AIMessage(content=error_msg)],
                    "final_response": error_msg
                }

        return worker_node

    def build(self) -> StateGraph:
        """
        Build the supervisor graph.

        Returns:
            Compiled LangGraph StateGraph
        """
        # Create graph
        graph = StateGraph(SupervisorState)

        # Add supervisor node
        graph.add_node("supervisor", self._supervisor_node)

        # Add worker agent nodes
        for agent_name, agent in self.agents.items():
            if not agent.enabled:
                continue

            worker_fn = self._create_worker_node(agent_name, agent)
            graph.add_node(agent_name, worker_fn)
            graph.add_edge(agent_name, END)

        # Routing function
        def route_to_agent(state: SupervisorState) -> str:
            """Route to the selected agent."""
            return state["next_agent"]

        # Set up conditional routing
        routes = {name: name for name, agent in self.agents.items() if agent.enabled}

        graph.set_entry_point("supervisor")
        graph.add_conditional_edges("supervisor", route_to_agent, routes)

        # Compile and store
        self.graph = graph.compile()
        return self.graph

    def invoke(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the supervisor with a user query.

        Args:
            query: User query string
            **kwargs: Additional state parameters

        Returns:
            Final state dictionary
        """
        if self.graph is None:
            raise RuntimeError("Graph not built. Call build() first.")

        initial_state = {
            "messages": [HumanMessage(content=query)],
            "next_agent": "",
            "agent_results": {},
            "final_response": "",
            "metadata": kwargs
        }

        result = self.graph.invoke(initial_state)
        return result

    @classmethod
    def from_config_file(cls, config_path: str, **kwargs) -> "SupervisorOrchestrator":
        """
        Create orchestrator from JSON configuration file.

        Args:
            config_path: Path to JSON config file
            **kwargs: Additional arguments for SupervisorOrchestrator

        Returns:
            Configured SupervisorOrchestrator instance
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Parse agents
        agents = {}
        for agent_name, agent_spec in config.get("agents", {}).items():
            agents[agent_name] = AgentConfig(
                name=agent_name,
                type=agent_spec["type"],
                description=agent_spec["description"],
                config=agent_spec.get("config", {}),
                enabled=agent_spec.get("enabled", True)
            )

        # Get supervisor config
        supervisor_config = config.get("supervisor", {})

        return cls(
            agents=agents,
            routing_strategy=supervisor_config.get("routing_strategy", "llm"),
            enable_fallback=supervisor_config.get("enable_fallback", True),
            default_agent=supervisor_config.get("default_agent", "general"),
            **kwargs
        )


# Built-in agent executors

def genie_agent_executor(config: Dict[str, Any], query: str) -> str:
    """Execute Genie agent."""
    try:
        from genie_client import GenieClient, format_as_markdown_table

        space_id = config["space_id"]
        client = GenieClient()

        # Query Genie
        message = client.start_conversation(space_id, query)
        data = client.extract_data(message)
        table = format_as_markdown_table(data)

        return f"Query results:\n\n{table}"

    except ImportError:
        return "Genie client not available. Please ensure genie_client.py is in your path."
    except Exception as e:
        return f"Genie agent error: {str(e)}"


def rag_agent_executor(config: Dict[str, Any], query: str) -> str:
    """Execute RAG agent."""
    try:
        from vector_search_retriever import create_retriever
        from databricks_langchain import ChatDatabricks

        index_name = config["index_name"]
        endpoint_name = config.get("endpoint_name", os.getenv("VS_ENDPOINT"))

        # Create retriever
        retriever = create_retriever(
            index_name=index_name,
            endpoint_name=endpoint_name,
            num_results=config.get("num_results", 5)
        )

        # Retrieve documents
        docs = retriever.get_relevant_documents(query)

        # Format context
        context = "\n\n".join([
            f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
            for doc in docs
        ])

        # Generate answer
        llm = ChatDatabricks(endpoint=config.get("llm_endpoint", "databricks-meta-llama-3-1-70b-instruct"))

        rag_prompt = f"""Answer using these documents:

Context:
{context}

Question: {query}

Answer:"""

        answer = llm.invoke(rag_prompt).content
        return answer

    except ImportError:
        return "RAG dependencies not available. Please ensure vector_search_retriever.py is in your path."
    except Exception as e:
        return f"RAG agent error: {str(e)}"


def llm_agent_executor(config: Dict[str, Any], query: str) -> str:
    """Execute simple LLM agent."""
    try:
        from databricks_langchain import ChatDatabricks

        llm = ChatDatabricks(
            endpoint=config.get("model", "databricks-meta-llama-3-1-70b-instruct"),
            temperature=config.get("temperature", 0.1)
        )

        system_message = config.get("system_message", "You are a helpful assistant.")
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=query)
        ]

        response = llm.invoke(messages)
        return response.content

    except Exception as e:
        return f"LLM agent error: {str(e)}"


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python supervisor_orchestrator.py <config.json> <query>")
        print("\nExample:")
        print('  python supervisor_orchestrator.py agents_config.json "What were Q4 sales?"')
        sys.exit(1)

    config_path = sys.argv[1]
    query = sys.argv[2]

    # Create orchestrator from config
    orchestrator = SupervisorOrchestrator.from_config_file(
        config_path,
        verbose=True
    )

    # Register built-in executors
    for agent_name, agent in orchestrator.agents.items():
        if agent.type == "genie":
            orchestrator.register_agent_executor(agent_name, genie_agent_executor)
        elif agent.type == "rag":
            orchestrator.register_agent_executor(agent_name, rag_agent_executor)
        elif agent.type == "llm":
            orchestrator.register_agent_executor(agent_name, llm_agent_executor)

    # Build graph
    orchestrator.build()

    # Execute query
    print(f"\nQuery: {query}\n")
    result = orchestrator.invoke(query)

    # Print result
    print("\nFinal Response:")
    print("=" * 60)
    print(result["final_response"])
    print("=" * 60)

    # Print routing info
    print(f"\nRouted to agent: {result.get('next_agent', 'unknown')}")
    print(f"Total messages: {len(result['messages'])}")
