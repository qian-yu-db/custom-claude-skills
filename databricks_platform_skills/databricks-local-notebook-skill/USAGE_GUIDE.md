# Databricks Local Notebook Skill - Usage Guide

## Overview

This skill generates Databricks notebooks (.py format) that seamlessly work in both local IDEs (with Databricks Connect) and Databricks workspace environments. It eliminates manual environment configuration and provides type-specific starter code for common use cases.

## Installation

1. Upload `databricks-local-notebook.zip` to Claude
2. The skill will be available for use in your conversations

## Basic Usage Examples

### Scenario 1: Simple Agent Development Notebook

You want to create an AI agent using LangGraph that uses Databricks LLMs.

**User prompt:**
```
Create a Databricks notebook for an AI agent called customer_support_agent
that will handle customer inquiries. Use profile e2_demo_fieldeng.
```

**Claude will:**
1. Generate `customer_support_agent.py`
2. Include LangGraph and ChatDatabricks setup
3. Add environment detection code
4. Provide starter code for agent state, nodes, and graph
5. Configure Databricks Connect with the specified profile

**Generated notebook includes:**
- Environment detection (local vs workspace)
- LangGraph imports and setup
- ChatDatabricks integration
- MLflow logging setup
- Example agent structure
- Placeholder cells for custom logic

**How to use:**
```bash
# Open in VS Code
code customer_support_agent.py

# Run cells - automatically connects to Databricks
# Develop your agent logic
# Test locally with live Databricks LLMs
```

### Scenario 2: ML Model Training Notebook

You need to train a machine learning model with MLflow tracking.

**User prompt:**
```
I need an ML notebook for customer churn prediction. Include MLflow tracking
and use my production profile called prod_ml.
```

**Claude will:**
1. Generate `customer_churn_prediction.py`
2. Include Spark ML imports
3. Add MLflow tracking setup
4. Provide starter code for data prep, training, evaluation
5. Configure connection to prod_ml profile

**Generated notebook includes:**
- Spark ML pipeline imports
- MLflow experiment tracking
- Data preparation examples
- Model training structure
- Evaluation metrics code
- Model logging to MLflow

**How to use:**
```bash
# Open in your IDE
code customer_churn_prediction.py

# Run locally
# Access training data from Databricks
# Train model with live compute
# Log to Databricks MLflow
```

### Scenario 3: ETL Pipeline Notebook

You're building a data pipeline for processing customer data.

**User prompt:**
```
Create an ETL notebook called customer_data_pipeline for ingesting
and transforming customer data from multiple sources.
```

**Claude will:**
1. Generate `customer_data_pipeline.py`
2. Include PySpark transformation utilities
3. Add schema definition helpers
4. Provide ETL workflow structure
5. Configure environment detection

**Generated notebook includes:**
- PySpark imports and utilities
- Schema definition examples
- Extract phase structure
- Transform functions
- Load operations
- Data quality checks

### Scenario 4: General Purpose Notebook

You need a flexible notebook for exploratory data analysis.

**User prompt:**
```
Create a general purpose notebook for analyzing sales data
in our data warehouse. Use the analytics profile.
```

**Claude will:**
1. Generate `sales_data_analysis.py`
2. Include common PySpark and pandas imports
3. Add flexible placeholder cells
4. Configure analytics profile connection

## Advanced Usage Examples

### Example 1: Multiple Notebooks for Pipeline

**User prompt:**
```
Create three notebooks for a data pipeline:
1. Agent notebook for data quality checking agent called data_quality_agent
2. ML notebook for anomaly detection called anomaly_detector
3. ETL notebook for data processing called data_processor

Use profile e2_demo_fieldeng for all.
```

**Claude will:**
Generate three separate notebooks, each with appropriate type-specific code.

### Example 2: Minimal Notebook Without Examples

**User prompt:**
```
Create a minimal ML notebook called quick_model without example code,
just the basic structure. Use profile dev.
```

**Claude will:**
Generate notebook with imports and structure but skip example cells.

### Example 3: Custom Output Directory

**User prompt:**
```
Create an agent notebook called recommendation_agent in the
./notebooks/agents/ directory. Use profile staging.
```

