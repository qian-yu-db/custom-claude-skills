# Pytest Test Creator Skill

## Purpose

This skill helps Claude automatically generate comprehensive unit tests for Python codebases, run tests with pytest, and generate coverage reports. It uses `uv` for fast, modern Python package management.

## When to Activate

This skill should activate when the user requests:
- "Create unit tests for this code"
- "Generate pytest tests for my project"
- "Run tests and show coverage"
- "Set up pytest for my codebase"
- "Add test coverage to this module"
- "Write tests based on my codebase"

## Core Capabilities

### 1. Codebase Analysis
- Scan project structure to identify testable modules
- Analyze functions, classes, and methods
- Detect dependencies and imports
- Identify edge cases and test scenarios
- Understand type hints and docstrings

### 2. Test Generation
- Create pytest test files following conventions
- Generate test functions with descriptive names
- Include fixtures for common setup/teardown
- Add parametrized tests for multiple scenarios
- Mock external dependencies
- Test edge cases and error conditions

### 3. Test Execution
- Run pytest with appropriate options
- Generate HTML and terminal coverage reports
- Display results with clear pass/fail indicators
- Show coverage percentages by module
- Identify untested code paths

### 4. Package Management with UV
- Use `uv` for fast dependency installation
- Manage test dependencies separately
- Create/update `pyproject.toml` configuration
- Handle virtual environments efficiently

## Workflow

### Step 1: Analyze Codebase
1. Ask user for target module/directory (or analyze entire project)
2. Use the Glob tool to find Python files
3. Use the Read tool to examine source code
4. Identify:
   - Functions and classes to test
   - Dependencies and imports
   - Type signatures
   - Docstrings and expected behavior
   - Existing test files (to avoid duplication)

### Step 2: Generate Tests
1. For each module, create corresponding test file in `tests/` directory
2. Follow naming convention: `test_<module_name>.py`
3. Generate tests that cover:
   - **Happy path**: Normal expected usage
   - **Edge cases**: Boundary conditions, empty inputs
   - **Error cases**: Invalid inputs, exceptions
   - **Integration**: How components work together
4. Use fixtures for:
   - Sample data
   - Mock objects
   - Database connections
   - API clients
5. Add docstrings to test functions explaining what's being tested

### Step 3: Setup Test Environment
1. Check if `uv` is installed, guide user to install if not
2. Ensure pytest and coverage tools are in dependencies:
   ```toml
   [project.optional-dependencies]
   test = [
       "pytest>=7.4.0",
       "pytest-cov>=4.1.0",
       "pytest-mock>=3.11.0",
   ]
   ```
3. Create/update `pytest.ini` or `pyproject.toml` with pytest config
4. Install dependencies: `uv pip install -e ".[test]"`

### Step 4: Run Tests
1. Execute: `uv run pytest --cov=<package> --cov-report=html --cov-report=term`
2. Display results in terminal
3. Generate HTML coverage report in `htmlcov/`
4. Summarize:
   - Total tests run
   - Pass/fail count
   - Coverage percentage
   - Areas needing more coverage

## Test Generation Patterns

### Basic Function Test
```python
def test_function_name_normal_case():
    """Test that function_name handles normal inputs correctly."""
    result = function_name(valid_input)
    assert result == expected_output
```

### Parametrized Test
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (5, 10),
    (0, 0),
])
def test_function_with_multiple_inputs(input, expected):
    """Test function with various input values."""
    assert function_name(input) == expected
```

### Exception Test
```python
def test_function_raises_error_on_invalid_input():
    """Test that function raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        function_name(invalid_input)
```

### Fixture Usage
```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using fixture data."""
    result = process_data(sample_data)
    assert result is not None
