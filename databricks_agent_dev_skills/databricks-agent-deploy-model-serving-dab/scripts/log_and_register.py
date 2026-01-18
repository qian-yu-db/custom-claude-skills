#!/usr/bin/env python3
"""
Log and register an AI agent to MLflow and Unity Catalog

This script helps you log different types of agents (LangGraph, OpenAI, custom)
to MLflow and register them in Unity Catalog for deployment.

Usage:
    python log_and_register.py \\
        --agent-path src/agent/agent.py \\
        --model-name main.agents.my_agent \\
        --agent-type langgraph

Requirements:
    - mlflow
    - databricks-agents
    - Agent framework (langchain, langgraph, openai, etc.)
"""

import argparse
import os
import sys
from pathlib import Path


def log_langgraph_agent(
    agent_path: str,
    model_name: str,
    experiment_name: str,
    pip_requirements: list,
    resources: list = None,
    input_example: dict = None
):
    """Log a LangGraph agent to MLflow"""
    import mlflow

    print(f"Logging LangGraph agent from: {agent_path}")

    mlflow.set_experiment(experiment_name)

    # Default input example
    if input_example is None:
        input_example = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ]
        }

    # Default resources
    if resources is None:
        resources = []

    with mlflow.start_run(run_name=f"{model_name.split('.')[-1]}-deployment"):
        logged_model = mlflow.langchain.log_model(
            lc_model=agent_path,
            artifact_path="agent",
            input_example=input_example,
            pip_requirements=pip_requirements,
            resources=resources
        )

        model_uri = logged_model.model_uri
        print(f"✓ Agent logged to: {model_uri}")

        # Register model
        print(f"Registering model: {model_name}")
        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        print(f"✓ Model registered: {model_name} version {registered_model.version}")

        return {
            "model_uri": model_uri,
            "model_name": model_name,
            "version": registered_model.version,
            "run_id": mlflow.active_run().info.run_id
        }


def log_openai_agent(
    agent_class_path: str,
    model_name: str,
    experiment_name: str,
    pip_requirements: list,
    model_config: dict = None,
    input_example: dict = None
):
    """Log an OpenAI SDK agent to MLflow"""
    import mlflow
    import importlib.util

    print(f"Logging OpenAI agent from: {agent_class_path}")

    # Import the agent class
    spec = importlib.util.spec_from_file_location("agent_module", agent_class_path)
    agent_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_module)

    # Assume the agent class is the first PythonModel subclass
    agent_class = None
    for item_name in dir(agent_module):
        item = getattr(agent_module, item_name)
        if (isinstance(item, type) and
            issubclass(item, mlflow.pyfunc.PythonModel) and
            item != mlflow.pyfunc.PythonModel):
            agent_class = item
            break

    if agent_class is None:
        raise ValueError("No PythonModel subclass found in agent file")

    mlflow.set_experiment(experiment_name)

    # Default input example
    if input_example is None:
        input_example = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }

    with mlflow.start_run(run_name=f"{model_name.split('.')[-1]}-deployment"):
        mlflow.pyfunc.log_model(
            artifact_path="agent",
            python_model=agent_class(),
            pip_requirements=pip_requirements,
            input_example=input_example,
            model_config=model_config or {}
        )

        model_uri = mlflow.get_artifact_uri("agent")
        print(f"✓ Agent logged to: {model_uri}")

        # Register model
        print(f"Registering model: {model_name}")
        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        print(f"✓ Model registered: {model_name} version {registered_model.version}")

        return {
            "model_uri": model_uri,
            "model_name": model_name,
            "version": registered_model.version,
            "run_id": mlflow.active_run().info.run_id
        }


def log_custom_agent(
    agent_class_path: str,
    model_name: str,
    experiment_name: str,
    pip_requirements: list,
    input_example: dict = None,
    model_config: dict = None
):
    """Log a custom agent (pyfunc) to MLflow"""
    # Same as OpenAI agent for now
    return log_openai_agent(
        agent_class_path,
        model_name,
        experiment_name,
        pip_requirements,
        model_config,
        input_example
    )


def main():
    parser = argparse.ArgumentParser(
        description="Log and register an AI agent to MLflow and Unity Catalog"
    )

    parser.add_argument(
        "--agent-path",
        required=True,
        help="Path to agent code (Python file)"
    )

    parser.add_argument(
        "--model-name",
        required=True,
        help="Unity Catalog model name (catalog.schema.model_name)"
    )

    parser.add_argument(
        "--agent-type",
        choices=["langgraph", "openai", "custom"],
        default="langgraph",
        help="Type of agent framework"
    )

    parser.add_argument(
        "--experiment-name",
        help="MLflow experiment name (auto-generated if not provided)"
    )

    parser.add_argument(
        "--pip-requirements",
        nargs="+",
        help="Additional pip requirements (space-separated)"
    )

    parser.add_argument(
        "--llm-endpoint",
        help="Databricks LLM endpoint name (for resource tracking)"
    )

    parser.add_argument(
        "--vector-search-index",
        help="Databricks Vector Search index name (for resource tracking)"
    )

    args = parser.parse_args()

    # Validate agent path exists
    if not Path(args.agent_path).exists():
        print(f"Error: Agent path does not exist: {args.agent_path}")
        sys.exit(1)

    # Generate experiment name if not provided
    if args.experiment_name is None:
        username = os.environ.get("USER", "user")
        agent_name = args.model_name.split(".")[-1]
        args.experiment_name = f"/Users/{username}/agent-experiments/{agent_name}"

    # Build pip requirements
    base_requirements = [
        "mlflow>=2.10.0",
        "databricks-agents>=0.1.0",
    ]

    if args.agent_type == "langgraph":
        base_requirements.extend([
            "langchain>=0.1.0",
            "langgraph>=0.0.20",
            "databricks-langchain>=0.1.0",
        ])
    elif args.agent_type == "openai":
        base_requirements.extend([
            "openai>=1.0.0",
        ])

    # Add custom requirements
    if args.pip_requirements:
        base_requirements.extend(args.pip_requirements)

    # Build resources list
    resources = []
    if args.llm_endpoint:
        resources.append({
            "databricks_serving_endpoint": {
                "name": args.llm_endpoint
            }
        })

    if args.vector_search_index:
        resources.append({
            "databricks_vector_search_index": {
                "index_name": args.vector_search_index
            }
        })

    # Log and register based on agent type
    try:
        if args.agent_type == "langgraph":
            result = log_langgraph_agent(
                agent_path=args.agent_path,
                model_name=args.model_name,
                experiment_name=args.experiment_name,
                pip_requirements=base_requirements,
                resources=resources if resources else None
            )
        elif args.agent_type == "openai":
            result = log_openai_agent(
                agent_class_path=args.agent_path,
                model_name=args.model_name,
                experiment_name=args.experiment_name,
                pip_requirements=base_requirements
            )
        elif args.agent_type == "custom":
            result = log_custom_agent(
                agent_class_path=args.agent_path,
                model_name=args.model_name,
                experiment_name=args.experiment_name,
                pip_requirements=base_requirements
            )

        print("\n=== Success ===")
        print(f"Model Name: {result['model_name']}")
        print(f"Version: {result['version']}")
        print(f"Run ID: {result['run_id']}")
        print(f"Model URI: {result['model_uri']}")
        print("\nNext steps:")
        print(f"1. Update databricks.yml with model version: {result['version']}")
        print(f"2. Deploy using: ./scripts/deploy.sh [target] [profile]")

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
