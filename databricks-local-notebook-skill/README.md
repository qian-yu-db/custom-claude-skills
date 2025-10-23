# Databricks Local Notebook Skill - Complete Package

🎯 **Purpose**: Generate Databricks notebooks (.py) with seamless local IDE development support using Databricks Connect.

## 📦 Package Contents

| File | Description |
|------|-------------|
| `databricks-local-notebook/` | **Main skill package** - Add to .claude/skills/ |
| `USAGE_GUIDE.md` | Comprehensive usage examples and scenarios |
| `QUICK_REFERENCE.md` | Quick reference card for common operations |
| `README.md` | This file - your starting point |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `databricks-local-notebook.zip` to Claude
- The skill activates when you need to create Databricks notebooks

### 2. Use the Skill
Simply tell Claude what type of notebook you need:

```
Create a Databricks notebook for agent development called customer_support_agent
using profile e2_demo_fieldeng
```

### 3. Get Your Notebook
Claude will generate a ready-to-use notebook that works both locally and in Databricks workspace!

## 📖 Documentation Guide

### For First-Time Users
1. **Start here**: Read this README
2. **Learn by example**: See `USAGE_GUIDE.md`
3. **Quick reference**: Keep `QUICK_REFERENCE.md` handy

### For Quick Reference
- **During use**: Check `QUICK_REFERENCE.md`
- **Common patterns**: See examples in `USAGE_GUIDE.md`

## 🎯 What This Skill Does

### Input
You provide:
- Notebook name (will be converted to snake_case)
- Notebook type (agent, ml, etl, or general)
- Databricks profile name (optional)
- Output directory (optional)

### Output
You get:
- Complete Databricks notebook (.py format)
- Automatic environment detection code
- Type-specific starter code and imports
- Ready to run locally or in workspace

### Example Transformation

**You say:**
```
Create an ML notebook called churn_prediction using profile my_profile
```

**You get:**
- File: `churn_prediction.py`
- Databricks notebook with:
  - Environment detection (local vs workspace)
  - Automatic Databricks Connect setup
  - ML-specific imports (Spark ML, MLflow)
  - Starter code for model training
  - Ready to run in VS Code or Databricks

## 🔥 Key Features

### Dual Environment Support
- Works in local IDE (VS Code, PyCharm, etc.)
- Works in Databricks workspace
- Automatic environment detection
- No code changes needed between environments

### Four Notebook Types
1. **Agent** - LangGraph AI agents with ChatDatabricks
2. **ML** - Machine learning with Spark ML and MLflow
3. **ETL** - Data pipelines with PySpark
4. **General** - Flexible notebooks for any use case

### Databricks Connect Integration
- Automatic connection to Databricks from local IDE
- Profile-based authentication
- Access to workspace resources (tables, MLflow, Unity Catalog)

### Type-Specific Starter Code
- Relevant imports for each notebook type
- Example code patterns
- Best practices built-in

## 💡 Common Use Cases

### AI Agent Development
```
Build LangGraph agents that use Databricks LLMs and logging
```

### Machine Learning
```
Train and evaluate models locally with Databricks resources
```

### Data Engineering
```
Develop ETL pipelines in your IDE with live Databricks data
```

### Data Analysis
```
Explore data locally with full Databricks capabilities
```

## 📝 Notebook Types

### Agent (`--type agent`)
**Best for**: LangGraph-based AI agents, agentic workflows, chatbots

**Includes**:
- LangGraph and LangChain imports
- ChatDatabricks for LLM integration
- MLflow for agent logging
- Starter code for agent state, nodes, and graph

### ML/AI (`--type ml`)
**Best for**: Machine learning model training and evaluation

**Includes**:
- Spark ML pipeline imports
- MLflow model logging
- Starter code for data prep, training, evaluation

### ETL Pipeline (`--type etl`)
**Best for**: Data ingestion, transformation, and loading

**Includes**:
- PySpark transformation functions
- Schema definition utilities
- Extract-Transform-Load workflow structure

### General Purpose (`--type general`)
**Best for**: Exploratory data analysis, custom workflows

**Includes**:
- Common PySpark and pandas imports
- Flexible placeholder cells

## 🔧 How It Works

1. **You describe your notebook** - Tell Claude the type and purpose
2. **Skill guides Claude** - Provides proper structure and format
3. **Script generates notebook** - Creates .py file with Databricks format
4. **You develop locally** - Open in IDE, code connects to Databricks automatically
5. **Deploy to workspace** - Upload if needed, works without modification

## 🎓 Learning Path

### Beginner
1. Read the "Quick Start" section above
2. Create a simple general notebook
3. Try running it locally in VS Code

### Intermediate
1. Create agent or ML notebooks
2. Use type-specific starter code
3. Customize the generated code

