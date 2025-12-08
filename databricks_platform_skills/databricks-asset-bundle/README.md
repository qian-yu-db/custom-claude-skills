# Databricks Asset Bundle Skill - Complete Package

🎯 **Purpose**: Automatically generate production-ready Databricks Asset Bundles with serverless compute, modular structure, and multiple input formats (text, Mermaid diagrams, or workflow images).

## 📦 Package Contents

| File | Description |
|------|-------------|
| `databricks-asset-bundle/` | **Main skill package** - Add to .claude/skills/|
| `USAGE_GUIDE.md` | Comprehensive usage examples and scenarios |
| `QUICK_REFERENCE.md` | Quick reference card for common operations |
| `SKILL_SUMMARY.md` | Complete overview of skill features and capabilities |
| `INPUT_OUTPUT_EXAMPLES.md` | Before/after examples showing transformations |
| `sample_databricks.yml` | Example output showing what gets generated |
| `README.md` | This file - your starting point |

## 🌟 New Features

### ⚡ Serverless Compute (Default)
- Uses Databricks Serverless compute (client version 3)
- Fast startup, cost-effective, no cluster management
- Option to use traditional clusters with `--no-serverless`

### 📊 Multiple Input Formats
1. **Text descriptions**: Simple task:path format with dependencies
2. **Mermaid diagrams**: Parse flowcharts automatically
3. **Diagram images**: AI-powered extraction from PNG/JPG/GIF/WebP

