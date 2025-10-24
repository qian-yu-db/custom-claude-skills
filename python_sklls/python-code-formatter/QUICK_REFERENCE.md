# Python Code Formatter - Quick Reference

## Common Claude Prompts

### Format Code
```
"Format my Python code"
"Format all files in src/"
"Format this Databricks notebook"
"Fix code style in my project"
"Auto-format this file"
```

### Check Formatting
```
"Check if my code is properly formatted"
"Verify formatting for CI/CD"
"Is my code formatted correctly?"
```

### Setup
```
"Set up code formatting with black and ruff"
"Configure formatters for my project"
"Install formatting tools with uv"
```

## UV Commands

### Install Formatters

```bash
# For Databricks projects
uv add --dev blackbricks ruff

# For regular Python projects
uv add --dev black isort ruff

# For mixed projects (recommended)
uv add --dev black isort blackbricks ruff
```

### Run Formatters

```bash
# Format with automatic tool selection
uv run python scripts/format_code.py .

# Check only (no modifications)
uv run python scripts/check_format.py .

# Format specific file
uv run python scripts/format_code.py src/utils.py
```

## Direct Tool Commands

### Databricks Notebooks

```bash
# Format single notebook
uv run blackbricks notebooks/etl_pipeline.py

# Format all notebooks
uv run blackbricks notebooks/

# Check only
uv run blackbricks --check notebooks/
```

### Regular Python Files

```bash
# Sort imports
uv run isort src/

# Format code
uv run black src/

# Check formatting
uv run black --check src/
uv run isort --check src/
```

### Ruff (All Files)

```bash
# Lint and auto-fix
uv run ruff check --fix .

# Check only
uv run ruff check .

# Format (alternative to black)
uv run ruff format .

# Specific file
uv run ruff check --fix src/utils.py
```

## Script Usage

### format_code.py

```bash
# Format entire project
python scripts/format_code.py .

# Format specific directory
python scripts/format_code.py src/

# Format single file
python scripts/format_code.py src/utils.py

# Skip Databricks notebooks
python scripts/format_code.py --skip-databricks src/

# Skip regular Python files
python scripts/format_code.py --skip-regular notebooks/

# Check without modifying
python scripts/format_code.py --check .

# Verbose output
python scripts/format_code.py -v src/

# Install missing dependencies
python scripts/format_code.py --install-deps .
```

### check_format.py

```bash
# Check current directory
python scripts/check_format.py

# Check specific path
python scripts/check_format.py src/

# Skip certain file types
python scripts/check_format.py --skip-databricks .

# Verbose output
python scripts/check_format.py -v .
```

## Configuration

### pyproject.toml

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
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true

[tool.blackbricks]
line_length = 100
target_version = ['py311']

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
    "E501",  # line too long (handled by formatters)
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports OK in __init__
"notebooks/*.py" = ["E402"]  # Import not at top (Databricks cells)
```

## Pre-commit Hooks

### Install Pre-commit

```bash
uv add --dev pre-commit
uv run pre-commit install
```

### .pre-commit-config.yaml

```yaml
repos:
  # Ruff (fast linting and formatting)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Black (regular Python files only)
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        exclude: '^.*# Databricks notebook source.*$'

  # isort (regular Python files only)
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        exclude: '^.*# Databricks notebook source.*$'

  # blackbricks (Databricks notebooks only)
  - repo: local
    hooks:
      - id: blackbricks
        name: blackbricks
        entry: blackbricks
        language: system
        types: [python]
        # Only run on files with Databricks marker
        files: '.*# Databricks notebook source.*'
```

### Run Pre-commit

```bash
# Run on all files
uv run pre-commit run --all-files

# Run on staged files only
uv run pre-commit run

# Update hooks
uv run pre-commit autoupdate
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Format Check

on: [push, pull_request]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv add --dev black isort blackbricks ruff

      - name: Check formatting
        run: |
          python scripts/check_format.py .
          exit_code=$?
          if [ $exit_code -ne 0 ]; then
            echo "::error::Code is not properly formatted"
            echo "Run: python scripts/format_code.py ."
            exit 1
          fi
