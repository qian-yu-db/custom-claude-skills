# Databricks Local Notebook Skill - Quick Reference

## What It Does
Generates Databricks notebooks (.py) with automatic local IDE support via Databricks Connect.

## When to Use
- Creating AI agent development notebooks
- Building ML/AI training notebooks
- Developing ETL data pipelines
- Need notebooks that work locally and in workspace
- Want automatic environment detection

## Basic Command
```bash
scripts/generate_notebook.py NOTEBOOK_NAME \
  --type TYPE \
  --profile PROFILE_NAME
```

## Quick Examples

### Agent Development
```bash
scripts/generate_notebook.py customer_support_agent \
  --type agent \
  --profile e2_demo_fieldeng
```

### ML Training
```bash
scripts/generate_notebook.py churn_prediction \
  --type ml \
  --profile my_profile
```

### ETL Pipeline
```bash
scripts/generate_notebook.py data_pipeline \
  --type etl
```

### General Purpose
```bash
scripts/generate_notebook.py data_analysis \
  --type general
```

## Script Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `notebook_name` | - | Name of notebook (required) | - |
| `--type` | `-t` | Type: agent, ml, etl, general | agent |
| `--profile` | `-p` | Databricks profile name | (prompts if not provided) |
| `--output-dir` | `-o` | Output directory | current directory |
| `--no-examples` | - | Skip example code cells | false |

## Notebook Types

### Agent (`--type agent`)
**For**: LangGraph agents, chatbots, agentic workflows

**Includes**:
- LangGraph/LangChain imports
- ChatDatabricks integration
- MLflow logging
- Agent state/node/graph starter code

**Best for**: AI agent development with LLMs

### ML (`--type ml`)
**For**: Machine learning training and evaluation

**Includes**:
- Spark ML imports
- MLflow model tracking
- Training/evaluation starter code

**Best for**: Model development and experimentation

### ETL (`--type etl`)
**For**: Data pipelines and transformations

**Includes**:
- PySpark transformations
- Schema utilities
- Extract-Transform-Load structure

**Best for**: Data engineering workflows

### General (`--type general`)
**For**: Exploratory analysis, custom workflows

**Includes**:
- Common PySpark/pandas imports
- Flexible placeholders

**Best for**: Ad-hoc analysis and exploration

## Generated Notebook Structure

All notebooks contain:

1. **Header** (Markdown)
   - Title
   - Description

2. **Environment Setup** (Code)
   - Automatic detection (local vs workspace)
   - Databricks Connect configuration
   - Profile-based authentication

3. **Type-Specific Cells** (Code)
   - Imports for chosen type
   - Starter code examples

4. **Placeholder Cells** (Code/Markdown)
   - For custom development

## Environment Detection

### Automatic Behavior

**When Running Locally** (VS Code, PyCharm):
```
🔧 Running in local IDE - setting up Databricks Connect
✅ Connected to Databricks using profile: your_profile
```

**When Running in Workspace**:
```
🏢 Running in Databricks workspace
```

### How It Works
```python
from src.utils.dev_utils import is_running_in_databricks

if not is_running_in_databricks():
    # Local: Use Databricks Connect
    from databricks.connect import DatabricksSession
    spark = DatabricksSession.builder.profile(profile).getOrCreate()
else:
    # Workspace: Use existing Spark session
    pass
```

## Prerequisites

### 1. Install Databricks Connect
```bash
pip install databricks-connect
# or
uv add databricks-connect
```

### 2. Configure Profile
Add to `~/.databrickscfg`:
```ini
[your_profile_name]
host = https://your-workspace.cloud.databricks.com
token = dapi...
```

### 3. Create Utility Function
Create `src/utils/dev_utils.py`:
```python
def is_running_in_databricks():
    """Detect if running in Databricks workspace"""
    import os
    return 'DATABRICKS_RUNTIME_VERSION' in os.environ
```

## Common Workflows

### 1. Generate Notebook
```bash
scripts/generate_notebook.py my_notebook --type agent --profile dev
```

### 2. Open in IDE
```bash
code my_notebook.py  # VS Code
# or
pycharm my_notebook.py  # PyCharm
```

### 3. Run Locally
- Notebook auto-connects to Databricks
- Access workspace tables, MLflow, Unity Catalog
- Develop with live data

### 4. Deploy to Workspace (Optional)
- Upload via UI, CLI, or DAB
- Runs without modification

## Advanced Usage

### Custom Output Directory
```bash
scripts/generate_notebook.py my_notebook \
  --type ml \
  --output-dir ./notebooks
```

### Minimal Notebook (No Examples)
```bash
scripts/generate_notebook.py minimal \
  --type general \
  --no-examples
```

