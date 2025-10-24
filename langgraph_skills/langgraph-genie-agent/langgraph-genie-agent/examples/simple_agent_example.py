"""
Simple Genie Agent Example

This example shows how to create a basic LangGraph agent that queries a Genie space.
"""

import os
from typing import TypedDict, Annotated, Sequence, Optional
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import mlflow

# Import Genie client (assumes genie_client.py is in the same directory or installed)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from genie_client import GenieClient, format_as_markdown_table


# Define agent state
class SimpleAgentState(TypedDict):
    """State for simple Genie agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    genie_space_id: str
    query_result: Optional[dict]


# Initialize Genie client
genie_client = GenieClient()


def query_genie_node(state: SimpleAgentState) -> SimpleAgentState:
    """Query Genie and format response."""
    user_query = state["messages"][-1].content
    space_id = state["genie_space_id"]

    print(f"Querying Genie space '{space_id}'...")

    try:
        # Query Genie
        message = genie_client.start_conversation(space_id, user_query)

        # Extract data
        data = genie_client.extract_data(message)

        # Format as markdown table
        table = format_as_markdown_table(data)

        # Create response
        response = f"Here are the results:\n\n{table}"

        return {
            "query_result": data,
            "messages": [AIMessage(content=response)]
        }

    except Exception as e:
        error_response = f"Error querying Genie: {str(e)}"
        return {
            "messages": [AIMessage(content=error_response)]
        }


# Build agent graph
def create_simple_agent(space_id: str):
    """Create a simple Genie agent."""

    # Create graph
    graph = StateGraph(SimpleAgentState)

    # Add node
    graph.add_node("query_genie", query_genie_node)

    # Set entry and exit
    graph.set_entry_point("query_genie")
    graph.add_edge("query_genie", END)

    # Compile
    return graph.compile()


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python simple_agent_example.py <space_id> <query>")
        print("\nExample:")
        print('  python simple_agent_example.py abc123 "What were Q4 sales?"')
        sys.exit(1)

    space_id = sys.argv[1]
    query = sys.argv[2]

    # Enable MLflow tracing
    mlflow.langchain.autolog()

    # Create agent
    print("Creating Genie agent...")
    agent = create_simple_agent(space_id)

    # Run agent
    print(f"\nQuery: {query}\n")

    with mlflow.start_run():
        result = agent.invoke({
            "messages": [HumanMessage(content=query)],
            "genie_space_id": space_id,
            "query_result": None
        })

        # Print response
        print("\nAgent Response:")
        print("=" * 60)
        print(result["messages"][-1].content)
        print("=" * 60)

        # Log to MLflow
        mlflow.log_param("genie_space_id", space_id)
        mlflow.log_param("query", query)
        if result.get("query_result"):
            row_count = result["query_result"].get("row_count", 0)
            mlflow.log_metric("result_row_count", row_count)

    print("\n✓ Done!")
