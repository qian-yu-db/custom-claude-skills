# Formatting Tool Comparison

Comprehensive comparison of Python formatting tools used in this skill.

## Overview

| Tool | Purpose | Speed | File Types | Auto-fix |
|------|---------|-------|------------|----------|
| **blackbricks** | Format Databricks notebooks | Fast | Databricks `.py` | Yes |
| **black** | Format regular Python code | Fast | Regular `.py` | Yes |
| **isort** | Sort and organize imports | Very Fast | Regular `.py` | Yes |
| **ruff** | Lint and auto-fix issues | Ultra Fast | All `.py` | Partial |

## blackbricks

### Purpose
Format Databricks Python notebooks while preserving special structure.

### When to Use
- Files starting with `# Databricks notebook source`
- Contains `# COMMAND ----------` cell markers
- Has `# MAGIC` commands for markdown/SQL

### What It Does
✅ Formats code cells with black-style formatting
✅ Preserves cell separators (`# COMMAND ----------`)
✅ Keeps magic commands intact (`# MAGIC %md`)
✅ Sorts imports within cells
✅ Maintains notebook structure

### What It Doesn't Do
❌ Format regular Python files
❌ Lint code
❌ Fix logic errors

### Example

**Before:**
```python
# Databricks notebook source
# COMMAND ----------
from pyspark.sql import functions as F
import pandas
# COMMAND ----------
def process(df,value:int):return df.filter(F.col('x')>value)
```

**After:**
```python
# Databricks notebook source
# COMMAND ----------
import pandas
from pyspark.sql import functions as F


# COMMAND ----------
def process(df, value: int):
    return df.filter(F.col("x") > value)
```

### Speed
⚡ Fast - Formats typical notebook in <1 second

### Configuration
```toml
[tool.blackbricks]
line_length = 100
target_version = ['py311']
```

### Pros
- ✅ Databricks-specific
- ✅ Preserves structure
- ✅ Black-compatible output

### Cons
- ❌ Only for Databricks notebooks
- ❌ Less mature than black

## black

### Purpose
The uncompromising Python code formatter.

### When to Use
- Regular Python files (`.py`, `.pyi`)
- Not Databricks notebooks
- Want consistent, PEP 8 compliant code

### What It Does
✅ Formats code to consistent style
✅ Handles string quotes
✅ Manages line length
✅ Fixes whitespace
✅ Formats collections

### What It Doesn't Do
❌ Sort imports (use isort)
❌ Lint code (use ruff)
❌ Preserve Databricks structure

### Example

**Before:**
```python
def calculate(x,y,z):
    result={'sum':x+y+z,'product':x*y*z}
    return result
```

**After:**
```python
def calculate(x, y, z):
    result = {"sum": x + y + z, "product": x * y * z}
    return result
```

### Speed
⚡⚡ Fast - Formats 1000 files in ~10 seconds

### Configuration
```toml
[tool.black]
line-length = 100
target-version = ['py311']
skip-string-normalization = false
```

### Pros
- ✅ Industry standard
- ✅ Consistent output
- ✅ Well-tested
- ✅ Widely adopted

### Cons
- ❌ Opinionated (limited config)
- ❌ Breaks Databricks notebooks

## isort

### Purpose
Sort and organize Python imports.

### When to Use
- Regular Python files
- After adding/removing imports
- Before running black

### What It Does
✅ Sorts imports alphabetically
✅ Groups imports (stdlib, third-party, local)
✅ Removes duplicate imports
✅ Formats multi-line imports
✅ Adds missing trailing commas

### What It Doesn't Do
❌ Format code (use black)
❌ Handle Databricks notebooks well

### Example

**Before:**
```python
from mypackage import utils
import os
from typing import List
import pandas as pd
from pathlib import Path
import sys
```

**After:**
```python
import os
import sys
from pathlib import Path
from typing import List

import pandas as pd

from mypackage import utils
```

### Speed
⚡⚡⚡ Very Fast - Sorts imports nearly instantly

### Configuration
```toml
[tool.isort]
profile = "black"  # Compatible with black
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
```

### Pros
- ✅ Fast
- ✅ Highly configurable
- ✅ Black-compatible mode
- ✅ Handles complex imports

### Cons
- ❌ Only does imports
- ❌ Needs coordination with black

## ruff

### Purpose
Ultra-fast Python linter and formatter (replacement for flake8, pylint, isort, black).

### When to Use
- All Python files (including Databricks)
- Want fast linting
- Need auto-fixes for common issues
- CI/CD pipelines

### What It Does
✅ Lints code (like flake8, pylint)
✅ Auto-fixes many issues
✅ Checks imports (like isort)
✅ Can format code (like black)
✅ Enforces code style
✅ Finds bugs and anti-patterns

