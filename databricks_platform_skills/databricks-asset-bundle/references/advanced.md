# Advanced DAB Customization

## Scheduling

Add to job definition in `resources/*.job.yml`:

```yaml
schedule:
  quartz_cron_expression: "0 0 * * * ?"  # Daily at midnight
  timezone_id: "America/Los_Angeles"
  pause_status: "UNPAUSED"
```

## Notifications

```yaml
email_notifications:
  on_success:
    - user@company.com
  on_failure:
    - team@company.com
```

## Timeouts and Retries

```yaml
tasks:
  - task_key: long_task
    timeout_seconds: 3600  # 1 hour

  - task_key: flaky_task
    max_retries: 3
    min_retry_interval_millis: 60000  # 1 minute
```

## Mixed Compute Per Task

```yaml
tasks:
  - task_key: small_task
    environment_key: serverless_env

  - task_key: large_task
    new_cluster:
      spark_version: "14.3.x-scala2.12"
      node_type_id: "i3.4xlarge"
      num_workers: 10
```

## Access Control

```yaml
targets:
  prod:
    mode: production
    permissions:
      - group_name: data_engineers
        level: CAN_MANAGE
      - group_name: analysts
        level: CAN_VIEW
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy Databricks Bundle

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Databricks CLI
        run: pip install databricks-cli

      - name: Validate Bundle
        run: databricks bundle validate -t prod
        env:
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}

      - name: Deploy Bundle
        run: databricks bundle deploy -t prod
        env:
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

## Serverless vs Traditional Clusters

### Serverless (Default)

Advantages: instant startup, cost-effective, no cluster management, auto-scaling.

```yaml
environments:
  - environment_key: serverless_env
    spec:
      client: "3"

tasks:
  - task_key: my_task
    environment_key: serverless_env
```

### Traditional Clusters

Use `--no-serverless` flag when generating:

```yaml
tasks:
  - task_key: my_task
    new_cluster:
      spark_version: "13.3.x-scala2.12"
      node_type_id: "i3.xlarge"
      num_workers: 2
```

## Troubleshooting

### Bundle Validation Fails
1. Check task dependency names (case-sensitive)
2. No circular dependencies
3. File paths correct relative to bundle root
4. Variables properly defined

### Serverless Not Available
Use traditional clusters: `scripts/generate_dab.py my_pipeline -d "..." --no-serverless`

### Image Parsing Fails
1. Verify `ANTHROPIC_API_KEY` is set
2. Install: `pip install anthropic`
3. Ensure image is clear with visible task names and arrows

### Job Execution Fails
1. Unity Catalog and schema exist with proper permissions
2. Source data paths are accessible
3. Parameters correctly passed to tasks