### 🏗️ Modular Structure
- **databricks.yml**: Main bundle with variables
- **resources/*.job.yml**: Separate job definitions
- **src/**: Source code directory
- **run_workflow.sh**: Automated deployment script

### ⚙️ Variable Management
- Configurable catalog, schema, paths
- Override at runtime with `--var` flags
- Environment-specific settings (dev/prod)

## 🚀 Quick Start

### 1. Install the Skill
- Upload `databricks-asset-bundle.zip` to Claude
- The skill will automatically activate when you describe Databricks workflows

### 2. Use the Skill
Simply tell Claude about your pipeline using any input method:

**Text description:**
```
Create a Databricks Asset Bundle for my ETL pipeline:
- extract_data: src/extract.py
- transform_data: src/transform.py [depends_on: extract_data]
- load_data: src/load.py [depends_on: transform_data]
```

**Mermaid diagram:**
```
Create a DAB from this Mermaid diagram:
flowchart TB
    A[extract] --> B[transform]
    B --> C[load]
```

**Workflow image:**
```
Parse this workflow diagram image and create a DAB
[Attach workflow.png]
```

### 3. Get Your Project
Claude will generate a complete project with:
- `databricks.yml` (main configuration)
- `resources/*.job.yml` (job definitions)
- `src/` (source code templates)
- `run_workflow.sh` (deployment script)
- `README.md` (documentation)

## 📖 Documentation Guide

### For First-Time Users
1. **Start here**: Read this README
2. **Learn by example**: See `INPUT_OUTPUT_EXAMPLES.md`
3. **Try it out**: Use the examples in `USAGE_GUIDE.md`

### For Quick Reference
- **During use**: Keep `QUICK_REFERENCE.md` handy
- **Common patterns**: Check `sample_databricks.yml`

### For Deep Dive
- **All features**: Read `SKILL_SUMMARY.md`
- **Advanced patterns**: See skill's internal `references/examples.md` (Claude will read this when needed)

## 🎯 What This Skill Does

### Input
You provide:
- Names of your notebooks or Python files
- Dependencies between tasks (which tasks depend on others)
- Optional: cluster configuration preferences

### Output
You get:
- Complete `databricks.yml` configuration file
- Properly configured task dependencies
- Both dev and prod environment targets
- Ready-to-deploy bundle configuration

### Example Transformation

**You say:**
```
Create bundle "etl_pipeline" with extract.ipynb, 
transform.py (depends on extract), and 
load.py (depends on transform)
```

**You get:**
```yaml
bundle:
  name: etl_pipeline
resources:
  jobs:
    etl_pipeline_job:
      tasks:
      - task_key: extract
        notebook_task: ...
      - task_key: transform
        depends_on:
        - task_key: extract
        python_wheel_task: ...
      - task_key: load
        depends_on:
        - task_key: transform
        python_wheel_task: ...
```

## 🔥 Key Features

### Automatic Task Type Detection
- `.ipynb` files → Notebook tasks
- `.py` files → Python wheel tasks

### Flexible Dependency Graphs
- Linear pipelines (A → B → C)
- Parallel processing (A, B → C)
- Complex patterns (diamond, fan-out, etc.)

### Configurable Clusters
- Spark version
- Node types
- Worker counts
- All customizable per request

### Environment Management
- Dev and prod targets included
- Easy deployment to multiple environments

## 💡 Common Use Cases

### Data Engineering
```
ETL pipelines, data quality checks, warehouse loading
```

### Machine Learning
```
Feature engineering, model training, batch inference
```

### Analytics
```
Reporting pipelines, dashboard prep, scheduled jobs
```

### Data Integration
```
Multi-source ingestion, data synchronization, migrations
```

## 📝 Task Description Format

Simple format for specifying tasks and dependencies:

```
task_name: path/to/file.py
dependent_task: path/to/file.ipynb [depends_on: task_name]
final_task: path/to/final.py [depends_on: task1, task2]
```

**Rules:**
- One task per line
- Dependencies in `[depends_on: ...]` clause
- Comma-separated for multiple dependencies
- No dependencies = runs immediately

## 🔧 How It Works

1. **Claude reads your request** - Understands your pipeline description
2. **Skill guides Claude** - Provides format and structure guidance
3. **Script generates config** - Creates proper YAML configuration
4. **You get the file** - Ready to validate and deploy

## 🎓 Learning Path

### Beginner
1. Read the "Quick Start" section above
2. Try a simple 3-task linear pipeline
3. Check `INPUT_OUTPUT_EXAMPLES.md` Example 1

### Intermediate
1. Explore parallel processing patterns
2. Try custom cluster configurations
3. Check `INPUT_OUTPUT_EXAMPLES.md` Example 2

### Advanced
1. Create complex dependency graphs
2. Customize generated configurations
3. Read skill's internal examples (Claude will load them)
4. Check `INPUT_OUTPUT_EXAMPLES.md` Example 3

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| How to use the skill | `USAGE_GUIDE.md` |
| Quick command reference | `QUICK_REFERENCE.md` |
| All features and capabilities | `SKILL_SUMMARY.md` |
| Before/after examples | `INPUT_OUTPUT_EXAMPLES.md` |
| Sample output | `sample_databricks.yml` |

## ⚙️ After Generation

Once you have your `databricks.yml`:

1. **Review** - Check paths and dependencies
2. **Validate** - Run `databricks bundle validate`
3. **Deploy** - Run `databricks bundle deploy -t dev`
4. **Test** - Run `databricks bundle run <job_name> -t dev`
5. **Customize** - Add schedules, notifications, etc. as needed

## 🛠️ Customization Options

Post-generation, you can add:
- ⏰ Schedules (cron expressions)
- 📧 Email notifications
- 🔄 Retry policies
- ⏱️ Timeout settings
- 🔐 Access controls
- 🏷️ Tags and metadata
- 📊 Parameters per task

## 💎 Best Practices

✅ **Do:**
- Use descriptive task names
- Keep dependency graphs simple
- Start with small clusters
- Test notebooks individually first
- Version control your configs

❌ **Don't:**
- Use generic names (task1, task2)
- Create circular dependencies
- Over-provision clusters initially
- Skip validation before deployment

## 🤝 Getting Help

### From Claude
- "Show me examples from references/examples.md"
- "Help me customize this databricks.yml"
- "What cluster size should I use?"
- "Explain this dependency pattern"

### From Documentation
- Check `QUICK_REFERENCE.md` for syntax
- See `INPUT_OUTPUT_EXAMPLES.md` for patterns
- Read `USAGE_GUIDE.md` for scenarios

## 🎯 Example Prompts

### Simple
```
"Create a DAB for my 3-notebook ETL pipeline"
```

### Detailed
```
"Create a Databricks Asset Bundle called 'customer_analytics' 
with: extract_customers.ipynb, enrich_data.py (depends on extract), 
calculate_metrics.py (depends on enrich), and create_dashboard.ipynb 
(depends on calculate). Use a 4-worker cluster."
```

### Complex
```
"Set up a DAB for ML training with parallel feature engineering. 
After ingestion and cleaning, run numeric and text feature 
engineering in parallel, then train a model using both outputs, 
then evaluate. Name it 'ml_training_pipeline'."
```

## 📦 What's In The Skill Package

The `databricks-asset-bundle.zip` contains:

```
databricks-asset-bundle/
├── SKILL.md                    # Main documentation
├── scripts/
│   └── generate_dab.py         # Core generation script
└── references/
    └── examples.md             # Detailed patterns and examples
```

## 🚀 Next Steps

1. **Upload** `databricks-asset-bundle.zip` to Claude
2. **Read** `USAGE_GUIDE.md` for examples
3. **Try** creating your first bundle
4. **Refer** to `QUICK_REFERENCE.md` as needed
5. **Explore** advanced patterns in `INPUT_OUTPUT_EXAMPLES.md`

## 📋 System Requirements

- Databricks workspace (AWS, Azure, or GCP)
- Databricks CLI (for deployment)
- Your notebooks or Python files
- Understanding of your task dependencies

## 🎉 Benefits

- ⚡ **Fast**: Generate configs in seconds
- ✅ **Accurate**: Proper YAML structure guaranteed
- 🔧 **Flexible**: Supports any dependency pattern
- 📚 **Educational**: Learn DAB structure from examples
- 🚀 **Production-ready**: Deploy immediately after review

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check the provided markdown files
- Review the Databricks Asset Bundles documentation

---

**Ready to get started?** Upload `databricks-asset-bundle.zip` to Claude and describe your pipeline!
