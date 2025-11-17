# Databricks Notebook Formatting Guide

Complete guide to formatting Databricks Python notebooks with blackbricks.

## Databricks Notebook Structure

Databricks `.py` notebooks have special structure that must be preserved:

```python
# Databricks notebook source          # Header (required)

# MAGIC %md                            # Markdown cell
# MAGIC # Title                        # Markdown content

# COMMAND ----------                   # Cell separator

# Python code cell
import pandas as pd

# COMMAND ----------                   # Next cell

def process_data(df):
    return df.filter(df.value > 0)

# COMMAND ----------
```

## Why blackbricks?

### Problem with Regular Formatters

**Using black directly BREAKS Databricks notebooks:**

```bash
❌ black notebook.py  # Removes cell markers!
```

**Result:**
- Cell markers disappear
- Notebook becomes unreadable in Databricks
- Structure destroyed

### Solution: blackbricks

```bash
✅ blackbricks notebook.py  # Preserves structure
```

**Result:**
- Code formatted
- Cell markers preserved
- Magic commands intact
- Works in Databricks

## Installation

```bash
uv add --dev blackbricks
```

## Basic Usage

### Format Single Notebook

```bash
uv run blackbricks notebooks/etl_pipeline.py
```

### Format Multiple Notebooks

```bash
uv run blackbricks notebooks/
```

### Check Without Modifying

```bash
uv run blackbricks --check notebooks/
```

## What Gets Formatted

### Code Cells

**Before:**
```python
# COMMAND ----------
def calculate(x,y,z):return x+y+z
result=calculate(1,2,3)
```

**After:**
```python
# COMMAND ----------


def calculate(x, y, z):
    return x + y + z


result = calculate(1, 2, 3)
```

### Imports

**Before:**
```python
# COMMAND ----------
from pyspark.sql import functions as F
import pandas as pd
from typing import List
import os
```

**After:**
```python
# COMMAND ----------
import os
from typing import List

import pandas as pd
from pyspark.sql import functions as F
```

### Type Hints

**Before:**
```python
def process(df:DataFrame,cols:List[str])->DataFrame:
    return df.select(*cols)
```

**After:**
```python
def process(df: DataFrame, cols: List[str]) -> DataFrame:
    return df.select(*cols)
```

## What Gets Preserved

### Cell Markers

```python
# COMMAND ----------  # ← Always preserved
```

### Magic Commands

```python
# MAGIC %md
# MAGIC # Title
# MAGIC Description here

# MAGIC %sql
# MAGIC SELECT * FROM table

# MAGIC %sh
# MAGIC ls -la
```

All preserved exactly as-is.

### Notebook Header

```python
# Databricks notebook source  # ← Required, always preserved
```

## Configuration

### pyproject.toml

```toml
[tool.blackbricks]
line_length = 100
target_version = ['py311']

# Optional: exclude patterns
exclude = '''
/(
    \.git
  | \.venv
  | build
)/
'''
```

### Command Line Options

```bash
# Custom line length
blackbricks --line-length 120 notebook.py

# Check only
blackbricks --check notebook.py

# Specify target version
blackbricks --target-version py311 notebook.py
```

## Complete Example

### Before Formatting

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Customer Analytics ETL

# COMMAND ----------
from pyspark.sql import functions as F,DataFrame
import pandas as pd
from typing import List,Dict

# COMMAND ----------
def process_customers(df:DataFrame,min_value:int=100)->DataFrame:
    """Process customer data."""
    return df.filter(F.col('purchase_amount')>min_value).select('customer_id','name','purchase_amount')

# COMMAND ----------
# Load data
customers_df=spark.table('catalog.schema.customers')
result=process_customers(customers_df,150)
display(result)