### Advanced
1. Integrate with Databricks Asset Bundles
2. Create custom notebook templates
3. Build complex multi-notebook workflows

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| How to use the skill | `USAGE_GUIDE.md` |
| Quick command reference | `QUICK_REFERENCE.md` |
| Notebook structure details | `references/notebook_structure.md` (in package) |
| API reference | `references/api_reference.md` (in package) |

## ⚙️ Prerequisites

Before using this skill, ensure you have:

1. **Databricks Connect installed**:
   ```bash
   pip install databricks-connect
   # or
   uv add databricks-connect
   ```

2. **Databricks profile configured** in `~/.databrickscfg`:
   ```ini
   [your_profile_name]
   host = https://your-workspace.cloud.databricks.com
   token = dapi...
   ```

3. **Utility function** at `src/utils/dev_utils.py`:
   ```python
   def is_running_in_databricks():
       """Detect if code is running in Databricks workspace"""
       import os
       return 'DATABRICKS_RUNTIME_VERSION' in os.environ
   ```

## 🛠️ Generated Notebook Structure

All notebooks include:

1. **Header cell**: Markdown title and description
2. **Environment setup cell**: Automatic detection and connection
3. **Type-specific cells**: Starter code for the chosen type
4. **Placeholder cells**: For custom development

### Environment Detection (Included in All)

```python
from src.utils.dev_utils import is_running_in_databricks
import os

if not is_running_in_databricks():
    print("🔧 Running in local IDE - setting up Databricks Connect")
    from databricks.connect import DatabricksSession

    # Clear conflicting environment variables
    for env_var in ['DATABRICKS_AUTH_TYPE', 'DATABRICKS_METADATA_SERVICE_URL',
                     'DATABRICKS_SERVERLESS_COMPUTE_ID']:
        os.environ.pop(env_var, None)

    # Connect using profile
    profile = "your_profile_name"
    spark = DatabricksSession.builder.profile(profile).getOrCreate()
    print(f"✅ Connected to Databricks using profile: {profile}")
else:
    print("🏢 Running in Databricks workspace")
```

## 💎 Best Practices

✅ **Do:**
- Use descriptive notebook names
- Specify the correct notebook type
- Test locally before deploying
- Keep notebooks focused on single tasks
- Use version control for notebooks

❌ **Don't:**
- Mix multiple concerns in one notebook
- Hardcode credentials
- Skip environment detection
- Forget to sync dependencies

## 🎯 Example Prompts

### Simple
```
"Create a Databricks notebook for data analysis"
```

### Detailed
```
"Create an agent development notebook called customer_support_agent
using profile e2_demo_fieldeng with LangGraph setup"
```

### Complex
```
"Generate an ML notebook for customer churn prediction with MLflow
tracking, using profile prod_ml, and include example training code"
```

## 🤝 Getting Help

### From Claude
- "Show me the notebook structure reference"
- "Help me customize this notebook"
- "What imports do I need for ML notebooks?"
- "How do I test this locally?"

### From Documentation
- Check `QUICK_REFERENCE.md` for syntax
- See `USAGE_GUIDE.md` for examples
- Read skill package docs for advanced patterns

## 📦 What's In The Skill Package

The `databricks-local-notebook.zip` contains:

```
databricks-local-notebook/
├── SKILL.md                    # Main documentation
├── scripts/
│   └── generate_notebook.py    # Core generation script
├── references/
│   ├── notebook_structure.md   # Detailed structure guide
│   └── api_reference.md        # API and conventions
└── assets/
    └── templates/              # Notebook templates
```

## 🚀 Next Steps

1. **Upload** `databricks-local-notebook.zip` to Claude
2. **Read** `USAGE_GUIDE.md` for examples
3. **Try** creating your first notebook
4. **Refer** to `QUICK_REFERENCE.md` as needed
5. **Develop** locally with Databricks Connect

## 📋 System Requirements

- Python 3.10+
- Databricks workspace (AWS, Azure, or GCP)
- Databricks Connect library
- IDE (VS Code, PyCharm, Cursor, etc.)
- Access to Databricks workspace resources

## 🔗 Integration with Other Tools

### Databricks Asset Bundles
Generated notebooks work seamlessly with DAB:

```yaml
resources:
  jobs:
    my_job:
      tasks:
        - task_key: my_task
          notebook_task:
            notebook_path: ./notebooks/my_notebook.py
```

### Version Control
Notebooks are .py files (not .ipynb), making them:
- Easy to diff
- Merge-friendly
- Great for code review

## 🎉 Benefits

- ⚡ **Fast**: Generate notebooks in seconds
- 🔄 **Dual-mode**: Work locally or in workspace
- 🎯 **Type-aware**: Get relevant starter code
- 📚 **Educational**: Learn best practices from templates
- 🚀 **Production-ready**: Deploy immediately after development

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check the provided markdown files
- Review Databricks Connect documentation

---

**Ready to get started?** Upload `databricks-local-notebook.zip` to Claude and start creating notebooks!