```

### Mocking External Dependencies
```python
def test_api_call(mocker):
    """Test function that calls external API."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": "ok"}
    mocker.patch('requests.get', return_value=mock_response)

    result = fetch_data()
    assert result["status"] == "ok"
```

### Class Test
```python
class TestMyClass:
    """Test suite for MyClass."""

    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return MyClass(param="value")

    def test_method(self, instance):
        """Test MyClass.method."""
        result = instance.method()
        assert result == expected
```

## UV Package Management

### Installation Check
```bash
# Check if uv is installed
which uv || echo "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
```

### Setup Project
```bash
# Initialize pyproject.toml if needed
uv init

# Add test dependencies
uv add --dev pytest pytest-cov pytest-mock
```

### Run Tests
```bash
# Install dependencies and run tests
uv pip install -e ".[test]"
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html --cov-report=term-missing
```

## Configuration Files

### pyproject.toml (Pytest Config)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

## Best Practices

### Test Naming
- ✅ `test_function_name_with_valid_input()`
- ✅ `test_class_method_raises_error_when_invalid()`
- ❌ `test_1()`, `test_stuff()`

### Test Organization
- One test file per source module
- Group related tests in classes
- Use fixtures for common setup
- Keep tests independent (no shared state)

### Coverage Goals
- Aim for >80% code coverage
- Focus on critical business logic first
- Don't test trivial getters/setters excessively
- Test edge cases and error paths

### What to Test
- ✅ Business logic
- ✅ Data transformations
- ✅ API endpoints
- ✅ Error handling
- ✅ Edge cases
- ❌ Third-party library internals
- ❌ Auto-generated code

## Reference Files

The skill includes these reference documents (Claude will read these when needed):

- `references/pytest-patterns.md` - Comprehensive pytest patterns and examples
- `references/mocking-guide.md` - Guide to mocking with pytest-mock
- `references/coverage-config.md` - Coverage configuration and best practices
- `references/uv-commands.md` - UV package management commands
- `references/databricks-notebook-testing.md` - Special guide for testing Databricks Python notebooks

## Scripts

### scripts/generate_tests.py
Analyzes source files and generates test templates.

**Usage:**
```bash
python scripts/generate_tests.py <source_file_or_directory>
```

**Features:**
- Scans Python files for functions and classes
- Generates test file with test stubs
- Includes appropriate fixtures
- Adds parametrize decorators where applicable

### scripts/run_tests.py
Runs pytest with coverage and generates reports.

**Usage:**
```bash
python scripts/run_tests.py [--coverage] [--html] [path]
```

**Features:**
- Executes pytest with optimal settings
- Generates coverage reports
- Opens HTML report in browser
- Summarizes results

## User Interaction Flow

1. **User Request**: "Create tests for my authentication module"

2. **Claude Actions**:
   - Read `src/auth.py` to understand the code
   - Identify testable functions and classes
   - Check for existing tests in `tests/test_auth.py`
   - Generate comprehensive test cases
   - Ensure pytest and coverage tools are available
   - Run tests to verify they work
   - Show coverage report

3. **Claude Response**:
   - "I've created comprehensive tests for your authentication module in `tests/test_auth.py`"
   - Shows test file with all test functions
   - Displays test results and coverage
   - Suggests areas that need more coverage
   - Provides commands to run tests again

## Error Handling

### Missing Dependencies
If pytest or coverage not installed:
```bash
uv add --dev pytest pytest-cov pytest-mock
```

### Import Errors in Tests
- Ensure source package is installed: `uv pip install -e .`
- Check Python path configuration
- Verify test file imports match source structure

### Coverage Not Working
- Ensure source code is in proper package structure
- Check `[tool.coverage.run]` source paths
- Verify tests are actually importing from source (not duplicates)

## Quality Checklist

Before completing, ensure:
- [ ] All public functions have at least one test
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Coverage is >80% for new code
- [ ] All tests pass
- [ ] No hardcoded values (use fixtures/parametrize)
- [ ] Tests are independent and can run in any order
- [ ] Docstrings explain what each test does

## Example Output

```
========================= test session starts ==========================
collected 45 items

tests/test_auth.py ......................................... [100%]

---------- coverage: platform darwin, python 3.11.5 -----------
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/auth.py             82      3    96%   45-47
--------------------------------------------------
TOTAL                   82      3    96%

========================= 45 passed in 1.23s ===========================
```

## Tips for Claude

- Always read the source code before generating tests
- Look for existing test patterns in the codebase
- Match the project's testing style and conventions
- Use type hints to infer test cases
- Check docstrings for expected behavior
- Generate meaningful test names that describe what's being tested
- Include comments in tests to explain complex assertions
- Suggest improvements to source code if it's hard to test
