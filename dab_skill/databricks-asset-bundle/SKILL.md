---
name: databricks-asset-bundle
description: Create Databricks Asset Bundles (DAB) from notebooks or Python files with task dependencies. Use when setting up Databricks workflows, jobs, or pipelines that need to orchestrate multiple notebooks/scripts with specified execution order and dependencies.
license: Apache-2.0
---

# Databricks Asset Bundle Creator

Generate Databricks Asset Bundles (DAB) from a set of notebooks or Python files with task dependencies and execution order.

## When to Use This Skill

Use this skill when:
- Setting up a Databricks workflow from multiple notebooks or Python files
- Creating a Databricks job with task dependencies
- Converting an existing pipeline into a Databricks Asset Bundle
- Orchestrating data pipelines with clear execution order
- Deploying reusable Databricks projects across environments

## Quick Start Workflow

1. **Gather task information** - Identify notebooks/Python files and their dependencies
2. **Create task description** - Format tasks with dependencies (see format below)
3. **Generate DAB configuration** - Run the generate_dab.py script
4. **Review and customize** - Edit databricks.yml as needed
5. **Deploy** - Use Databricks CLI to validate and deploy

## Task Description Format

Use this format to specify tasks and dependencies:

```
- task_name: path/to/file.py
- another_task: path/to/notebook.ipynb [depends_on: task_name]
- final_task: path/to/final.py [depends_on: task1, task2]
```

**Format rules:**
- One task per line
- Format: `task_name: file_path [depends_on: dep1, dep2]`
- Optional leading dash (`-`) for readability
- Dependencies are comma-separated in `[depends_on: ...]`
- Tasks without dependencies have no `[depends_on: ...]` clause
- Comments start with `#`

## Generating the Bundle

### Basic Usage

```bash
scripts/generate_dab.py my_pipeline \
  -d "extract: extract.ipynb
      transform: transform.py [depends_on: extract]
      load: load.py [depends_on: transform]"
```

### With Custom Configuration

```bash
scripts/generate_dab.py my_pipeline \
  -d "task1: notebook1.ipynb
      task2: script.py [depends_on: task1]" \
  --spark-version "14.3.x-scala2.12" \
  --node-type "i3.2xlarge" \
  --num-workers 4 \
  --notebook-dir "./notebooks" \
  -o databricks.yml
```

### Script Parameters

- `bundle_name` (required): Name of the bundle and job
- `-d, --description` (required): Task description with dependencies
- `-o, --output`: Output file path (default: databricks.yml)
- `--notebook-dir`: Notebook directory (default: ./notebooks)
- `--spark-version`: Spark version (default: 13.3.x-scala2.12)
- `--node-type`: Node type ID (default: i3.xlarge)
- `--num-workers`: Number of workers (default: 2)

## Understanding Task Dependencies

Tasks execute based on their dependencies:

**No dependencies** → Runs immediately when job starts
**Has dependencies** → Runs only after all dependencies complete successfully

Example execution flow:
```
- extract_a: extract_a.ipynb          # Runs first (parallel)
- extract_b: extract_b.ipynb          # Runs first (parallel)
- merge: merge.py [depends_on: extract_a, extract_b]  # Runs after both complete
- analyze: analyze.py [depends_on: merge]             # Runs last
```

## Common Patterns

For detailed examples and patterns, see [references/examples.md](references/examples.md):

**Linear pipeline**: Sequential tasks (ETL)
**Parallel processing**: Independent tasks that converge
**Fan-out pattern**: One source feeding multiple downstream tasks
**Diamond pattern**: Multiple dependency paths converging

Load the reference file for specific implementation examples.

## Post-Generation Steps

After generating databricks.yml:

1. **Review configuration** - Check cluster settings, task paths, dependencies
2. **Customize if needed** - Add parameters, adjust cluster config, add schedules
3. **Validate bundle** - Run `databricks bundle validate`
4. **Deploy to environment** - Run `databricks bundle deploy -t dev`
5. **Test execution** - Run `databricks bundle run my_pipeline_job -t dev`

## Generated Bundle Structure

The script generates:

```yaml
bundle:
  name: <bundle_name>

resources:
  jobs:
    <bundle_name>_job:
      name: <bundle_name>_job
      tasks:
        - task_key: <task1>
          notebook_task: ...
          new_cluster: ...
        - task_key: <task2>
          depends_on:
            - task_key: <task1>
          python_wheel_task: ...
          new_cluster: ...

targets:
  dev:
    mode: "development"
    default: true
  prod:
    mode: "production"
```

## Task Type Detection

The script automatically determines task type from file extension:

- `.ipynb` files → `notebook_task`
- `.py` files → `python_wheel_task`

## Cluster Configuration

Default cluster config (customizable via parameters):
```yaml
new_cluster:
  spark_version: "13.3.x-scala2.12"
  node_type_id: "i3.xlarge"
  num_workers: 2
```

For advanced cluster configurations, edit databricks.yml after generation. See references/examples.md for common cluster patterns.

## Environment Targets

Generated bundle includes two targets:

**dev (default)**: Development mode with workspace host variable
**prod**: Production mode with workspace host variable

Configure target-specific settings in databricks.yml after generation.

## Troubleshooting

**No valid tasks found**: Check task description format, ensure proper syntax

**Invalid dependencies**: Verify dependency task names match exactly (case-sensitive)

**Bundle validation fails**: Run `databricks bundle validate` for specific errors

**Path issues**: Ensure notebook/file paths are correct relative to notebook_dir

## Best Practices

- Use descriptive task names (e.g., `ingest_customer_data` not `task1`)
- Keep dependency chains simple and explicit
- Start with small clusters and scale based on actual data volume
- Use development target for testing before deploying to production
- Version control your databricks.yml configuration
- Test individual notebooks before orchestrating them in a bundle

## Advanced Customization

After generation, customize databricks.yml for:

- Schedule/triggers (cron expressions)
- Email notifications on success/failure
- Timeout settings per task
- Retry policies
- Parameter passing between tasks
- Different clusters per task
- Access control and permissions
- Tags and metadata

See references/examples.md for advanced configuration patterns.