**Claude will:**
Generate notebook in specified directory path.

## Notebook Types Deep Dive

### Agent Development Notebooks

**Purpose**: Build LangGraph-based AI agents with Databricks LLMs

**Use cases:**
- Customer support chatbots
- Data analysis agents
- Document processing agents
- Multi-step reasoning workflows

**What you get:**
```python
# Imports
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState
from databricks_langchain import ChatDatabricks
import mlflow

# ChatDatabricks setup
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1
)

# Agent state definition
class AgentState(MessagesState):
    pass

# Node functions
def agent_node(state: AgentState):
    # Your logic here
    pass

# Graph construction
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
# ... more setup
```

**Best practices:**
- Use MLflow for agent logging
- Test with small prompts first
- Monitor token usage
- Version your prompts

### ML/AI Notebooks

**Purpose**: Train and evaluate machine learning models

**Use cases:**
- Classification models
- Regression models
- Clustering analysis
- Model experimentation

**What you get:**
```python
# Imports
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
import mlflow

# Data preparation
feature_cols = ['feature1', 'feature2', 'feature3']
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

# Pipeline
pipeline = Pipeline(stages=[assembler, model])

# Training with MLflow
with mlflow.start_run():
    model = pipeline.fit(train_data)
    mlflow.log_param("model_type", "logistic_regression")
    # ... more logging
```

**Best practices:**
- Log all experiments to MLflow
- Use consistent feature engineering
- Validate on hold-out sets
- Track model performance metrics

### ETL Pipeline Notebooks

**Purpose**: Extract, transform, and load data

**Use cases:**
- Data ingestion from sources
- Data cleansing and validation
- Schema transformations
- Data quality checks

**What you get:**
```python
# Imports
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

# Schema definition
schema = StructType([
    StructField("id", StringType(), False),
    StructField("name", StringType(), True),
    # ... more fields
])

# Extract
raw_data = spark.read.format("delta").load("path/to/source")

# Transform
transformed = raw_data \
    .filter(F.col("status") == "active") \
    .withColumn("processed_at", F.current_timestamp())

# Load
transformed.write.format("delta").mode("overwrite").save("path/to/target")
```

**Best practices:**
- Define schemas explicitly
- Add data quality checks
- Use incremental processing
- Log pipeline metrics

### General Purpose Notebooks

**Purpose**: Flexible notebooks for any use case

**Use cases:**
- Exploratory data analysis
- Ad-hoc queries
- Prototyping
- Custom workflows

**What you get:**
```python
# Common imports
from pyspark.sql import functions as F
import pandas as pd
import matplotlib.pyplot as plt

# Flexible placeholder cells for your code
```

**Best practices:**
- Start with exploration
- Document findings
- Refactor to specific types later
- Keep organized

## Workflow Examples

### Workflow 1: Agent Development

1. **Generate notebook:**
   ```
   User: "Create an agent notebook called sales_assistant using profile dev"
   ```

2. **Develop locally:**
   - Open `sales_assistant.py` in VS Code
   - Run environment setup cell
   - See: "✅ Connected to Databricks using profile: dev"
   - Develop agent logic with live LLM access

3. **Test locally:**
   - Run agent with test inputs
   - Check MLflow for logged runs
   - Iterate on prompts and logic

4. **Deploy to workspace:**
   - Upload to Databricks workspace
   - Schedule as job or serve as app
   - No code changes needed

### Workflow 2: ML Model Development

1. **Generate notebook:**
   ```
   User: "Create ML notebook for fraud detection using profile ml_prod"
   ```

2. **Develop locally:**
   - Open `fraud_detection.py` in IDE
   - Connect to Databricks
   - Access training data from Unity Catalog
   - Develop feature engineering pipeline

3. **Train and track:**
   - Train model locally using Databricks compute
   - MLflow automatically logs to workspace
   - Compare experiments in MLflow UI

4. **Deploy model:**
   - Register best model in MLflow
   - Deploy to model serving endpoint
   - Use in production

### Workflow 3: ETL Pipeline

1. **Generate notebook:**
   ```
   User: "Create ETL notebook for daily sales aggregation"
   ```

