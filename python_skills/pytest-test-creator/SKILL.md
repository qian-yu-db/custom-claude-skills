---
name: pytest-test-creator
description: Auto-generate comprehensive unit tests for Python codebases with pytest, coverage reports, and uv package management. Use when creating tests, setting up pytest, analyzing test coverage, or testing Databricks notebooks with local Spark. Generates fixtures, parametrized tests, mocking, and coverage reports.
---

# Pytest Test Creator Skill

Auto-generate comprehensive unit tests for Python codebases, run tests with pytest, and generate coverage reports using `uv` for package management.

## Workflow

### Step 1: Analyze Codebase

1. Find Python files with Glob tool
2. Read source code to identify functions, classes, type signatures, docstrings
3. Check for existing tests to avoid duplication

### Step 2: Generate Tests

For each module, create `tests/test_<module_name>.py` covering:
- **Happy path**: Normal expected usage
- **Edge cases**: Boundary conditions, empty inputs
- **Error cases**: Invalid inputs, exceptions
- **Integration**: How components work together

Use fixtures for sample data, mock objects, and shared setup.

### Step 3: Setup Test Environment

Ensure dependencies are in `pyproject.toml`:

```toml
[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
]
```

```bash
uv add --dev pytest pytest-cov pytest-mock
```

### Step 4: Run Tests

```bash
uv run pytest --cov=src --cov-report=html --cov-report=term-missing
```

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["--strict-markers", "--strict-config", "-ra"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

## Best Practices

- **Naming**: `test_function_name_with_valid_input()`, not `test_1()`
- **Organization**: One test file per source module, group related tests in classes
- **Coverage**: Aim for >80%, focus on critical business logic first
- **Independence**: No shared mutable state between tests
- **What to test**: Business logic, data transformations, error handling, edge cases
- **What to skip**: Third-party library internals, auto-generated code, trivial getters/setters

## Scripts

- **scripts/generate_tests.py** - Analyzes source files and generates test templates with fixtures and parametrize decorators
- **scripts/run_tests.py** - Runs pytest with coverage and generates reports (`--coverage`, `--html` flags)

## References

- [references/pytest-patterns.md](references/pytest-patterns.md) - Comprehensive pytest patterns and examples
- [references/mocking-guide.md](references/mocking-guide.md) - Guide to mocking with pytest-mock
- [references/coverage-config.md](references/coverage-config.md) - Coverage configuration and best practices
- [references/uv-commands.md](references/uv-commands.md) - UV package management commands
- [references/databricks-notebook-testing.md](references/databricks-notebook-testing.md) - Testing Databricks Python notebooks
