# Python Code Formatter Skill

## Purpose

This skill helps Claude automatically format Python code using modern tools with `uv` package management. It intelligently handles different file types:
- **Databricks notebooks (.py)**: Uses `blackbricks` package
- **Regular Python files**: Uses `black` and `isort` packages
- **All files**: Uses `ruff` for linting and auto-fixing

## When to Activate

This skill should activate when the user requests:
- "Format my Python code"
- "Run black on this file"
- "Format my Databricks notebook"
- "Fix code style issues"
- "Run ruff on my project"
- "Sort imports in my Python files"
- "Auto-format this codebase"

## Core Capabilities

### 1. Automatic File Type Detection
- Detect Databricks notebooks by special markers
- Identify regular Python files
- Handle directories with mixed file types
- Skip non-Python files automatically

### 2. Databricks Notebook Formatting
- Use `blackbricks` for Databricks `.py` notebooks
- Preserve cell markers (`# COMMAND ----------`)
- Preserve magic commands (`# MAGIC %md`)
- Format code cells while keeping structure intact

### 3. Regular Python File Formatting
- Use `black` for code formatting (PEP 8 compliant)
- Use `isort` for import sorting
- Configurable line length and style options

### 4. Linting and Auto-fixing
- Use `ruff` for fast linting
- Auto-fix common issues
- Enforce code quality standards
- Check formatting without modifying files

## Workflow

### Step 1: Detect File Type

```python
def is_databricks_notebook(file_path: Path) -> bool:
    """Detect if file is a Databricks notebook."""
    with open(file_path, 'r') as f:
        first_line = f.readline()
        return '# Databricks notebook source' in first_line
```

### Step 2: Format Based on Type

**For Databricks Notebooks:**
```bash
uv run blackbricks <notebook.py>
```

**For Regular Python Files:**
```bash
uv run isort <file.py>
uv run black <file.py>
```

**For All Files (Linting):**
```bash
uv run ruff check --fix <file_or_directory>
```

### Step 3: Verify Formatting

```bash
# Check without modifying
uv run black --check <file.py>
uv run isort --check <file.py>
uv run ruff check <file.py>
```

## Tool Selection Logic

### blackbricks (Databricks Notebooks Only)

**When to use:**
- File starts with `# Databricks notebook source`
- File contains `# COMMAND ----------` markers
- File has `# MAGIC` commands

**What it does:**
- Formats code cells using black
- Preserves Databricks-specific structure
- Maintains cell separators
- Keeps magic commands intact

**Configuration:**
```toml
[tool.blackbricks]
line_length = 100
target_version = ['py311']
```

### black (Regular Python Files)

**When to use:**
- Standard Python files (.py)
- Non-Databricks notebooks
- Python scripts and modules

**What it does:**
- Enforces consistent code style
- Handles string quotes, line length, whitespace
- PEP 8 compliant formatting

**Configuration:**
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

### isort (Import Sorting)

**When to use:**
- Regular Python files (not Databricks notebooks)
- After adding/removing imports
- Before committing code

**What it does:**
- Sorts imports alphabetically
- Groups imports (stdlib, third-party, local)
- Removes duplicate imports
- Formats multi-line imports

**Configuration:**
```toml
[tool.isort]
profile = "black"  # Compatible with black
line_length = 100
multi_line_output = 3
include_trailing_comma = true
```

### ruff (Linting & Auto-fix)

**When to use:**
- All Python files (including Databricks notebooks)
- Pre-commit checks
- CI/CD pipelines
- Quick code quality checks

**What it does:**
- Fast linting (100x faster than pylint)
- Auto-fixes many issues
- Checks for common errors
- Enforces code style

**Configuration:**
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
```

## Formatting Strategies

### Strategy 1: Format Single File

```python
def format_file(file_path: Path) -> dict:
    """Format a single Python file."""
    if is_databricks_notebook(file_path):
        # Use blackbricks
        result = run_command(["uv", "run", "blackbricks", str(file_path)])
    else:
        # Use isort + black
        run_command(["uv", "run", "isort", str(file_path)])
        result = run_command(["uv", "run", "black", str(file_path)])

    # Run ruff for additional fixes
    run_command(["uv", "run", "ruff", "check", "--fix", str(file_path)])

    return result
