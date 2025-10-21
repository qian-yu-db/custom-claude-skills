---
name: databricks-local-notebook
description: Generate Databricks notebooks (.py) with local IDE development support using Databricks Connect. This skill should be used when creating new notebooks for AI agent development, ML/AI workflows, or ETL pipelines that need to work both locally (in VS Code/PyCharm) and in Databricks workspace. Automatically includes dual-environment detection and setup code.
---

# Databricks Local Notebook Generator

Generate Databricks notebook files that seamlessly work in both local IDEs (with Databricks Connect) and Databricks workspace, eliminating the need for manual environment configuration.

## Overview

This skill creates Databricks notebooks (.py format) with built-in environment detection that automatically:
- Connects to Databricks when running locally using Databricks Connect
- Uses the existing Spark session when running in Databricks workspace
- Handles authentication via profiles (from `~/.databrickscfg`)
- Includes type-specific starter code for agent development, ML/AI, ETL, or general workflows

## When to Use This Skill

Use this skill when:
- Starting a new AI agent development project with LangGraph
- Creating ML/AI notebooks for model training and evaluation
- Building ETL data pipelines
- Need to develop Databricks notebooks locally in your IDE
- Want notebooks that work in both local and workspace environments without code changes

## Quick Start

### Basic Usage

Generate an AI agent development notebook:
```bash
scripts/generate_notebook.py my_agent_name --type agent --profile e2_demo_fieldeng
```

Generate an ML notebook:
```bash
scripts/generate_notebook.py model_training --type ml --profile your_profile
```

Generate without specifying profile (will prompt at runtime):
```bash
scripts/generate_notebook.py data_analysis --type general
```

### Script Parameters

- `notebook_name` (required): Name of the notebook (converted to snake_case)
- `--type, -t`: Type of notebook (`agent`, `ml`, `etl`, `general`) - default: `agent`
- `--profile, -p`: Databricks profile name from `~/.databrickscfg` (optional - will prompt if not provided)
- `--output-dir, -o`: Output directory - default: current directory
- `--no-examples`: Skip example code cells (just include empty placeholders)

## Notebook Types

### Agent Development (`--type agent`)

**Best for**: LangGraph-based AI agents, agentic workflows, chatbots

**Includes**:
- LangGraph and LangChain imports
- ChatDatabricks for LLM integration
- MLflow for agent logging
- Starter code for agent state, nodes, and graph construction

**Example**:
```bash
scripts/generate_notebook.py customer_support_agent --type agent --profile e2_demo_fieldeng
```

### ML/AI (`--type ml`)

**Best for**: Machine learning model training, evaluation, and deployment

**Includes**:
- Spark ML pipeline imports
- MLflow model logging setup
- Starter code for data prep, training, and evaluation

**Example**:
```bash
scripts/generate_notebook.py churn_prediction --type ml --profile my_profile
```

### ETL Pipeline (`--type etl`)

**Best for**: Data ingestion, transformation, and loading workflows

**Includes**:
- PySpark transformation functions
- Schema definition utilities
- Extract-Transform-Load workflow structure

**Example**:
```bash
scripts/generate_notebook.py customer_data_pipeline --type etl
```

### General Purpose (`--type general`)

**Best for**: Exploratory data analysis, custom workflows

**Includes**:
- Common PySpark and pandas imports
- Flexible placeholder cells for any use case

## Generated Notebook Structure

All generated notebooks include:

1. **Header cell**: Markdown title and description
2. **Environment setup cell**: Automatic detection and Databricks Connect configuration
3. **Type-specific cells**: Starter code based on notebook type
4. **Placeholder cells**: For custom development

### Environment Setup (Included in All Notebooks)

```python
from src.utils.dev_utils import is_running_in_databricks
import os

if not is_running_in_databricks():
    print("🔧 Running in local IDE - setting up Databricks Connect")
    from databricks.connect import DatabricksSession

    # Clear conflicting environment variables
    for env_var in ['DATABRICKS_AUTH_TYPE', 'DATABRICKS_METADATA_SERVICE_URL', 'DATABRICKS_SERVERLESS_COMPUTE_ID']:
        os.environ.pop(env_var, None)

    # Connect using profile
    profile = "your_profile_name"  # or prompt for input
    spark = DatabricksSession.builder.profile(profile).getOrCreate()
    print(f"✅ Connected to Databricks using profile: {profile}")
else:
    print("🏢 Running in Databricks workspace")
```

## Prerequisites

Before using this skill, ensure:

1. **Databricks Connect installed**:
   ```bash
   uv add databricks-connect
   ```

2. **Profile configured** in `~/.databrickscfg`:
   ```ini
   [your_profile_name]
   host = https://your-workspace.cloud.databricks.com
   token = dapi...
   ```

3. **Utility function exists** at `src/utils/dev_utils.py`:
   ```python
   def is_running_in_databricks():
       """Detect if code is running in Databricks workspace"""
       # Implementation checks for Databricks environment variables
   ```

## Workflow

1. **Generate notebook** using the script with desired parameters
2. **Open in IDE** (VS Code, PyCharm, etc.)
3. **Develop locally** - Spark connects to Databricks automatically
4. **Test with Databricks resources** - Access tables, volumes, MLflow, etc.
5. **Upload to workspace** (optional) - Works without modification

## Advanced Usage

### Custom Output Directory

```bash
scripts/generate_notebook.py my_notebook --type agent --output-dir ./notebooks
```

### Minimal Notebook (No Examples)

```bash
scripts/generate_notebook.py minimal_notebook --type general --no-examples
```

### Multiple Notebooks with Same Profile

```bash
# Set profile once, generate multiple notebooks
for name in agent_1 agent_2 agent_3; do
    scripts/generate_notebook.py $name --type agent --profile e2_demo_fieldeng
done
```

## Troubleshooting

**"Profile not found" error**:
- Verify profile exists in `~/.databrickscfg`
- Check profile name spelling

**Connection timeout**:
- Verify workspace URL is accessible
- Check token validity
- Ensure no VPN/network restrictions

**Import errors locally**:
- Run `uv sync` to install dependencies
- Verify `src/utils/dev_utils.py` exists
- Check Python path includes project root

## Reference Documentation

For detailed information about notebook structure, conventions, and best practices, see:
- `references/notebook_structure.md` - Complete guide to Databricks notebook format and patterns

## Integration with Databricks Asset Bundles

Generated notebooks can be used in Databricks Asset Bundles (DAB):

1. Generate notebooks using this skill
2. Reference them in `databricks.yml`:
   ```yaml
   resources:
     jobs:
       my_job:
         tasks:
           - task_key: my_task
             notebook_task:
               notebook_path: ./notebooks/my_notebook.py
   ```
3. Deploy with `databricks bundle deploy`

The environment detection ensures notebooks work whether executed via DAB jobs or locally in your IDE.
