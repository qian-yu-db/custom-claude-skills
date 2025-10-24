# Python Code Formatter Skill

🎯 **Purpose**: Automatically format Python code using the right tools - `blackbricks` for Databricks notebooks, `black` + `isort` for regular Python files, and `ruff` for linting/auto-fixes. All managed with `uv`.

## 📦 Package Contents

| File | Description |
|------|-------------|
| `python-code-formatter/` | **Main skill package** - Add to .claude/skills/ |
| `README.md` | This file - your starting point |
| `QUICK_REFERENCE.md` | Quick reference card for formatting commands |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `python-code-formatter.zip` to Claude
- The skill activates when you request code formatting

### 2. Use the Skill
Simply tell Claude what you need:

```
"Format my Python code"
"Format this Databricks notebook"
"Fix code style issues in src/"
"Run ruff on my project"
"Sort imports and format code"
```

### 3. Get Formatted Code
Claude will:
- Auto-detect Databricks notebooks vs regular Python files
- Apply the correct formatter for each type
- Fix linting issues with ruff
- Show summary of changes

## 🎯 What This Skill Does

### Input
You provide:
- Path to file or directory
- Formatting preferences (optional)
- Whether to check only or modify files

### Output
You get:
- Properly formatted Python code
- Sorted imports (regular Python files)
- Preserved Databricks notebook structure
- Fixed linting issues
- Summary of changes made

### Tool Selection

**Databricks Notebooks (.py with special markers):**
- ✅ `blackbricks` - Preserves cell markers and magic commands
- ✅ `ruff` - Linting and auto-fixes

**Regular Python Files:**
- ✅ `isort` - Sorts imports
- ✅ `black` - Code formatting
- ✅ `ruff` - Linting and auto-fixes

## 🔥 Key Features

### Intelligent File Detection
- Automatically detects Databricks notebooks
- Identifies regular Python files
- Handles mixed projects seamlessly
- Skips virtual environments and build directories

### Databricks Notebook Support
- Preserves `# COMMAND ----------` markers
- Keeps `# MAGIC %md` markdown cells intact
- Formats code cells while maintaining structure
- Databricks-compatible formatting

### Modern Formatting
- Black-style formatting (PEP 8 compliant)
- Automatic import sorting
- Fast linting with ruff (100x faster than pylint)
- Auto-fixes common code issues

### UV Package Management
- Fast dependency installation
- Manages formatting tools separately
- Virtual environment handling
- Lock file support

## 💡 Common Use Cases

### Format Entire Project
```
"Format all Python files in my project"
```

### Format Databricks Notebooks
```
"Format my Databricks ETL notebooks in the notebooks/ directory"
```

### Check Formatting (CI/CD)
```
"Check if my code is properly formatted without changing it"
```

### Fix Specific Issues
```
"Fix import order and code style in src/utils.py"
```

### Pre-commit Formatting
```
"Set up automatic formatting before commits"
```

## 📝 Before and After Examples

### Databricks Notebook

**Before:**
```python
# Databricks notebook source
# MAGIC %md
# MAGIC # ETL Pipeline

# COMMAND ----------

from pyspark.sql import functions as F
import pandas as pd
from typing import List

# COMMAND ----------

def process(df,cols:List[str])->DataFrame:
    return df.select(*cols).filter(F.col('value')>0)
```

**After:**
```python
# Databricks notebook source
# MAGIC %md
# MAGIC # ETL Pipeline

# COMMAND ----------

from typing import List

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# COMMAND ----------


def process(df: DataFrame, cols: List[str]) -> DataFrame:
    return df.select(*cols).filter(F.col("value") > 0)
```

### Regular Python File

**Before:**
```python
from typing import List
import os
from pathlib import Path

def calc(data:List[int])->dict:
    return {'sum':sum(data),'count':len(data)}
```

**After:**
```python
import os
from pathlib import Path
from typing import List


def calc(data: List[int]) -> dict:
    return {"sum": sum(data), "count": len(data)}
```

## 🔧 How It Works

### Step 1: Scan Files
Claude scans your codebase and categorizes files:
- Databricks notebooks (detected by special markers)
- Regular Python files
- Skips virtual environments and build directories

### Step 2: Apply Formatters

**For Databricks notebooks:**
```bash
uv run blackbricks notebook.py
uv run ruff check --fix notebook.py
```

**For regular Python files:**
```bash
uv run isort file.py
uv run black file.py
uv run ruff check --fix file.py
```

### Step 3: Report Results
Shows summary of:
- Files formatted
- Issues fixed
- Any errors encountered

## 🎓 Learning Path

### Beginner
1. Format a single file
2. Understand the formatting changes
3. Review tool outputs