2. **Develop locally:**
   - Open `daily_sales_aggregation.py`
   - Connect to Databricks
   - Test transforms on sample data
   - Validate output schema

3. **Schedule:**
   - Upload to workspace
   - Create job with schedule
   - Monitor pipeline runs
   - Set up alerts

## Customization After Generation

### Adding Custom Libraries

Edit the generated notebook to add imports:

```python
# COMMAND ----------

# Add your custom imports
from my_custom_library import CustomTransformer
import special_package

# COMMAND ----------
```

### Changing Cluster Configuration

When deploying to workspace, you can specify compute:

```yaml
# In Databricks Asset Bundle
resources:
  jobs:
    my_job:
      tasks:
        - task_key: my_task
          notebook_task:
            notebook_path: ./notebooks/my_notebook.py
          new_cluster:
            spark_version: "14.3.x-scala2.12"
            node_type_id: "i3.xlarge"
            num_workers: 4
```

### Adding Widgets for Parameters

Add parameter widgets to notebooks:

```python
# COMMAND ----------

# Create widgets for runtime parameters
dbutils.widgets.text("input_path", "/default/path")
dbutils.widgets.dropdown("environment", "dev", ["dev", "staging", "prod"])

# Get widget values
input_path = dbutils.widgets.get("input_path")
environment = dbutils.widgets.get("environment")

# COMMAND ----------
```

### Adding Schedules and Notifications

In workspace or DAB configuration:

```yaml
resources:
  jobs:
    my_job:
      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Daily at midnight
        timezone_id: "America/Los_Angeles"
      email_notifications:
        on_failure:
          - team@example.com
```

## Integration Examples

### Integration with Databricks Asset Bundles

**Scenario**: Deploy multiple notebooks as a workflow

1. **Generate notebooks:**
   ```
   User: "Create three notebooks:
   - ETL notebook called ingest_data
   - ML notebook called train_model
   - General notebook called create_report
   All using profile prod"
   ```

2. **Create DAB configuration** (`databricks.yml`):
   ```yaml
   resources:
     jobs:
       ml_pipeline:
         name: "ML Training Pipeline"
         tasks:
           - task_key: ingest
             notebook_task:
               notebook_path: ./notebooks/ingest_data.py
           - task_key: train
             depends_on:
               - task_key: ingest
             notebook_task:
               notebook_path: ./notebooks/train_model.py
           - task_key: report
             depends_on:
               - task_key: train
             notebook_task:
               notebook_path: ./notebooks/create_report.py
   ```

3. **Deploy:**
   ```bash
   databricks bundle deploy -t prod
   databricks bundle run ml_pipeline -t prod
   ```

### Integration with Unity Catalog

Access catalog resources in generated notebooks:

```python
# COMMAND ----------

# Read from Unity Catalog table
df = spark.table("main.my_schema.my_table")

# Write to Unity Catalog
df.write.saveAsTable("main.my_schema.output_table")

# Use UC volumes
file_path = "/Volumes/main/my_schema/my_volume/data.csv"
data = spark.read.csv(file_path, header=True)

# COMMAND ----------
```

### Integration with MLflow

Use MLflow in generated notebooks:

```python
# COMMAND ----------

import mlflow

# Set experiment
mlflow.set_experiment("/Users/me@example.com/my_experiment")

# Log run
with mlflow.start_run(run_name="experiment_1"):
    # Train model
    model = train_model(data)

    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1_score", 0.93)

    # Log model
    mlflow.spark.log_model(model, "model")

# COMMAND ----------
```

## Troubleshooting Guide

### Issue: Profile not found

**Error:**
```
Error: Profile 'my_profile' not found in ~/.databrickscfg
```

**Solution:**
1. Check profile name spelling
2. Verify `~/.databrickscfg` exists
3. Confirm profile is configured:
   ```bash
   cat ~/.databrickscfg | grep "\[my_profile\]"
   ```

### Issue: Connection timeout

**Error:**
```
Connection timeout when connecting to Databricks
```

**Solution:**
1. Verify workspace URL in profile
2. Check network connectivity
3. Verify token is valid
4. Check VPN requirements

### Issue: Import errors locally

**Error:**
```
ModuleNotFoundError: No module named 'src.utils.dev_utils'
```

