---
name: python-code-formatter
description: Auto-format Python code with intelligent tool selection based on file type using uv package management. Uses blackbricks for Databricks notebooks (preserves cell structure), black+isort for regular Python, and ruff for linting. Use when formatting code, fixing style issues, or preparing code for CI/CD.
---

# Python Code Formatter Skill

Auto-format Python code using modern tools with `uv` package management. Intelligently handles different file types:
- **Databricks notebooks (.py)**: `blackbricks` (preserves cell markers and magic commands)
- **Regular Python files**: `black` + `isort`
- **All files**: `ruff` for linting and auto-fixing

## Workflow

### Step 1: Detect File Type

```python
def is_databricks_notebook(file_path: Path) -> bool:
    with open(file_path, 'r') as f:
        first_line = f.readline()
        return '# Databricks notebook source' in first_line
```

### Step 2: Format Based on Type

**Databricks Notebooks:**
```bash
uv run blackbricks <notebook.py>
```

**Regular Python Files:**
```bash
uv run isort <file.py>
uv run black <file.py>
```

**Linting (all files):**
```bash
uv run ruff check --fix <file_or_directory>
```

### Step 3: Verify

```bash
uv run black --check <file.py>
uv run isort --check <file.py>
uv run ruff check <file.py>
```

## Installation

```bash
# Databricks projects
uv add --dev blackbricks ruff

# Regular Python projects
uv add --dev black isort ruff

# Mixed projects
uv add --dev black isort blackbricks ruff
```

## Configuration (pyproject.toml)

```toml
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

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
```

## Usage

### Format Single File
```bash
uv run python scripts/format_code.py <any_file.py>   # Auto-detects type
```

### Format Entire Project
```bash
uv run python scripts/format_code.py .                 # All Python files
uv run python scripts/format_code.py src/               # Specific directory
uv run python scripts/format_code.py src/ --skip-databricks  # Skip notebooks
```

### Check Only (CI/CD)
```bash
uv run python scripts/check_format.py .
uv run python scripts/check_format.py src/ --strict     # Exit with error if unformatted
```

### Run Individual Tools
```bash
uv run ruff check --fix .
uv run black src/
uv run isort src/
uv run blackbricks notebooks/
```

## Key Rules

- Always detect file type before formatting
- Use `blackbricks` for Databricks notebooks to preserve cell structure
- Run `isort` before `black` for regular files
- Run `ruff` last for final cleanup
- Use consistent line length (100) across all tools
- Skip formatting for generated or vendored code

## Scripts

- **scripts/format_code.py** - Auto-detects file types and applies correct formatters recursively
- **scripts/check_format.py** - Validates formatting without modifying files (for CI/CD)

## References

- [references/databricks-formatting.md](references/databricks-formatting.md) - Databricks notebook formatting details and examples
- [references/tool-comparison.md](references/tool-comparison.md) - Comparison of formatting tools
