# Pytest Test Creator - Quick Reference

## Common Claude Prompts

### Generate Tests
```
"Create tests for src/auth.py"
"Generate unit tests for my calculator module"
"Add tests for the UserService class"
"Create comprehensive tests for src/api/handlers.py"
```

### Run Tests
```
"Run all tests with coverage"
"Execute tests for the auth module"
"Run tests and show me the HTML coverage report"
"Test the API endpoints and show results"
```

### Coverage Analysis
```
"Show me what's not covered by tests"
"Which functions need more test coverage?"
"Generate coverage report for src/ directory"
```

### Setup
```
"Set up pytest for this project"
"Configure pytest with uv and coverage"
"Initialize testing infrastructure"
```

## UV Commands

### Install Test Dependencies
```bash
# Add pytest and coverage tools
uv add --dev pytest pytest-cov pytest-mock

# Install project with test dependencies
uv pip install -e ".[test]"
```

### Run Tests
```bash
# Basic test run
uv run pytest

# With coverage
uv run pytest --cov=src

# With HTML report
uv run pytest --cov=src --cov-report=html

# Verbose output
uv run pytest -v

# Specific file
uv run pytest tests/test_auth.py

# Specific test
uv run pytest tests/test_auth.py::test_login
```

## Pytest Commands

### Running Tests
```bash
# All tests
pytest

# Specific directory
pytest tests/

# Specific file
pytest tests/test_auth.py

# Specific test function
pytest tests/test_auth.py::test_login

# Specific test class
pytest tests/test_auth.py::TestAuth

# Match keyword
pytest -k "auth"

# Match marker
pytest -m "slow"
```

### Verbosity Options
```bash
pytest -v          # Verbose
pytest -vv         # Very verbose
pytest -q          # Quiet
pytest --tb=short  # Short traceback
pytest --tb=line   # One-line traceback
```

### Coverage Options
```bash
# Basic coverage
pytest --cov=src

# With missing lines
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html

# XML report (for CI)
pytest --cov=src --cov-report=xml

# Set minimum coverage
pytest --cov=src --cov-fail-under=80
```

### Useful Flags
```bash
-x              # Stop on first failure
--maxfail=2     # Stop after 2 failures
--lf            # Run last failed tests
--ff            # Run failures first
--pdb           # Drop into debugger on failure
-s              # Don't capture output (show prints)
--durations=10  # Show 10 slowest tests
```

## Test Patterns

### Basic Test
```python
def test_function_name():
    """Test description."""
    result = function()
    assert result == expected
```

### Parametrized Test
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (5, 10),
])
def test_multiply(input, expected):
    assert multiply(input, 2) == expected
```

### Exception Test
```python
def test_raises_error():
    with pytest.raises(ValueError):
        invalid_function()
```

### Fixture
```python
@pytest.fixture
def data():
    return {"key": "value"}

def test_with_fixture(data):
    assert data["key"] == "value"
```

### Mocking
```python
def test_with_mock(mocker):
    mock = mocker.patch('module.function')
    mock.return_value = "mocked"
    assert call_function() == "mocked"
```

### Class Tests
```python
class TestClass:
    def test_method(self):
        assert True
```

## Markers

### Define Markers
```python
# In test file
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_api_call():
    pass
```

### Use Markers
```bash
# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"

# Multiple markers
pytest -m "slow or integration"
```

### Register Markers (pyproject.toml)
```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "unit: marks unit tests",
]
```

## Coverage Configuration

### pyproject.toml
```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Project Structure

### Recommended Layout
```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   └── test_module.py
├── pyproject.toml
└── README.md
```

### Test File Naming
- `test_*.py` or `*_test.py`
- `test_<module_name>.py` (preferred)

### Test Function Naming
- `test_<function>_<scenario>`
- Examples:
  - `test_login_with_valid_credentials`
  - `test_calculate_total_with_empty_list`
  - `test_api_raises_error_on_timeout`

## Common Fixtures

### Temporary Files
```python
def test_with_temp_file(tmp_path):
    """tmp_path is a built-in fixture."""
    file = tmp_path / "test.txt"
    file.write_text("content")
    assert file.read_text() == "content"
```

### Monkeypatch
```python
def test_env_var(monkeypatch):
    """Monkeypatch environment variables."""
    monkeypatch.setenv("API_KEY", "test-key")
    assert os.getenv("API_KEY") == "test-key"
```

### Capsys (Capture Output)
```python
def test_print(capsys):
    """Capture printed output."""
    print("hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out
```

## Scripts Usage

### Generate Tests
```bash
# Single file
python scripts/generate_tests.py src/auth.py

# Directory
python scripts/generate_tests.py src/

# Custom output directory
python scripts/generate_tests.py src/auth.py -o custom_tests/

# Verbose
python scripts/generate_tests.py src/ -v
```

### Run Tests
```bash
# All tests with coverage
python scripts/run_tests.py --coverage

# HTML report
python scripts/run_tests.py --html

# Specific path
python scripts/run_tests.py tests/test_auth.py

# Keyword filter
python scripts/run_tests.py -k "login"

# Marker filter
python scripts/run_tests.py -m "integration"

# Verbose
python scripts/run_tests.py -v

# Custom source directory
python scripts/run_tests.py --source mypackage

# Check dependencies
python scripts/run_tests.py --check-deps
```

## Troubleshooting

### Tests Not Found
```bash
# Check test discovery
pytest --collect-only

# Verify naming conventions
# Files: test_*.py
# Functions: test_*()
# Classes: Test*
```

### Import Errors
```bash
# Install package in editable mode
uv pip install -e .

# Or add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

### Coverage Not Working
```bash
# Verify source paths in pyproject.toml
[tool.coverage.run]
source = ["src"]  # Must match your package location
```

### Slow Tests
```bash
# Profile test duration
pytest --durations=10

# Run in parallel (requires pytest-xdist)
uv add --dev pytest-xdist
pytest -n auto
```

## Best Practices

### Test Independence
✅ Each test should run independently
✅ Use fixtures for setup/teardown
✅ Don't rely on test execution order
❌ Don't use global state

### Test Coverage
✅ Aim for >80% coverage
✅ Test edge cases and errors
✅ Focus on business logic
❌ Don't chase 100% blindly

### Test Naming
✅ Descriptive names
✅ Explain what's being tested
✅ Include scenario/condition
❌ Generic names (test1, test2)

### Test Organization
✅ One test file per module
✅ Group related tests in classes
✅ Use clear section comments
❌ Mix unit and integration tests

## Quick Tips

1. **Run failed tests first**: `pytest --ff`
2. **Stop on first failure**: `pytest -x`
3. **Show print statements**: `pytest -s`
4. **Drop into debugger**: `pytest --pdb`
5. **Generate HTML report**: `pytest --cov=src --cov-report=html`
6. **Update snapshots**: Use `pytest --snapshot-update` (with pytest-snapshot)
7. **Parallel execution**: `pytest -n auto` (requires pytest-xdist)
8. **Rerun failures**: `pytest --lf`

## Keyboard Shortcuts (in PDB debugger)

- `n` - Next line
- `s` - Step into function
- `c` - Continue execution
- `l` - List current location
- `p <var>` - Print variable
- `q` - Quit debugger

## Resources

- Pytest docs: https://docs.pytest.org
- Coverage.py: https://coverage.readthedocs.io
- UV docs: https://github.com/astral-sh/uv
- Pytest plugins: https://docs.pytest.org/en/latest/reference/plugin_list.html