```

### GitLab CI

```yaml
format-check:
  image: python:3.11
  script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.cargo/bin:$PATH"
    - uv add --dev black isort blackbricks ruff
    - python scripts/check_format.py .
  only:
    - merge_requests
    - main
```

## Tool Comparison

| Tool | Purpose | Speed | Files |
|------|---------|-------|-------|
| **blackbricks** | Format Databricks notebooks | Fast | `.py` with DB markers |
| **black** | Format regular Python | Fast | Regular `.py` files |
| **isort** | Sort imports | Very Fast | Regular `.py` files |
| **ruff** | Lint + auto-fix | Ultra Fast | All `.py` files |

## Common Workflows

### Format Before Commit

```bash
# 1. Format code
python scripts/format_code.py .

# 2. Check if formatted correctly
python scripts/check_format.py .

# 3. Stage and commit
git add .
git commit -m "Your message"
```

### Setup New Project

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Initialize project
uv init

# 3. Add formatters
uv add --dev black isort blackbricks ruff

# 4. Create pyproject.toml config
# (see Configuration section above)

# 5. Format existing code
python scripts/format_code.py .
```

### CI/CD Pipeline

```bash
# 1. Install dependencies
uv add --dev black isort blackbricks ruff

# 2. Check formatting
python scripts/check_format.py .

# 3. Exit with error if not formatted
# (script exits with code 1 if issues found)
```

## File Type Detection

### Databricks Notebook
Detected by:
```python
# Databricks notebook source  # <- This marker
```

### Regular Python File
Any `.py` file without Databricks marker

## Formatting Order

### Databricks Notebooks
1. `blackbricks` - Format code cells
2. `ruff --fix` - Fix linting issues

### Regular Python Files
1. `isort` - Sort imports
2. `black` - Format code
3. `ruff --fix` - Fix linting issues

## Common Options

### Line Length

```toml
# Consistent across all tools
[tool.black]
line-length = 100

[tool.isort]
line_length = 100

[tool.blackbricks]
line_length = 100

[tool.ruff]
line-length = 100
```

### Python Version

```toml
# Target Python version
[tool.black]
target-version = ['py311']

[tool.blackbricks]
target_version = ['py311']

[tool.ruff]
target-version = "py311"
```

### Exclude Patterns

```toml
[tool.black]
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | build
  | dist
  | __pycache__
)/
'''

[tool.ruff]
exclude = [
    ".git",
    ".venv",
    "build",
    "dist",
]
```

## Troubleshooting

### Missing Dependencies

```bash
# Install missing tools
uv add --dev black isort blackbricks ruff

# Or use auto-install
python scripts/format_code.py --install-deps .
```

### Syntax Errors

```bash
# Formatters won't work on files with syntax errors
# Fix syntax first, then format
python -m py_compile file.py  # Check syntax
```

### Different Results Locally vs CI

```bash
# Ensure same versions
uv lock  # Create lock file
uv sync  # Use lock file

# Commit uv.lock
git add uv.lock
```

### Databricks Structure Broken

```bash
# Use blackbricks, not black
uv run blackbricks notebook.py

# NOT: uv run black notebook.py
```

## Quick Tips

1. **Always use the right tool**:
   - Databricks notebooks → `blackbricks`
   - Regular Python → `black + isort`

2. **Run ruff last**:
   - It catches issues the formatters miss

3. **Check before committing**:
   ```bash
   python scripts/check_format.py .
   ```

4. **Use pre-commit hooks**:
   - Automates formatting
   - Prevents unformatted commits

5. **Keep config consistent**:
   - Same line length everywhere
   - Compatible tool settings

## Resources

- Black: https://black.readthedocs.io
- isort: https://pycqa.github.io/isort/
- Ruff: https://docs.astral.sh/ruff/
- blackbricks: https://github.com/inspera/blackbricks
- UV: https://github.com/astral-sh/uv