```

### Strategy 2: Format Directory

```python
def format_directory(directory: Path, skip_databricks: bool = False):
    """Format all Python files in directory."""
    databricks_files = []
    regular_files = []

    for py_file in directory.rglob("*.py"):
        if is_databricks_notebook(py_file):
            databricks_files.append(py_file)
        else:
            regular_files.append(py_file)

    # Format Databricks notebooks
    if not skip_databricks:
        for nb in databricks_files:
            run_command(["uv", "run", "blackbricks", str(nb)])

    # Format regular Python files
    if regular_files:
        run_command(["uv", "run", "isort"] + [str(f) for f in regular_files])
        run_command(["uv", "run", "black"] + [str(f) for f in regular_files])

    # Run ruff on everything
    run_command(["uv", "run", "ruff", "check", "--fix", str(directory)])
```

### Strategy 3: Check Only (CI/CD)

```python
def check_formatting(path: Path) -> bool:
    """Check if files are properly formatted without modifying."""
    checks_passed = True

    if is_databricks_notebook(path):
        result = run_command(["uv", "run", "blackbricks", "--check", str(path)])
        checks_passed = result.returncode == 0
    else:
        # Check isort
        result = run_command(["uv", "run", "isort", "--check", str(path)])
        checks_passed &= (result.returncode == 0)

        # Check black
        result = run_command(["uv", "run", "black", "--check", str(path)])
        checks_passed &= (result.returncode == 0)

    # Check ruff
    result = run_command(["uv", "run", "ruff", "check", str(path)])
    checks_passed &= (result.returncode == 0)

    return checks_passed
```

## Installation and Setup

### Step 1: Install Dependencies

```bash
# For Databricks projects
uv add --dev blackbricks ruff

# For regular Python projects
uv add --dev black isort ruff

# For mixed projects (Databricks + regular Python)
uv add --dev black isort blackbricks ruff
```

### Step 2: Configure pyproject.toml

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
target_version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]
```

### Step 3: Create Format Script

The skill provides `scripts/format_code.py` that handles all formatting automatically.

## Usage Patterns

### Format Single File

```bash
# Databricks notebook
python scripts/format_code.py notebooks/etl_pipeline.py

# Regular Python file
python scripts/format_code.py src/utils.py

# Auto-detect and format
python scripts/format_code.py <any_file.py>
```

### Format Entire Project

```bash
# Format all Python files
python scripts/format_code.py .

# Format specific directory
python scripts/format_code.py src/

# Format only regular Python files (skip Databricks)
python scripts/format_code.py src/ --skip-databricks
```

### Check Formatting (CI/CD)

```bash
# Check without modifying
python scripts/check_format.py .

# Exit with error if not formatted
python scripts/check_format.py src/ --strict
```

### Run Individual Tools

```bash
# Just ruff
uv run ruff check --fix .

# Just black
uv run black src/

# Just isort
uv run isort src/

# Just blackbricks
uv run blackbricks notebooks/
```

## Databricks Notebook Example

### Before Formatting

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # ETL Pipeline

# COMMAND ----------

from pyspark.sql import functions as F
import pandas as pd
from typing import List

# COMMAND ----------

def process_data(df,columns:List[str])->DataFrame:
    result=df.select(*columns).filter(F.col('value')>0)
    return result

# COMMAND ----------
```

### After Formatting (with blackbricks)

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


def process_data(df: DataFrame, columns: List[str]) -> DataFrame:
    result = df.select(*columns).filter(F.col("value") > 0)
    return result


# COMMAND ----------
```

**Note:**
- Cell markers preserved
- Magic commands intact
- Imports sorted (isort style)
- Code formatted (black style)
- Type hints properly spaced

## Regular Python File Example

### Before Formatting

```python
from typing import List
import os
from pathlib import Path
import pandas as pd

def calculate_metrics(data:List[int],threshold:int=10)->dict:
    filtered=[x for x in data if x>threshold]
    return {'count':len(filtered),'sum':sum(filtered),'avg':sum(filtered)/len(filtered) if filtered else 0}
```

### After Formatting (black + isort)

