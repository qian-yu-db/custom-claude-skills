# Databricks Asset Bundle Skill - Usage Examples

## Overview

This skill helps you create Databricks Asset Bundles (DAB) from a collection of notebooks or Python files with specified task dependencies and execution order.

## Installation

1. Upload the `databricks-asset-bundle.zip` to Claude
2. The skill will be available for use in your conversations

## Basic Usage Example

### Scenario: Simple ETL Pipeline

You have three notebooks that need to run in sequence:
- `extract_data.ipynb` - extracts data from source
- `transform_data.ipynb` - transforms the extracted data
- `load_data.ipynb` - loads data to destination

**User prompt:**
```
I have three Databricks notebooks for an ETL pipeline:
1. extract_data.ipynb - extracts data
2. transform_data.ipynb - transforms data (depends on extract)
3. load_data.ipynb - loads data (depends on transform)

Create a Databricks Asset Bundle for this pipeline called "etl_pipeline"
```

**Claude will:**
1. Use the generate_dab.py script
2. Create the task description with proper dependencies
3. Generate a databricks.yml file
4. Provide the file for download

## Advanced Example

### Scenario: Parallel Processing Pipeline

You have a complex pipeline with parallel tasks:
- `ingest_sales.py` - ingests sales data (independent)
- `ingest_inventory.py` - ingests inventory data (independent)
- `validate_sales.py` - validates sales data (depends on ingest_sales)
- `validate_inventory.py` - validates inventory data (depends on ingest_inventory)
- `merge_data.py` - merges validated data (depends on both validation tasks)
- `generate_report.ipynb` - generates final report (depends on merge)

**User prompt:**
```
Create a Databricks Asset Bundle called "data_integration" with these tasks:
- ingest_sales: src/ingest_sales.py
- ingest_inventory: src/ingest_inventory.py
- validate_sales: src/validate_sales.py (depends on ingest_sales)
- validate_inventory: src/validate_inventory.py (depends on ingest_inventory)
- merge_data: src/merge_data.py (depends on validate_sales and validate_inventory)
- generate_report: notebooks/report.ipynb (depends on merge_data)

Use a larger cluster with 4 workers and Spark 14.3.x
```

## Customization Options

### Cluster Configuration

You can specify custom cluster settings:
- Spark version: `--spark-version "14.3.x-scala2.12"`
- Node type: `--node-type "i3.2xlarge"`
- Number of workers: `--num-workers 8`

### File Organization

- Notebooks are expected in `./notebooks` by default (customizable with `--notebook-dir`)
- Python files can be anywhere in your project structure

## After Generation

Once Claude generates the `databricks.yml` file:

1. **Review the configuration** - Check paths, dependencies, and cluster settings
2. **Add customizations** if needed:
   - Schedule/triggers
   - Email notifications
   - Retry policies
   - Environment-specific variables
3. **Deploy the bundle**:
   ```bash
   databricks bundle validate
   databricks bundle deploy -t dev
   databricks bundle run etl_pipeline_job -t dev
   ```

## Common Use Cases

### 1. Data Engineering Pipeline
ETL workflows with clear stages and dependencies

### 2. ML Training Pipeline
Data preparation → feature engineering → model training → evaluation

### 3. Reporting Pipeline
Data extraction → aggregation → report generation

### 4. Data Quality Pipeline
Ingestion → validation → quality checks → error handling

## Tips for Best Results

1. **Be specific about dependencies**: Clearly state which tasks depend on which
2. **Use descriptive task names**: Makes the pipeline easier to understand
3. **Mention file types**: Claude will auto-detect .ipynb vs .py files
4. **Specify cluster needs**: If you need special compute, mention it upfront
5. **Include file paths**: Full or relative paths to your notebooks/scripts

## Example Prompts

**Simple:**
```
Create a DAB for my three-stage ETL pipeline
```

**Detailed:**
```
Set up a Databricks Asset Bundle called "customer_analytics" with:
- Stage 1: extract_customers.ipynb (no dependencies)
- Stage 2: enrich_data.py (depends on extract_customers)
- Stage 3: calculate_metrics.py (depends on enrich_data)
- Stage 4: create_dashboard.ipynb (depends on calculate_metrics)

Use development cluster settings.
```

**Complex:**
```
I need a DAB for a machine learning pipeline with parallel feature engineering:
- ingest_raw_data.ipynb (no deps)
- clean_data.py (depends on ingest_raw_data)
- engineer_numeric_features.py (depends on clean_data)
- engineer_text_features.py (depends on clean_data)
- train_model.py (depends on engineer_numeric_features, engineer_text_features)
- evaluate_model.ipynb (depends on train_model)

Name it "ml_training_pipeline" and use a GPU cluster.
```

## Troubleshooting

**Issue: Dependencies not working**
- Ensure task names match exactly (case-sensitive)
- Check for typos in dependency references

**Issue: Files not found**
- Verify file paths are correct
- Check if notebook directory path is set correctly

**Issue: Cluster configuration insufficient**
- Request larger clusters in your prompt
- Or edit the generated databricks.yml manually

## Getting Help

For more details on:
- Common DAB patterns → Ask Claude to reference `references/examples.md`
- Cluster configurations → Ask for specific cluster sizing guidance
- Advanced customizations → Ask about specific features (schedules, notifications, etc.)
