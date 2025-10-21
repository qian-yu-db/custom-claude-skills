#!/usr/bin/env python3
"""
Generate Databricks notebook (.py) files with local IDE development support.

This script creates notebooks that work both locally (with Databricks Connect)
and in Databricks workspace, supporting AI agent and ML/AI development workflows.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional


def generate_notebook(
    notebook_name: str,
    notebook_type: str = "agent",
    profile_name: Optional[str] = None,
    output_dir: str = ".",
    include_examples: bool = True
) -> str:
    """
    Generate a Databricks notebook with local IDE development support.

    Args:
        notebook_name: Name of the notebook (without .py extension)
        notebook_type: Type of notebook ('agent', 'ml', 'etl', 'general')
        profile_name: Databricks profile name for local development
        output_dir: Directory where the notebook will be created
        include_examples: Whether to include example code cells

    Returns:
        Path to the generated notebook file
    """

    # Ensure notebook name uses snake_case
    notebook_name = notebook_name.replace(" ", "_").replace("-", "_").lower()
    filename = f"{notebook_name}.py"
    output_path = os.path.join(output_dir, filename)

    # Generate notebook title (convert snake_case to Title Case)
    title = " ".join(word.capitalize() for word in notebook_name.split("_"))

    # Build notebook content
    content = generate_notebook_content(
        title=title,
        notebook_type=notebook_type,
        profile_name=profile_name,
        include_examples=include_examples
    )

    # Write to file
    with open(output_path, 'w') as f:
        f.write(content)

    return output_path


def generate_notebook_content(
    title: str,
    notebook_type: str,
    profile_name: Optional[str],
    include_examples: bool
) -> str:
    """Generate the complete notebook content as a string."""

    # Get type-specific description and example cells
    description, example_cells = get_type_specific_content(notebook_type)

    # Build the notebook content
    lines = []

    # Header cell
    lines.extend([
        "# Databricks notebook source",
        "# MAGIC %md",
        f"# MAGIC # {title}",
        f"# MAGIC {description}",
        f"# MAGIC",
        f"# MAGIC ## Setup",
        f"# MAGIC - Works locally with Databricks Connect",
        f"# MAGIC - Works in Databricks workspace",
        f"# MAGIC - Automatic environment detection",
        "",
        "# COMMAND ----------",
        ""
    ])

    # Environment setup cell
    lines.extend([
        "# Environment setup - works both locally and in Databricks",
        "from src.utils.dev_utils import is_running_in_databricks",
        "import os",
        "",
        "if not is_running_in_databricks():",
        "    print(\"🔧 Running in local IDE - setting up Databricks Connect\")",
        "    from databricks.connect import DatabricksSession",
        "    ",
        "    # Clear any conflicting environment variables",
        "    for env_var in ['DATABRICKS_AUTH_TYPE', 'DATABRICKS_METADATA_SERVICE_URL', 'DATABRICKS_SERVERLESS_COMPUTE_ID']:",
        "        os.environ.pop(env_var, None)",
        "    ",
    ])

    if profile_name:
        lines.extend([
            f"    # Use the specified Databricks profile",
            f"    profile = \"{profile_name}\"",
            f"    spark = DatabricksSession.builder.profile(profile).getOrCreate()",
            f"    print(f\"✅ Connected to Databricks using profile: {{profile}}\")",
        ])
    else:
        lines.extend([
            "    # Prompt for Databricks profile name",
            "    profile = input(\"Enter Databricks profile name (from ~/.databrickscfg): \")",
            "    spark = DatabricksSession.builder.profile(profile).getOrCreate()",
            "    print(f\"✅ Connected to Databricks using profile: {profile}\")",
        ])

    lines.extend([
        "else:",
        "    print(\"🏢 Running in Databricks workspace\")",
        "",
        "# COMMAND ----------",
        ""
    ])

    # Add example cells if requested
    if include_examples:
        lines.extend(example_cells)
    else:
        # Add empty placeholder cells
        for i in range(3):
            lines.extend([
                f"# TODO: Add your code here",
                "",
                "# COMMAND ----------",
                ""
            ])

    return "\n".join(lines)


def get_type_specific_content(notebook_type: str) -> tuple[str, List[str]]:
    """
    Get notebook description and example cells based on type.

    Returns:
        Tuple of (description, example_cells)
    """

    if notebook_type == "agent":
        description = "AI Agent Development Notebook - Build and test LangGraph agents with local IDE support"
        example_cells = [
            "# Import agent development libraries",
            "from langgraph.graph import StateGraph, END",
            "from langchain_core.messages import HumanMessage, AIMessage",
            "from databricks_langchain import ChatDatabricks",
            "import mlflow",
            "",
            "# TODO: Define your agent state schema",
            "# TODO: Create agent nodes and edges",
            "# TODO: Build and compile the graph",
            "",
            "# COMMAND ----------",
            "",
            "# Test the agent locally",
            "# TODO: Create test inputs",
            "# TODO: Invoke the agent",
            "# TODO: Validate outputs",
            "",
            "# COMMAND ----------",
            "",
            "# Log agent to MLflow (works in both environments)",
            "# with mlflow.start_run():",
            "#     mlflow.langchain.log_model(...)",
            "",
            "# COMMAND ----------",
            ""
        ]

    elif notebook_type == "ml":
        description = "Machine Learning Development Notebook - Train, evaluate, and deploy ML models"
        example_cells = [
            "# Import ML libraries",
            "from pyspark.ml import Pipeline",
            "from pyspark.ml.feature import VectorAssembler",
            "from pyspark.ml.classification import RandomForestClassifier",
            "import mlflow",
            "import mlflow.spark",
            "",
            "# TODO: Load and prepare your data",
            "# df = spark.table(\"catalog.schema.table\")",
            "",
            "# COMMAND ----------",
            "",
            "# Feature engineering and model training",
            "# TODO: Define features and target",
            "# TODO: Create ML pipeline",
            "# TODO: Train model",
            "",
            "# COMMAND ----------",
            "",
            "# Model evaluation and logging",
            "# TODO: Evaluate model performance",
            "# TODO: Log model to MLflow",
            "",
            "# COMMAND ----------",
            ""
        ]

    elif notebook_type == "etl":
        description = "ETL Pipeline Notebook - Extract, transform, and load data workflows"
        example_cells = [
            "# Import ETL libraries",
            "from pyspark.sql.functions import col, when, lit, current_timestamp",
            "from pyspark.sql.types import StructType, StructField, StringType, IntegerType",
            "",
            "# TODO: Define your source and target tables",
            "# source_table = \"catalog.schema.source\"",
            "# target_table = \"catalog.schema.target\"",
            "",
            "# COMMAND ----------",
            "",
            "# Extract data",
            "# TODO: Read from source",
            "# df = spark.table(source_table)",
            "",
            "# COMMAND ----------",
            "",
            "# Transform data",
            "# TODO: Apply transformations",
            "# df_transformed = df.transform(...)",
            "",
            "# COMMAND ----------",
            "",
            "# Load data",
            "# TODO: Write to target",
            "# df_transformed.write.mode(\"overwrite\").saveAsTable(target_table)",
            "",
            "# COMMAND ----------",
            ""
        ]

    else:  # general
        description = "General Purpose Databricks Notebook - Flexible notebook for any development task"
        example_cells = [
            "# Import common libraries",
            "from pyspark.sql.functions import col, when, lit",
            "import pandas as pd",
            "",
            "# TODO: Add your imports here",
            "",
            "# COMMAND ----------",
            "",
            "# Data loading and exploration",
            "# TODO: Load your data",
            "# df = spark.table(\"catalog.schema.table\")",
            "",
            "# COMMAND ----------",
            "",
            "# Analysis and processing",
            "# TODO: Add your analysis code",
            "",
            "# COMMAND ----------",
            "",
            "# Results and output",
            "# TODO: Display or save results",
            "",
            "# COMMAND ----------",
            ""
        ]

    return description, example_cells


def main():
    parser = argparse.ArgumentParser(
        description="Generate Databricks notebooks with local IDE development support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate an agent development notebook with profile
  generate_notebook.py customer_sentiment_agent --type agent --profile e2_demo_fieldeng

  # Generate an ML notebook without examples
  generate_notebook.py model_training --type ml --no-examples

  # Generate a general notebook prompting for profile
  generate_notebook.py data_analysis --type general
        """
    )

    parser.add_argument(
        "notebook_name",
        help="Name of the notebook to generate (e.g., 'customer_sentiment_agent')"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["agent", "ml", "etl", "general"],
        default="agent",
        help="Type of notebook to generate (default: agent)"
    )
    parser.add_argument(
        "--profile", "-p",
        help="Databricks profile name for local development (from ~/.databrickscfg)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=".",
        help="Output directory for the notebook (default: current directory)"
    )
    parser.add_argument(
        "--no-examples",
        action="store_true",
        help="Don't include example code cells (just empty placeholders)"
    )

    args = parser.parse_args()

    # Generate the notebook
    try:
        output_path = generate_notebook(
            notebook_name=args.notebook_name,
            notebook_type=args.type,
            profile_name=args.profile,
            output_dir=args.output_dir,
            include_examples=not args.no_examples
        )

        print(f"✅ Generated Databricks notebook: {output_path}")
        print(f"   Type: {args.type}")
        if args.profile:
            print(f"   Profile: {args.profile}")
        else:
            print(f"   Profile: Will prompt at runtime")
        print(f"\nNext steps:")
        print(f"   1. Open {output_path} in your IDE")
        print(f"   2. Customize the notebook for your use case")
        print(f"   3. Run locally or upload to Databricks workspace")

    except Exception as e:
        print(f"❌ Error generating notebook: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