### Intermediate
1. Format entire directories
2. Configure formatting preferences
3. Use check mode for CI/CD

### Advanced
1. Set up pre-commit hooks
2. Customize formatting rules
3. Integrate with CI/CD pipelines

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| Quick commands | `QUICK_REFERENCE.md` |
| Tool comparison | `references/tool-comparison.md` (in package) |
| Databricks formatting | `references/databricks-formatting.md` (in package) |
| Configuration guide | `references/configuration-guide.md` (in package) |
| Troubleshooting | `references/troubleshooting.md` (in package) |

## ⚙️ Prerequisites

### Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Python Version
- Python 3.10 or higher

### Project Structure (Recommended)
```
your-project/
├── src/               # Regular Python code
├── notebooks/         # Databricks notebooks
├── tests/            # Test files
├── pyproject.toml    # Configuration
└── .pre-commit-config.yaml  # Pre-commit hooks (optional)
```

## 🛠️ What Gets Created

### Scripts

**format_code.py**:
- Auto-detects file types
- Formats with appropriate tools
- Handles directories recursively
- Shows detailed progress

**check_format.py**:
- Checks formatting without modifying
- Perfect for CI/CD
- Returns exit codes for automation

### Configuration (pyproject.toml)

```toml
[project.optional-dependencies]
format = [
    "black>=24.0.0",
    "isort>=5.13.0",
    "blackbricks>=2.0.0",
    "ruff>=0.3.0",
]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.blackbricks]
line_length = 100

[tool.ruff]
line-length = 100
target-version = "py311"
```

## 💎 Best Practices Built In

### Consistent Configuration
✅ Same line length across all tools (default: 100)
✅ Black-compatible isort configuration
✅ Coordinated tool settings

### Smart Detection
✅ Automatically identifies file types
✅ Uses correct formatter for each
✅ Preserves Databricks structure

### Fast and Efficient
✅ UV for fast package management
✅ Ruff for rapid linting
✅ Batch processing for multiple files

### CI/CD Ready
✅ Check mode for validation
✅ Exit codes for automation
✅ Pre-commit hook templates

## 🎯 Example Prompts

### Simple
```
"Format my Python code"
```

### Specific
```
"Format the Databricks notebooks in notebooks/ and regular Python files in src/"
```

### CI/CD
```
"Check if all Python files are properly formatted for my CI pipeline"
```

### Configuration
```
"Set up code formatting with black, isort, and ruff using uv"
```

## 🤝 Getting Help

### From Claude
- "Show me the formatting tool comparison"
- "How do I configure line length to 120?"
- "Set up pre-commit hooks for auto-formatting"
- "Why is my Databricks notebook structure broken?"

### From Documentation
- Check `QUICK_REFERENCE.md` for commands
- See package references for detailed guides
- Review tool documentation for advanced options

## 📦 What's In The Skill Package

```
python-code-formatter/
├── SKILL.md                          # Main skill instructions
├── scripts/
│   ├── format_code.py                # Main formatting script
│   └── check_format.py               # Check-only mode for CI/CD
└── references/
    ├── tool-comparison.md            # Comparison of tools
    ├── databricks-formatting.md      # Databricks-specific guide
    ├── configuration-guide.md        # Full config reference
    └── troubleshooting.md            # Common issues
```

## 🚀 Next Steps

1. **Upload** `python-code-formatter.zip` to Claude
2. **Try** formatting a single file
3. **Review** the changes
4. **Configure** preferences in pyproject.toml
5. **Automate** with pre-commit hooks

## 📋 System Requirements

- Python 3.10 or higher
- UV package manager
- Git (recommended for pre-commit hooks)

## 🔗 Integration

### Pre-commit Hooks
Automatically format before commits:
```bash
uv add --dev pre-commit
uv run pre-commit install
```

### CI/CD (GitHub Actions)
```yaml
- name: Check formatting
  run: |
    uv add --dev black isort blackbricks ruff
    python scripts/check_format.py .
```

### VS Code
Add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

## 🎉 Benefits

- ⚡ **Fast**: UV-powered installation and execution
- 🎯 **Smart**: Detects and formats correctly based on file type
- 🔧 **Flexible**: Works with Databricks and regular Python
- 📊 **Comprehensive**: Formatting + import sorting + linting
- 🚀 **Modern**: Uses latest tools (ruff, uv, black)
- ✅ **Reliable**: Preserves Databricks notebook structure

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check `QUICK_REFERENCE.md` for common commands
- Review the references in the skill package
- Consult tool documentation (black, ruff, isort, blackbricks)

---

**Ready to get started?** Upload `python-code-formatter.zip` to Claude and start formatting!