### What It Doesn't Do
❌ Handle Databricks structure (use blackbricks)

### Example - Linting

**Input:**
```python
import os, sys  # Bad: multiple imports on one line
from typing import *  # Bad: star import

def process(data):
    x = 1  # Unused variable
    return data
```

**After `ruff check --fix`:**
```python
import os
import sys
from typing import Dict, List

def process(data):
    return data
```

### Speed
⚡⚡⚡⚡ Ultra Fast - 10-100x faster than pylint/flake8

### Configuration
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
ignore = ["E501"]  # Line too long

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports
```

### Pros
- ✅ Extremely fast
- ✅ Replaces multiple tools
- ✅ Active development
- ✅ Great auto-fixes
- ✅ Works with Databricks (for linting)

### Cons
- ❌ Newer (less mature)
- ❌ Formatting not as perfect as black yet

## Tool Selection Matrix

### For Databricks Notebooks

| Task | Tool | Command |
|------|------|---------|
| Format code | blackbricks | `blackbricks notebook.py` |
| Lint code | ruff | `ruff check --fix notebook.py` |
| Sort imports | (included in blackbricks) | N/A |

### For Regular Python Files

| Task | Tool | Command |
|------|------|---------|
| Sort imports | isort | `isort file.py` |
| Format code | black | `black file.py` |
| Lint + auto-fix | ruff | `ruff check --fix file.py` |

### Recommended Order

**Databricks:**
```bash
blackbricks notebook.py  # Format + sort imports
ruff check --fix notebook.py  # Lint and fix
```

**Regular Python:**
```bash
isort file.py  # Sort imports first
black file.py  # Then format
ruff check --fix file.py  # Finally lint
```

## Speed Comparison

Formatting 1000 files:

| Tool | Time | Relative Speed |
|------|------|----------------|
| **ruff** | 0.5s | 100x (fastest) |
| **isort** | 2s | 25x |
| **black** | 10s | 5x |
| **blackbricks** | 12s | 4x |
| **pylint** | 50s | 1x (baseline) |

## Feature Comparison

| Feature | blackbricks | black | isort | ruff |
|---------|-------------|-------|-------|------|
| Format code | ✅ | ✅ | ❌ | ✅ |
| Sort imports | ✅ | ❌ | ✅ | ✅ |
| Lint code | ❌ | ❌ | ❌ | ✅ |
| Auto-fix | ✅ | ✅ | ✅ | ✅ (partial) |
| Databricks support | ✅ | ❌ | ❌ | ⚠️ (lint only) |
| Speed | Fast | Fast | Very Fast | Ultra Fast |
| Configurability | Low | Low | High | High |

## Configuration Compatibility

### Line Length

Must be consistent across all tools:

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

### isort + black Compatibility

```toml
[tool.isort]
profile = "black"  # Makes isort compatible with black
```

This ensures isort doesn't format imports in a way that black will change.

## When to Use Each Tool

### Use blackbricks When:
- ✅ File is a Databricks notebook
- ✅ File has `# Databricks notebook source` marker
- ✅ Need to preserve cell structure

### Use black When:
- ✅ Regular Python file
- ✅ Want consistent formatting
- ✅ Following industry standard

### Use isort When:
- ✅ Regular Python file
- ✅ Imports need organizing
- ✅ Before running black

### Use ruff When:
- ✅ Any Python file
- ✅ Want fast linting
- ✅ Need auto-fixes
- ✅ CI/CD pipelines

## Combined Workflow

### For Mixed Projects (Databricks + Regular Python)

```python
# Automatic detection and formatting
def format_project():
    for file in python_files:
        if is_databricks_notebook(file):
            run("blackbricks", file)
        else:
            run("isort", file)
            run("black", file)
        run("ruff check --fix", file)
```

## Alternatives Considered

### Why not autopep8?
- ❌ Slower than black
- ❌ Less consistent output
- ❌ More configuration needed

### Why not yapf?
- ❌ More configuration complexity
- ❌ Less widely adopted
- ❌ Slower than black

### Why not pylint?
- ❌ 100x slower than ruff
- ❌ No auto-formatting
- ❌ Ruff covers most checks

### Why not flake8?
- ❌ 50x slower than ruff
- ❌ Less auto-fixing
- ❌ Ruff is compatible replacement

## Summary

**Best Practice:**
- **Databricks notebooks**: blackbricks + ruff
- **Regular Python**: isort + black + ruff
- **All projects**: Use UV for package management
- **CI/CD**: Use check modes for validation

**Key Principle:**
Use the right tool for the right job - blackbricks for Databricks, black for regular Python, ruff for linting everywhere.
