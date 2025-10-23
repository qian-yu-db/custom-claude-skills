# Databricks Asset Bundle Skill - Complete Package

## What's Included

This package contains a complete Claude skill for generating Databricks Asset Bundles (DAB) from notebooks or Python files with task dependencies.

### Package Contents

1. **databricks-asset-bundle.zip** - The skill package (ready to upload to Claude)
2. **USAGE_GUIDE.md** - Comprehensive usage examples and scenarios
3. **QUICK_REFERENCE.md** - Quick reference card for common operations

## Skill Components

### Core Script: `generate_dab.py`
Python script that generates databricks.yml configuration files from task descriptions.

**Features:**
- Parses task descriptions with dependencies
- Auto-detects file types (.ipynb vs .py)
- Configurable cluster settings
- Generates both dev and prod targets
- Validates task dependencies

### Reference Documentation: `examples.md`
Detailed examples and patterns including:
- Common DAB patterns (linear, parallel, fan-out, diamond)
- Task configuration options
- Cluster configurations
- Environment-specific settings
- Best practices

### Main Documentation: `SKILL.md`
Complete skill documentation with:
- When to use the skill
- Task description format
- Script parameters and usage
- Post-generation workflow
- Troubleshooting guide

## How It Works

1. **User describes their pipeline** - Tasks and dependencies in natural language
2. **Claude uses the skill** - Reads SKILL.md and references as needed
3. **Script generates config** - Creates databricks.yml with proper structure
4. **User deploys** - Uses Databricks CLI to deploy and run

## Example Workflow

### User Input
```
Create a Databricks Asset Bundle for my ETL pipeline:
- extract_data.ipynb extracts from source
- transform_data.py transforms (depends on extract)
- load_data.py loads to destination (depends on transform)

Call it "etl_pipeline" and use a 4-worker cluster.
```

### Claude Actions
1. Reads the skill documentation
2. Formats the task description properly
3. Runs generate_dab.py with appropriate parameters
4. Generates databricks.yml
5. Provides the file to user

### Output
A complete databricks.yml file with:
- All tasks properly configured
- Dependencies correctly set
- Cluster configuration applied
- Dev and prod targets ready

## Key Features

### Dependency Management
- Simple syntax: `[depends_on: task1, task2]`
- Supports any dependency graph (no circular dependencies)
- Parallel execution for independent tasks
- Sequential execution for dependent tasks

### Flexibility
- Works with notebooks (.ipynb) and Python files (.py)
- Customizable cluster configurations
- Multiple environment targets (dev, prod)
- Extensible for additional customizations

### Best Practices Built-In
- Descriptive task naming guidelines
- Cluster sizing recommendations
- Development-first workflow
- Clear validation and deployment steps

## Use Cases

### 1. Data Engineering
- ETL pipelines
- Data quality checks
- Data warehouse loading
- Stream processing workflows

### 2. Machine Learning
- Feature engineering pipelines
- Model training workflows
- Batch inference jobs
- Model evaluation and validation

### 3. Analytics
- Reporting pipelines
- Dashboard data preparation
- Scheduled analytics jobs
- Data aggregation workflows

### 4. Data Integration
- Multi-source data ingestion
- Data synchronization
- Cross-system data movement
- Data migration jobs

## Installation Instructions

1. Download `databricks-asset-bundle.zip`
2. Upload to Claude in your conversation
3. Claude will automatically use it when relevant

## Requirements

- Databricks workspace (any cloud provider)
- Databricks CLI installed (for deployment)
- Notebooks or Python files to orchestrate
- Understanding of task dependencies

## Getting Started

### Quick Start
Simply tell Claude: "Create a Databricks Asset Bundle for [describe your pipeline]"

### Detailed Request
Provide:
- Bundle name
- List of notebooks/files
- Dependencies between tasks
- Cluster requirements (optional)

### Example Prompts

**Simple:**
```
Create a DAB for my three-notebook ETL pipeline
```

**Detailed:**
```
I need a Databricks Asset Bundle called "customer_analytics" with:
- extract_customers.ipynb (runs first)
- enrich_data.py (depends on extract)
- calculate_metrics.py (depends on enrich)
- create_dashboard.ipynb (depends on calculate)
```

**Complex:**
```
Create a DAB with parallel data ingestion from three sources,
then validate each source independently, merge the results,
and generate a final report. Use a 4-worker cluster.
```

## Advanced Usage

### Custom Cluster Configuration
Specify Spark version, node type, and worker count in your request.

### Multiple Environments
The generated bundle includes dev and prod targets ready to customize.

### Post-Generation Customization
Edit the databricks.yml to add:
- Schedules and triggers
- Email notifications
- Retry policies
- Timeout settings
- Access controls

## Support and Documentation

### In-Skill Documentation
- `SKILL.md` - Complete skill documentation
- `references/examples.md` - Detailed patterns and examples

### External Resources
- Databricks Asset Bundles documentation
- Databricks CLI documentation
- Databricks workspace guides

### Getting Help
Ask Claude to:
- Reference the examples file for patterns
- Explain specific configurations
- Help customize the generated config
- Troubleshoot issues

## Testing

The skill has been tested with:
- Simple linear pipelines (3 tasks)
- Complex multi-dependency pipelines (8+ tasks)
- Mixed file types (notebooks and Python files)
- Multiple dependency patterns
- Various cluster configurations

## Version Information

**Skill Version:** 1.0
**Created:** 2025
**License:** Apache-2.0
**Compatible with:** Databricks Runtime 13.3+ (customizable)

## Notes

- The script generates clean, production-ready YAML
- All dependencies are validated before generation
- Task names must be unique within a bundle
- File paths are relative to specified directories
- Cluster configurations follow Databricks best practices

## Future Enhancements

Potential additions (not currently included):
- Support for SQL tasks
- Integration with Unity Catalog
- Automatic parameter passing
- Built-in retry strategies
- Email notification templates

## Feedback

This skill is designed to be practical and easy to use. The generated configurations follow Databricks best practices and are ready for production deployment with minimal customization.