**Solution:**
1. Create `src/utils/dev_utils.py`:
   ```python
   def is_running_in_databricks():
       import os
       return 'DATABRICKS_RUNTIME_VERSION' in os.environ
   ```
2. Ensure project root is in Python path
3. Run from correct directory

### Issue: Databricks Connect version mismatch

**Error:**
```
DatabricksError: Version mismatch
```

**Solution:**
1. Check cluster runtime version
2. Install matching Databricks Connect:
   ```bash
   pip install databricks-connect==14.3.*
   ```

## Best Practices Summary

### Development
✅ Test locally before deploying
✅ Use version control for notebooks
✅ Keep notebooks focused on single tasks
✅ Add comments and documentation
✅ Use descriptive variable names

### Security
✅ Use profiles for authentication
✅ Never hardcode tokens
✅ Rotate tokens regularly
✅ Use service principals for production
✅ Set appropriate access controls

### Performance
✅ Start with small data samples locally
✅ Use appropriate cluster sizes
✅ Cache intermediate results
✅ Monitor Spark UI for optimizations
✅ Use Delta Lake for better performance

### Collaboration
✅ Use .py format for easy diffs
✅ Review changes before merging
✅ Document notebook purpose
✅ Share profiles securely
✅ Use consistent naming conventions

## Tips for First-Time Users

1. **Start simple**: Begin with a general notebook to understand the structure
2. **Test connection**: Verify Databricks Connect works before complex development
3. **Use examples**: Generated example code shows best practices
4. **Read references**: Check `notebook_structure.md` for detailed format info
5. **Iterate**: Develop locally, test frequently, deploy when ready

## Common Patterns

### Pattern 1: Incremental ETL

```python
# Read last processed timestamp
checkpoint = spark.table("main.schema.checkpoint").collect()[0][0]

# Process new data
new_data = spark.read.format("delta") \
    .load("path/to/source") \
    .filter(F.col("timestamp") > checkpoint)

# Transform and load
process_and_load(new_data)

# Update checkpoint
spark.sql(f"UPDATE main.schema.checkpoint SET last_run = current_timestamp()")
```

### Pattern 2: A/B Testing with Agents

```python
# Define agent variants
agent_a = create_agent(temperature=0.1)
agent_b = create_agent(temperature=0.7)

# Test with sample
for test_case in test_cases:
    result_a = agent_a.run(test_case)
    result_b = agent_b.run(test_case)

    # Log to MLflow
    mlflow.log_metrics({
        "agent_a_score": score(result_a),
        "agent_b_score": score(result_b)
    })
```

### Pattern 3: Pipeline with Data Quality

```python
# Extract
df = spark.table("source_table")

# Validate
quality_checks = [
    ("row_count", df.count() > 0),
    ("no_nulls_in_id", df.filter(F.col("id").isNull()).count() == 0),
    ("valid_dates", df.filter(F.col("date") < "2020-01-01").count() == 0)
]

for check_name, passed in quality_checks:
    if not passed:
        raise ValueError(f"Quality check failed: {check_name}")

# Transform and load
df.write.saveAsTable("target_table")
```

## Next Steps

After mastering basic usage:

1. **Explore advanced features**: Check `references/` documentation
2. **Integrate with DAB**: Combine multiple notebooks into workflows
3. **Set up CI/CD**: Automate testing and deployment
4. **Optimize performance**: Learn Spark optimization techniques
5. **Share knowledge**: Help team members use the skill

## Getting Help

### From Claude
- "Show me the notebook structure reference"
- "How do I add custom imports to this notebook?"
- "What's the best way to handle large datasets locally?"
- "Help me debug this connection issue"

### From Documentation
- `QUICK_REFERENCE.md` - Quick syntax reference
- `README.md` - Package overview
- `references/notebook_structure.md` - Detailed structure guide
- `references/api_reference.md` - API conventions

## Additional Resources

- **Databricks Connect Docs**: Official documentation
- **LangGraph Docs**: For agent development
- **MLflow Docs**: For experiment tracking
- **Delta Lake Docs**: For data storage
- **Unity Catalog Docs**: For governance

---

**Ready to build?** Start with a simple notebook and work your way up to complex workflows!
