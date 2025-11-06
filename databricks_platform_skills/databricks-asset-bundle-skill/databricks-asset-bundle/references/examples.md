# Databricks Asset Bundle Examples and Patterns

## Common DAB Patterns

### Simple Linear Pipeline

For sequential data processing with clear dependencies:

```
- extract: extract_data.ipynb
- transform: transform_data.ipynb [depends_on: extract]
- load: load_data.ipynb [depends_on: transform]
```

### Parallel Processing with Merge

For independent tasks that converge:

```
- fetch_source_a: fetch_a.py
- fetch_source_b: fetch_b.py
- process_a: process_a.py [depends_on: fetch_source_a]
- process_b: process_b.py [depends_on: fetch_source_b]
- merge: merge_data.py [depends_on: process_a, process_b]
```

### Fan-out Pattern

For one task feeding multiple independent downstream tasks:

```
- ingest: ingest_raw.ipynb
- transform_sales: transform_sales.ipynb [depends_on: ingest]
- transform_inventory: transform_inventory.ipynb [depends_on: ingest]
- transform_customers: transform_customers.ipynb [depends_on: ingest]
```

### Complex Diamond Pattern

For tasks with multiple dependency paths:

```
- extract: extract.py
- validate: validate.py [depends_on: extract]
- enrich_demographics: enrich_demo.py [depends_on: validate]
- enrich_behavior: enrich_behavior.py [depends_on: validate]
- aggregate: aggregate.py [depends_on: enrich_demographics, enrich_behavior]
```

## Task Configuration Options

### Notebook Tasks

For Jupyter notebooks stored in workspace:

```yaml
notebook_task:
  notebook_path: "./notebooks/analysis.ipynb"
  source: "WORKSPACE"
  base_parameters:
    env: "production"
    date: "2024-01-01"
```

### Python Wheel Tasks

For Python packages:

```yaml
python_wheel_task:
  package_name: "my_pipeline"
  entry_point: "main"
  parameters: ["--env", "prod"]
```

### Spark Python Tasks

For standalone Python files:

```yaml
spark_python_task:
  python_file: "./src/process.py"
  parameters: ["--input", "/data/input"]
```

## Cluster Configuration Options

### Job Clusters (Recommended)

New cluster for each task:

```yaml
new_cluster:
  spark_version: "13.3.x-scala2.12"
  node_type_id: "i3.xlarge"
  num_workers: 2
  spark_conf:
    "spark.speculation": "true"
  aws_attributes:
    availability: "SPOT"
```

### Existing Clusters

Use pre-existing cluster:

```yaml
existing_cluster_id: "1234-567890-abcd1234"
```

### Job Compute (Serverless)

For serverless compute:

```yaml
job_cluster_key: "main_cluster"
# Define in job_clusters section
```

## Environment-Specific Configuration

### Development Target

```yaml
targets:
  dev:
    mode: "development"
    default: true
    workspace:
      host: "https://dev-workspace.cloud.databricks.com"
    variables:
      catalog: "dev_catalog"
      schema: "dev_schema"
```

### Production Target

```yaml
targets:
  prod:
    mode: "production"
    workspace:
      host: "https://prod-workspace.cloud.databricks.com"
    variables:
      catalog: "prod_catalog"
      schema: "prod_schema"
    permissions:
      - level: "CAN_VIEW"
        user_name: "data-team@company.com"
```

## Common Cluster Configurations

### Small Development Cluster

```yaml
spark_version: "13.3.x-scala2.12"
node_type_id: "i3.xlarge"
num_workers: 1
spark_conf:
  "spark.databricks.delta.preview.enabled": "true"
```

### Production ETL Cluster

```yaml
spark_version: "13.3.x-scala2.12"
node_type_id: "i3.2xlarge"
num_workers: 8
autoscale:
  min_workers: 4
  max_workers: 16
spark_conf:
  "spark.sql.adaptive.enabled": "true"
  "spark.databricks.delta.optimizeWrite.enabled": "true"
```

### ML Training Cluster

```yaml
spark_version: "13.3.x-gpu-ml-scala2.12"
node_type_id: "g4dn.xlarge"
num_workers: 2
custom_tags:
  project: "ml-training"
```

## Best Practices

### Task Naming

- Use descriptive, action-oriented names: `ingest_customer_data`, `transform_sales`, `generate_report`
- Avoid generic names like `task1`, `step2`, `process`
- Use consistent naming convention across bundle

### Dependency Management

- Keep dependencies simple and explicit
- Avoid circular dependencies
- Use parallelization where possible for independent tasks
- Consider retry policies for flaky tasks

### Cluster Sizing

- Start small and scale based on data volume
- Use autoscaling for variable workloads
- Consider spot instances for cost savings in non-critical pipelines
- Use job clusters (new_cluster) for isolated environments

### File Organization

```
my-bundle/
├── databricks.yml          # Main configuration
├── notebooks/              # Jupyter notebooks
│   ├── extract.ipynb
│   └── transform.ipynb
├── src/                    # Python source code
│   ├── __init__.py
│   ├── common/
│   └── tasks/
└── tests/                  # Unit tests
    └── test_tasks.py
```
