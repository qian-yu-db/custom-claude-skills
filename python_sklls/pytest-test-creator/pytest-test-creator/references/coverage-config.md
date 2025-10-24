# Coverage Configuration Guide

Comprehensive guide to configuring and using coverage.py with pytest.

## Installation

```bash
uv add --dev pytest-cov
```

## Basic Usage

### Command Line

```bash
# Basic coverage
pytest --cov=src

# With missing line numbers
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html

# Multiple formats
pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml
```

## Configuration

### pyproject.toml (Recommended)

```toml
[tool.pytest.ini_options]
# Pytest configuration
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--cov=src",
    "--cov-report=term-missing:skip-covered",
    "--cov-fail-under=80",
]

[tool.coverage.run]
# What to measure
source = ["src"]
branch = true
parallel = true

# What to omit
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
    "*/site-packages/*",
    "*/__init__.py",
]

[tool.coverage.report]
# Reporting options
precision = 2
show_missing = true
skip_covered = false
skip_empty = true

# Ignore these lines
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "if typing.TYPE_CHECKING:",
    "@abstract",
    "@abstractmethod",
]

# Minimum coverage
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"
```

### .coveragerc (Alternative)

```ini
[run]
source = src
branch = True
omit =
    */tests/*
    */__pycache__/*
    */venv/*

[report]
precision = 2
show_missing = True
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__:

[html]
directory = htmlcov
```

## Coverage Options

### Source Specification

```toml
[tool.coverage.run]
# Single source directory
source = ["src"]

# Multiple source directories
source = ["src", "lib"]

# Specific packages
source = ["mypackage", "myotherpackage"]
```

### Omitting Files

```toml
[tool.coverage.run]
omit = [
    "*/tests/*",           # All test files
    "*/__pycache__/*",     # Compiled Python
    "*/migrations/*",      # Database migrations
    "*/venv/*",            # Virtual environment
    "*/.venv/*",           # Virtual environment
    "*/site-packages/*",   # Third-party packages
    "*/__init__.py",       # Init files
    "*/conftest.py",       # Pytest config
    "*/setup.py",          # Setup script
]
```

### Branch Coverage

```toml
[tool.coverage.run]
branch = true  # Measure branch coverage
```

Branch coverage checks if both `True` and `False` branches are tested:

```python
def check_value(x):
    if x > 0:        # Both branches need testing
        return "positive"
    else:
        return "non-positive"
```

### Excluding Lines

```toml
[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",              # Explicit exclusion
    "def __repr__",                  # String representations
    "raise AssertionError",          # Debug code
    "raise NotImplementedError",     # Abstract methods
    "if __name__ == .__main__.:",    # Script entry points
    "if TYPE_CHECKING:",             # Type checking blocks
    "@abstract",                     # Abstract decorators
    "@abstractmethod",               # Abstract methods
    "except ImportError:",           # Import fallbacks
    "pass",                          # Empty blocks
]
```

Using in code:

```python
def function():
    if debug:  # pragma: no cover
        print("Debug info")
    return process_data()
```

## Report Formats

### Terminal Report

```bash
# Basic terminal output
pytest --cov=src --cov-report=term

# With missing line numbers
pytest --cov=src --cov-report=term-missing

# Skip fully covered files
pytest --cov=src --cov-report=term-missing:skip-covered
```

Output:
```
Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
src/auth.py            45      3     12      1    92%   23-25, 67
src/utils.py           30      0      8      0   100%
---------------------------------------------------------------
TOTAL                  75      3     20      1    95%
```

### HTML Report

```bash
pytest --cov=src --cov-report=html
```

Configuration:
```toml
[tool.coverage.html]
directory = "htmlcov"           # Output directory
title = "My Project Coverage"   # Report title
```

Opens `htmlcov/index.html` in browser showing:
- File-by-file coverage
- Line-by-line highlighting
- Branch coverage details

### XML Report (for CI)

```bash
pytest --cov=src --cov-report=xml
```

Configuration:
```toml
[tool.coverage.xml]
output = "coverage.xml"
```

Used by:
- Codecov
- Coveralls
- SonarQube
- GitHub Actions

### JSON Report

```bash
pytest --cov=src --cov-report=json
```

Configuration:
```toml
[tool.coverage.json]
output = "coverage.json"
pretty_print = true
```

## Coverage Thresholds

### Minimum Coverage

```toml
[tool.coverage.report]
fail_under = 80  # Fail if coverage < 80%
```

Command line:
```bash
pytest --cov=src --cov-fail-under=80
```

### Per-File Thresholds

Not directly supported, but can use coverage combine with CI scripts.

## Advanced Features

### Context Tracking

Track coverage per test:

