# Databricks Asset Bundle Skill - Quick Reference

## What It Does
Creates Databricks Asset Bundle (DAB) configuration files from notebooks or Python files with task dependencies.

## When to Use
- Setting up Databricks workflows
- Orchestrating data pipelines
- Creating jobs with task dependencies
- Deploying multi-step processes

## Task Description Format
```
- task_name: path/to/file.py
- task_with_deps: path/to/notebook.ipynb [depends_on: task_name]
- multiple_deps: final.py [depends_on: task1, task2]
```

## Basic Command
```bash
scripts/generate_dab.py BUNDLE_NAME \
  -d "TASK_DESCRIPTION"
```

## Example
```bash
scripts/generate_dab.py my_pipeline \
  -d "extract: extract.ipynb
      transform: transform.py [depends_on: extract]
      load: load.py [depends_on: transform]"
```

## Common Options
| Option | Description | Default |
|--------|-------------|---------|
| `-d, --description` | Task description (required) | - |
| `-o, --output` | Output file path | databricks.yml |
| `--notebook-dir` | Notebook directory | ./notebooks |
| `--spark-version` | Spark version | 13.3.x-scala2.12 |
| `--node-type` | Node type ID | i3.xlarge |
| `--num-workers` | Number of workers | 2 |

## Dependency Patterns

### Linear (Sequential)
```
A → B → C → D
```

### Parallel with Merge
```
A ─┐
   ├─→ C → D
B ─┘
```

### Fan-out
```
     ┌→ B
A ──┼→ C
     └→ D
```

### Diamond
```
     ┌→ B ─┐
A ──┤      ├─→ D
     └→ C ─┘
```

## File Types
- `.ipynb` → notebook_task
- `.py` → python_wheel_task

## Post-Generation Steps
1. Review databricks.yml
2. Validate: `databricks bundle validate`
3. Deploy: `databricks bundle deploy -t dev`
4. Run: `databricks bundle run <job_name> -t dev`

## Generated Targets
- **dev** (default): Development mode
- **prod**: Production mode

## Best Practices
✓ Use descriptive task names
✓ Keep dependencies simple
✓ Start with small clusters
✓ Test individual notebooks first
✓ Version control databricks.yml

✗ Avoid generic names (task1, task2)
✗ Avoid circular dependencies
✗ Don't over-provision clusters initially

## Common Customizations
After generation, edit databricks.yml to add:
- Schedules (cron expressions)
- Email notifications
- Timeout settings
- Retry policies
- Parameter passing
- Per-task cluster configs
- Access control
- Tags and metadata

## Quick Examples

### Simple ETL
```
User: "Create a DAB for extract.ipynb, transform.py, load.py in sequence"
```

### Parallel Processing
```
User: "Create a DAB with parallel ingestion from 3 sources, 
      then merge them, then generate report"
```

### ML Pipeline
```
User: "Create ML pipeline: ingest → clean → feature_engineering 
      → train → evaluate"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No valid tasks found | Check task format syntax |
| Invalid dependencies | Verify task name matches exactly |
| Path issues | Confirm paths relative to notebook_dir |
| Bundle validation fails | Run `databricks bundle validate` for details |

## Advanced Features
See `references/examples.md` for:
- Common cluster configurations
- Advanced patterns
- Environment-specific settings
- Best practices by use case