```python
import os
from pathlib import Path
from typing import List

import pandas as pd


def calculate_metrics(data: List[int], threshold: int = 10) -> dict:
    filtered = [x for x in data if x > threshold]
    return {
        "count": len(filtered),
        "sum": sum(filtered),
        "avg": sum(filtered) / len(filtered) if filtered else 0,
    }
```

## Integration with Git Hooks

### pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        exclude: '.*\.databricks\.py$'

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        exclude: '.*\.databricks\.py$'

  - repo: local
    hooks:
      - id: blackbricks
        name: blackbricks
        entry: blackbricks
        language: system
        types: [python]
        files: '.*\.databricks\.py$'
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Format Check

on: [push, pull_request]

jobs:
  format-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv add --dev black isort blackbricks ruff

      - name: Check formatting
        run: |
          uv run python scripts/check_format.py .
          if [ $? -ne 0 ]; then
            echo "Code is not properly formatted"
            exit 1
          fi

      - name: Run ruff
        run: uv run ruff check .
```

## Best Practices

### 1. Format Before Committing

Always format code before committing:
```bash
python scripts/format_code.py .
git add .
git commit -m "Your message"
```

### 2. Use Pre-commit Hooks

Install pre-commit to format automatically:
```bash
uv add --dev pre-commit
uv run pre-commit install
```

### 3. Configure Line Length Consistently

Use the same line length across all tools:
```toml
[tool.black]
line-length = 100

[tool.isort]
line_length = 100

[tool.blackbricks]
line_length = 100

[tool.ruff]
line-length = 100
```

### 4. Check in CI/CD

Add formatting checks to your CI pipeline to prevent unformatted code from merging.

### 5. Format by File Type

- Databricks notebooks: `blackbricks` only
- Regular Python: `isort` → `black` → `ruff --fix`
- Mixed projects: Use detection script

## Reference Files

The skill includes these reference documents (Claude will read these when needed):

- `references/tool-comparison.md` - Comparison of formatting tools
- `references/databricks-formatting.md` - Databricks notebook formatting guide
- `references/configuration-guide.md` - Complete configuration reference
- `references/troubleshooting.md` - Common issues and solutions

## Scripts

### scripts/format_code.py
Automatically formats Python files with appropriate tools.

**Features:**
- Auto-detects Databricks notebooks
- Uses correct formatter for each file type
- Handles directories recursively
- Provides detailed output

### scripts/check_format.py
Checks formatting without modifying files (for CI/CD).

**Features:**
- Validates all files are formatted
- Returns exit code for CI/CD
- Shows which files need formatting
- Fast check mode

## User Interaction Flow

1. **User Request**: "Format my Python code"

2. **Claude Actions**:
   - Scan directory for Python files
   - Detect Databricks notebooks vs regular files
   - Install formatters if needed (`uv add --dev black isort blackbricks ruff`)
   - Run appropriate formatter for each file type
   - Show summary of formatted files

3. **Claude Response**:
   - "I've formatted 12 Python files:"
   - "  - 3 Databricks notebooks (blackbricks)"
   - "  - 9 regular Python files (black + isort)"
   - "  - Fixed 15 linting issues with ruff"
   - Provides commands to run formatting again

## Error Handling

### Missing Dependencies

```bash
# Auto-install missing tools
uv add --dev black isort blackbricks ruff
```

### Syntax Errors

If file has syntax errors, formatters will fail:
- Show error message
- Identify problematic file and line
- Suggest fixing syntax first

### File Permissions

Handle read-only files gracefully:
- Skip read-only files
- Show warning
- Continue with other files

## Quality Checklist

Before completing, ensure:
- [ ] All Python files are formatted
- [ ] Imports are sorted
- [ ] No ruff violations
- [ ] Databricks notebook structure preserved
- [ ] Configuration files updated
- [ ] Pre-commit hooks work
- [ ] CI/CD checks pass

## Tips for Claude

- Always detect file type before formatting
- Use blackbricks for Databricks notebooks to preserve structure
- Run isort before black for regular files
- Run ruff last for final cleanup
- Check formatting in CI/CD without modifying files
- Suggest pre-commit hooks for automation
- Configure consistent line length across all tools
- Skip formatting for generated or vendored code