```toml
[tool.coverage.run]
dynamic_context = "test_function"
```

### Parallel Coverage

For parallel test execution:

```toml
[tool.coverage.run]
parallel = true
```

Then combine:
```bash
pytest -n auto --cov=src
coverage combine
coverage report
```

### Source Code Context

Show source code in reports:

```toml
[tool.coverage.report]
show_missing = true
```

### Precision

Control decimal places:

```toml
[tool.coverage.report]
precision = 2  # Show 95.23% instead of 95%
```

## Integrating with CI/CD

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e ".[test]"

      - name: Run tests with coverage
        run: |
          uv run pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### GitLab CI

```yaml
test:
  image: python:3.11
  script:
    - pip install uv
    - uv pip install -e ".[test]"
    - uv run pytest --cov=src --cov-report=xml --cov-report=term
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

## Coverage Badges

### Codecov

```markdown
[![codecov](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/user/repo)
```

### Coveralls

```markdown
[![Coverage Status](https://coveralls.io/repos/github/user/repo/badge.svg?branch=main)](https://coveralls.io/github/user/repo?branch=main)
```

## Best Practices

### 1. Set Realistic Thresholds

Start with current coverage and gradually increase:

```toml
[tool.coverage.report]
fail_under = 70  # Start here
# Later increase to 80, then 90
```

### 2. Focus on Important Code

Don't chase 100% coverage. Focus on:
- ✅ Business logic
- ✅ Data transformations
- ✅ API endpoints
- ✅ Error handling
- ❌ Simple getters/setters
- ❌ Configuration files
- ❌ Auto-generated code

### 3. Use Branch Coverage

```toml
[tool.coverage.run]
branch = true  # Catches untested conditions
```

### 4. Exclude Generated Code

```toml
[tool.coverage.run]
omit = [
    "*/migrations/*",
    "*/generated/*",
    "*_pb2.py",  # Protobuf
]
```

### 5. Review HTML Reports

HTML reports help identify:
- Untested branches
- Missing error handling
- Dead code

### 6. Combine with Other Metrics

Coverage ≠ Quality. Also use:
- Type checking (mypy)
- Linting (ruff)
- Code review
- Integration tests

## Common Patterns

### Testing Private Functions

```python
# Don't test private functions directly
def _internal_helper():  # pragma: no cover
    return "helper"

# Test through public API
def public_function():
    return _internal_helper()

# Test this instead
def test_public_function():
    assert public_function() == "helper"
```

### Platform-Specific Code

```python
import sys

if sys.platform == "win32":  # pragma: no cover
    # Windows-specific code
    pass
else:  # pragma: no cover
    # Unix-specific code
    pass
```

### Debug Code

```python
if DEBUG:  # pragma: no cover
    print("Debug info")
    log_details()
```

### Abstract Methods

```python
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod  # pragma: no cover
    def process(self):
        """Subclasses must implement."""
        pass
```

## Troubleshooting

### Low Coverage Despite Tests

**Problem**: Coverage shows low percentage but tests exist

**Solutions**:
1. Check `source` path matches your code location
2. Verify tests are importing from correct location
3. Look for untested branches (use `branch = true`)

### Coverage Not Generated

**Problem**: No coverage report generated

**Solutions**:
1. Ensure pytest-cov is installed: `uv pip list | grep pytest-cov`
2. Check source path is correct
3. Verify tests are actually running

### Import Errors in Coverage

**Problem**: Coverage fails with import errors

**Solutions**:
1. Install package in editable mode: `uv pip install -e .`
2. Set PYTHONPATH: `export PYTHONPATH="${PWD}/src"`
3. Check `omit` patterns aren't too broad

### Different Coverage Locally vs CI

**Problem**: Coverage differs between environments

**Solutions**:
1. Use same Python version
2. Ensure same dependencies with lock file
3. Check `.coveragerc` or `pyproject.toml` is committed
4. Use `parallel = true` for parallel tests

## Coverage Reports Analysis

### Reading Terminal Report

```
Name                Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------
src/auth.py            45      3     12      1    92%   23-25, 67
```

- **Stmts**: Total statements
- **Miss**: Uncovered statements
- **Branch**: Total branches
- **BrPart**: Partially covered branches
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

### Reading HTML Report

Colors in HTML:
- 🟢 **Green**: Covered
- 🔴 **Red**: Not covered
- 🟡 **Yellow**: Partially covered branch

## Summary

1. Configure coverage in `pyproject.toml`
2. Use `--cov-report=term-missing` for development
3. Generate HTML reports for detailed analysis
4. Set `fail_under` threshold for CI
5. Enable branch coverage
6. Exclude appropriate files
7. Focus on meaningful coverage, not 100%
8. Integrate with CI/CD and coverage services