# COMMAND ----------
```

### After Formatting

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Customer Analytics ETL

# COMMAND ----------
from typing import Dict, List

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


# COMMAND ----------
def process_customers(df: DataFrame, min_value: int = 100) -> DataFrame:
    """Process customer data."""
    return (
        df.filter(F.col("purchase_amount") > min_value)
        .select("customer_id", "name", "purchase_amount")
    )


# COMMAND ----------
# Load data
customers_df = spark.table("catalog.schema.customers")
result = process_customers(customers_df, 150)
display(result)


# COMMAND ----------
```

## Integration with Workflow

### Development Workflow

```bash
# 1. Edit notebook in IDE
vim notebooks/etl_pipeline.py

# 2. Format before testing
blackbricks notebooks/etl_pipeline.py

# 3. Test locally with Databricks Connect
python -m databricks.connect.client test

# 4. Upload to Databricks (optional)
databricks workspace import notebooks/etl_pipeline.py /Workspace/notebooks/etl_pipeline
```

### Git Workflow

```bash
# Before committing
blackbricks notebooks/

git add notebooks/
git commit -m "Format notebooks"
```

### CI/CD

```yaml
# .github/workflows/format.yml
- name: Check Databricks notebook formatting
  run: |
    uv add --dev blackbricks
    uv run blackbricks --check notebooks/
```

## Combining with Other Tools

### With ruff

```bash
# Format first
blackbricks notebook.py

# Then lint
ruff check --fix notebook.py
```

### With pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: blackbricks
        name: blackbricks
        entry: blackbricks
        language: system
        types: [python]
        files: '^notebooks/.*\.py$'
```

## Common Patterns

### Agent Development Notebooks

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # LangGraph Agent

# COMMAND ----------
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from databricks_langchain import ChatDatabricks


# COMMAND ----------
class AgentState(TypedDict):
    """Agent state schema."""

    messages: Annotated[list[BaseMessage], "The messages"]


def agent_node(state: AgentState) -> AgentState:
    """Process agent logic."""
    llm = ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


# COMMAND ----------
# Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
compiled_graph = graph.compile()


# COMMAND ----------
```

## Troubleshooting

### Cell Markers Removed

**Problem:** Cell markers disappear after formatting

**Cause:** Used `black` instead of `blackbricks`

**Solution:**
```bash
# Don't use
black notebook.py  # ❌

# Use instead
blackbricks notebook.py  # ✅
```

### Import Errors After Formatting

**Problem:** Imports broken in Databricks

**Cause:** Import order changed, dependencies not available in cell

**Solution:** blackbricks sorts imports correctly for Databricks

### Formatting Takes Long Time

**Problem:** Slow formatting on many notebooks

**Solution:**
```bash
# Format in parallel (requires GNU parallel)
find notebooks/ -name "*.py" | parallel blackbricks {}
```

### Check Failed in CI

**Problem:** CI fails on unformatted notebooks

**Solution:**
```bash
# Format locally before pushing
blackbricks notebooks/
git add notebooks/
git commit -m "Format notebooks"
git push
```

## Best Practices

1. **Always use blackbricks** for Databricks notebooks
2. **Never use black** on Databricks notebooks
3. **Format before committing** to Git
4. **Add to pre-commit hooks** for automation
5. **Keep line length consistent** with project (default: 100)
6. **Run ruff after blackbricks** for additional cleanup

## Comparison with Other Options

### blackbricks vs black

| Feature | blackbricks | black |
|---------|-------------|-------|
| Format code | ✅ | ✅ |
| Preserve cells | ✅ | ❌ |
| Preserve magic | ✅ | ❌ |
| Databricks notebooks | ✅ | ❌ |
| Regular Python | ❌ | ✅ |

### blackbricks vs Manual Formatting

| Aspect | blackbricks | Manual |
|--------|-------------|--------|
| Speed | Fast (< 1s) | Slow (minutes) |
| Consistency | Perfect | Variable |
| Effort | Zero | High |
| Errors | None | Common |

## Summary

- **Use blackbricks** for all Databricks notebooks
- **Preserves** cell structure and magic commands
- **Formats** code with black-style
- **Integrates** with ruff for linting
- **Essential** for Databricks + Git workflows
