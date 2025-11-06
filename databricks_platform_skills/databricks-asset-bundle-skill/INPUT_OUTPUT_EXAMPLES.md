# Input vs Output Examples

This document shows how user descriptions are transformed into Databricks Asset Bundle configurations.

## Example 1: Simple Linear ETL

### User Input
```
Create a Databricks Asset Bundle called "etl_pipeline" with:
- extract_data.ipynb - extracts data from source
- transform_data.py - transforms the data (depends on extract_data)
- load_data.py - loads to destination (depends on transform_data)
```

### Task Description Format
```
extract_data: extract_data.ipynb
transform_data: transform_data.py [depends_on: extract_data]
load_data: load_data.py [depends_on: transform_data]
```

### Generated databricks.yml
```yaml
bundle:
  name: etl_pipeline

resources:
  jobs:
    etl_pipeline_job:
      name: etl_pipeline_job
      tasks:
      - task_key: extract_data
        notebook_task:
          notebook_path: ./notebooks/extract_data.ipynb
          source: WORKSPACE
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 2

      - task_key: transform_data
        depends_on:
        - task_key: extract_data
        python_wheel_task:
          package_name: etl_pipeline
          entry_point: transform_data
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 2

      - task_key: load_data
        depends_on:
        - task_key: transform_data
        python_wheel_task:
          package_name: etl_pipeline
          entry_point: load_data
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 2

      max_concurrent_runs: 1

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${workspace.host}
  prod:
    mode: production
    workspace:
      host: ${workspace.host}
```

## Example 2: Parallel Processing with Merge

### User Input
```
Create a bundle "data_integration" with parallel ingestion:
- ingest_sales: src/ingest_sales.py (no dependencies)
- ingest_inventory: src/ingest_inventory.py (no dependencies)
- merge_data: src/merge.py (depends on both ingestion tasks)
- generate_report: notebooks/report.ipynb (depends on merge_data)

Use 4 workers per cluster.
```

### Task Description Format
```
ingest_sales: src/ingest_sales.py
ingest_inventory: src/ingest_inventory.py
merge_data: src/merge.py [depends_on: ingest_sales, ingest_inventory]
generate_report: notebooks/report.ipynb [depends_on: merge_data]
```

### Generated databricks.yml
```yaml
bundle:
  name: data_integration

resources:
  jobs:
    data_integration_job:
      name: data_integration_job
      tasks:
      # These two tasks run in parallel (no dependencies)
      - task_key: ingest_sales
        python_wheel_task:
          package_name: data_integration
          entry_point: src.ingest_sales
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 4

      - task_key: ingest_inventory
        python_wheel_task:
          package_name: data_integration
          entry_point: src.ingest_inventory
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 4

      # This task waits for both parallel tasks to complete
      - task_key: merge_data
        depends_on:
        - task_key: ingest_sales
        - task_key: ingest_inventory
        python_wheel_task:
          package_name: data_integration
          entry_point: src.merge
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 4

      # Final task depends on merge
      - task_key: generate_report
        depends_on:
        - task_key: merge_data
        notebook_task:
          notebook_path: ./notebooks/notebooks/report.ipynb
          source: WORKSPACE
        new_cluster:
          spark_version: 13.3.x-scala2.12
          node_type_id: i3.xlarge
          num_workers: 4

      max_concurrent_runs: 1

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${workspace.host}
  prod:
    mode: production
    workspace:
      host: ${workspace.host}
```

## Example 3: Complex Diamond Pattern

### User Input
```
Create "ml_pipeline" with:
1. ingest_raw: notebooks/ingest.ipynb (no deps)
2. clean_data: src/clean.py (depends on ingest_raw)
3. feature_eng_numeric: src/features_numeric.py (depends on clean_data)
4. feature_eng_text: src/features_text.py (depends on clean_data)
5. train_model: src/train.py (depends on both feature engineering tasks)
6. evaluate: notebooks/evaluate.ipynb (depends on train_model)

Use Spark 14.3.x with 8 workers.
```

### Task Description Format
```
ingest_raw: notebooks/ingest.ipynb
clean_data: src/clean.py [depends_on: ingest_raw]
feature_eng_numeric: src/features_numeric.py [depends_on: clean_data]
feature_eng_text: src/features_text.py [depends_on: clean_data]
train_model: src/train.py [depends_on: feature_eng_numeric, feature_eng_text]
evaluate: notebooks/evaluate.ipynb [depends_on: train_model]
```

### Visual Dependency Graph
```
ingest_raw
    ↓
clean_data
    ├─→ feature_eng_numeric ─┐
    │                        │
    └─→ feature_eng_text ────┴→ train_model
                                      ↓
                                  evaluate
```

### Key Points in Generated Config
```yaml
# Stage 1: Ingestion (no dependencies - runs first)
- task_key: ingest_raw
  notebook_task: ...

# Stage 2: Cleaning (depends on ingestion)
- task_key: clean_data
  depends_on:
  - task_key: ingest_raw
  python_wheel_task: ...

# Stage 3: Parallel feature engineering (both depend on clean_data)
- task_key: feature_eng_numeric
  depends_on:
  - task_key: clean_data
  python_wheel_task: ...

- task_key: feature_eng_text
  depends_on:
  - task_key: clean_data
  python_wheel_task: ...

# Stage 4: Model training (depends on both feature tasks)
- task_key: train_model
  depends_on:
  - task_key: feature_eng_numeric
  - task_key: feature_eng_text
  python_wheel_task: ...

# Stage 5: Evaluation (depends on training)
- task_key: evaluate
  depends_on:
  - task_key: train_model
  notebook_task: ...
```

## Execution Flow Comparison

### Example 1 (Linear)
```
Time →
  T1: extract_data ──────────┐
  T2:                        └→ transform_data ──────────┐
  T3:                                                    └→ load_data
```

### Example 2 (Parallel with Merge)
```
Time →
  T1: ingest_sales ──────┐
  T2: ingest_inventory ──┴→ merge_data ────→ generate_report
```

### Example 3 (Diamond)
```
Time →
  T1: ingest_raw ──→ clean_data
  T2:                      ├──→ feature_eng_numeric ──┐
  T3:                      └──→ feature_eng_text ─────┴→ train_model ──→ evaluate
```

## Key Transformation Rules

1. **File Type Detection**
   - `.ipynb` → `notebook_task` with `notebook_path` and `source: WORKSPACE`
   - `.py` → `python_wheel_task` with `package_name` and `entry_point`

2. **Dependency Translation**
   - `[depends_on: task1, task2]` → YAML `depends_on` list with `task_key` references

3. **Cluster Configuration**
   - User specifications → `new_cluster` configuration block
   - YAML anchors (&id001, *id001) for cluster reuse

4. **Target Environments**
   - Always generates `dev` (default) and `prod` targets
   - Both use workspace host variables for flexibility

5. **Bundle Naming**
   - Bundle name → Job name with `_job` suffix
   - Task keys remain as specified by user

## Customization Points

After generation, users commonly customize:

1. **Cluster per task** - Different clusters for different workloads
2. **Parameters** - Add base_parameters to notebook_task
3. **Schedules** - Add quartz_cron_expression to job
4. **Notifications** - Add email_notifications
5. **Retries** - Add max_retries and retry settings
6. **Timeouts** - Add timeout_seconds per task
7. **Access control** - Add permissions section
8. **Environment variables** - Add different configs per target

These customizations are done by editing the generated databricks.yml file.