### Generate Multiple Notebooks
```bash
for name in agent_1 agent_2 agent_3; do
  scripts/generate_notebook.py $name \
    --type agent \
    --profile e2_demo_fieldeng
done
```

### Specify Profile at Runtime
```bash
# Don't specify --profile
# Script will prompt:
scripts/generate_notebook.py my_notebook --type ml
# Enter profile name: [user inputs profile]
```

## Integration with DAB

Generated notebooks work with Databricks Asset Bundles:

```yaml
resources:
  jobs:
    my_job:
      tasks:
        - task_key: my_task
          notebook_task:
            notebook_path: ./notebooks/my_notebook.py
```

Deploy:
```bash
databricks bundle deploy -t dev
databricks bundle run my_job -t dev
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Profile not found | Check `~/.databrickscfg` has correct profile |
| Connection timeout | Verify workspace URL and token validity |
| Import errors | Run `uv sync` or `pip install` dependencies |
| dev_utils not found | Create `src/utils/dev_utils.py` with detection function |
| Permission errors | Check token permissions in workspace |
| Spark session error | Ensure no conflicting Spark installations |

## Common Issues

### Local Development
```bash
# Clear conflicting env vars if needed
unset DATABRICKS_AUTH_TYPE
unset DATABRICKS_METADATA_SERVICE_URL
unset DATABRICKS_SERVERLESS_COMPUTE_ID
```

### Profile Issues
```bash
# List available profiles
cat ~/.databrickscfg | grep "^\["

# Test profile connection
databricks fs ls dbfs:/ --profile your_profile
```

### Dependencies
```bash
# Install all dependencies
uv sync

# Or specific packages
uv add databricks-connect langchain langgraph mlflow
```

## File Format

### Databricks Python Notebook (.py)
```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook Title

# COMMAND ----------

# Code cell 1

# COMMAND ----------

# Code cell 2
```

**Benefits**:
- Works in Databricks workspace
- Works with Databricks Connect locally
- Version control friendly (pure Python)
- Easy to diff and merge

## Best Practices

✅ **Do:**
- Use descriptive notebook names
- Specify correct notebook type
- Test locally before deploying
- Use profile for environment-specific config
- Keep notebooks focused

✗ **Avoid:**
- Generic names (notebook1, test)
- Hardcoding credentials
- Mixing multiple concerns
- Skipping local testing
- Large monolithic notebooks

## Quick Command Reference

### Generate Agent Notebook
```bash
scripts/generate_notebook.py my_agent -t agent -p dev
```

### Generate ML Notebook
```bash
scripts/generate_notebook.py my_model -t ml -p prod
```

### Generate ETL Notebook
```bash
scripts/generate_notebook.py my_etl -t etl -p dev
```

### Generate Minimal Notebook
```bash
scripts/generate_notebook.py minimal -t general --no-examples
```

### Generate to Specific Directory
```bash
scripts/generate_notebook.py my_nb -t agent -o ./notebooks
```

## Environment Variables

The script handles these automatically:

```python
# Cleared for local development
DATABRICKS_AUTH_TYPE
DATABRICKS_METADATA_SERVICE_URL
DATABRICKS_SERVERLESS_COMPUTE_ID

# Used for detection
DATABRICKS_RUNTIME_VERSION  # Present in workspace only
```

## Profile Configuration

### ~/.databrickscfg Format
```ini
[profile_name]
host = https://workspace.cloud.databricks.com
token = dapi1234567890abcdef...

[another_profile]
host = https://another-workspace.cloud.databricks.com
token = dapi9876543210fedcba...
```

### Get Token
1. Go to Databricks workspace
2. Settings → User Settings → Access Tokens
3. Generate New Token
4. Copy and add to `~/.databrickscfg`

## Next Steps After Generation

1. **Open in IDE** - Start coding locally
2. **Test connection** - Run the environment setup cell
3. **Develop** - Write your code with live Databricks access
4. **Test locally** - Verify functionality
5. **Deploy** - Upload to workspace or use DAB

## Related Documentation

- Full details: `USAGE_GUIDE.md`
- Package overview: `README.md`
- Notebook structure: `references/notebook_structure.md`
- API reference: `references/api_reference.md`

## Quick Tips

💡 **Profile Management**
- Use different profiles for dev/staging/prod
- Keep tokens secure
- Rotate tokens regularly

💡 **Local Development**
- Use virtual environments
- Install dependencies first
- Test with small datasets locally

💡 **Notebook Organization**
- One notebook per logical task
- Use descriptive names
- Group related notebooks in directories

💡 **Version Control**
- Commit .py notebooks to git
- Review diffs before merging
- Use meaningful commit messages
