# Databricks Notebook Structure Reference

This document describes the structure and conventions for Databricks notebooks that support both local IDE and workspace development.

## File Format

Databricks notebooks in `.py` format use special comment markers to define cells:

```python
# Databricks notebook source       # File header (required)
# MAGIC %md                         # Markdown cell marker
# MAGIC # Title                     # Markdown content (prefixed with # MAGIC)

# COMMAND ----------              # Cell separator

# Regular Python code             # Code cell
print("Hello World")

# COMMAND ----------              # Next cell separator
```

## Environment Detection Pattern

All generated notebooks include this pattern for dual-environment support:

```python
from src.utils.dev_utils import is_running_in_databricks
import os

if not is_running_in_databricks():
    # Local IDE environment
    from databricks.connect import DatabricksSession

    # Clear conflicting environment variables
    for env_var in ['DATABRICKS_AUTH_TYPE', 'DATABRICKS_METADATA_SERVICE_URL', 'DATABRICKS_SERVERLESS_COMPUTE_ID']:
        os.environ.pop(env_var, None)

    # Connect using profile
    profile = "your_profile_name"
    spark = DatabricksSession.builder.profile(profile).getOrCreate()
else:
    # Databricks workspace environment
    # spark is already available
    pass
```

## Notebook Types

### Agent Development Notebooks

**Purpose**: Build and test LangGraph-based AI agents

**Key imports**:
- `langgraph.graph` - For agent graph construction
- `langchain_core.messages` - For message handling
- `databricks_langchain.ChatDatabricks` - For Databricks LLM integration
- `mlflow` - For agent logging and deployment

**Typical workflow**:
1. Define agent state schema
2. Create agent nodes and edges
3. Build and compile the graph
4. Test locally with sample inputs
5. Log to MLflow for deployment

### ML/AI Notebooks

**Purpose**: Train, evaluate, and deploy machine learning models

**Key imports**:
- `pyspark.ml` - For Spark ML pipelines
- `mlflow.spark` - For model logging
- ML-specific libraries (sklearn, xgboost, etc.)

**Typical workflow**:
1. Load and prepare data
2. Feature engineering
3. Model training
4. Evaluation and validation
5. MLflow logging and registration

### ETL Pipeline Notebooks

**Purpose**: Extract, transform, and load data

**Key imports**:
- `pyspark.sql.functions` - For transformations
- `pyspark.sql.types` - For schema definitions

**Typical workflow**:
1. Extract from source tables/files
2. Apply transformations
3. Load to target tables
4. Data quality checks

### General Purpose Notebooks

**Purpose**: Flexible notebooks for any development task

**Includes**: Common imports and placeholder cells for custom workflows

## Local Development Setup

### Prerequisites

1. **Databricks Connect**: Installed via `uv` or `pip`
   ```bash
   uv add databricks-connect
   ```

2. **Profile Configuration**: `~/.databrickscfg` file with profile settings
   ```ini
   [your_profile_name]
   host = https://your-workspace.cloud.databricks.com
   token = dapi...
   ```

3. **Utility Function**: `src/utils/dev_utils.py` with `is_running_in_databricks()`

### Running Locally

1. Open notebook in VS Code or your preferred IDE
2. Run cells interactively using Jupyter extension
3. Spark session automatically connects to Databricks using your profile
4. All Databricks resources (tables, volumes, MLflow) are accessible

### Running in Databricks

1. Upload notebook to Databricks workspace
2. Attach to a cluster
3. Run cells - environment is automatically detected
4. No code changes needed

## Best Practices

1. **Always use environment detection** - Ensures notebooks work in both environments
2. **Clear conflicting env vars** - Prevents authentication issues locally
3. **Use profile-based auth** - More secure than hardcoded tokens
4. **Add descriptive comments** - Help collaborators understand cell purposes
5. **Test locally first** - Faster iteration than running in workspace
6. **Use MLflow for tracking** - Works seamlessly in both environments

## Common Patterns

### Loading Configuration

```python
import yaml

with open("./config.yaml", "r") as file:
    config = yaml.safe_load(file)

catalog = config["databricks_config"]["catalog"]
schema = config["databricks_config"]["schema"]
```

### Table Operations

```python
# Read table
df = spark.table(f"{catalog}.{schema}.{table_name}")

# Write table
df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{target_table}")
```

### MLflow Integration

```python
import mlflow

# Works in both environments
with mlflow.start_run():
    mlflow.log_param("param_name", value)
    mlflow.log_metric("metric_name", score)
    mlflow.langchain.log_model(agent, "agent_model")
```

## Troubleshooting

### Connection Issues

If you encounter "Failed to connect to Databricks":
1. Verify profile exists in `~/.databrickscfg`
2. Check token validity
3. Ensure no conflicting environment variables
4. Verify network connectivity to workspace

### Import Errors

If imports fail locally:
1. Ensure all dependencies are installed (`uv sync`)
2. Check Python path includes project root
3. Verify `src/utils/dev_utils.py` exists

### Spark Session Issues

If spark session doesn't initialize:
1. Check Databricks Connect version compatibility
2. Verify cluster/serverless compute is accessible
3. Review profile configuration in `~/.databrickscfg`
