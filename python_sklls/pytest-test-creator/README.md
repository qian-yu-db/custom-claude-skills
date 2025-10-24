# Pytest Test Creator Skill

🎯 **Purpose**: Automatically generate comprehensive unit tests for Python codebases, run tests with pytest, and generate coverage reports using modern `uv` package management.

## 📦 Package Contents

| File | Description |
|------|-------------|
| `pytest-test-creator/` | **Main skill package** - Add to .claude/skills/ |
| `README.md` | This file - your starting point |
| `QUICK_REFERENCE.md` | Quick reference card for common operations |

## 🚀 Quick Start

### 1. Install the Skill
- Upload `pytest-test-creator.zip` to Claude
- The skill activates when you request test generation or execution

### 2. Use the Skill
Simply tell Claude what you need:

```
"Create unit tests for my authentication module"
"Generate tests for src/utils/parser.py"
"Run all tests with coverage report"
"Set up pytest for this project"
```

### 3. Get Comprehensive Tests
Claude will:
- Analyze your source code
- Generate test files with fixtures and assertions
- Run tests and show coverage
- Suggest improvements for better testing

## 🎯 What This Skill Does

### Input
You provide:
- Path to source code file or directory
- Type of tests needed (unit, integration, etc.)
- Coverage requirements
- Any specific test scenarios

### Output
You get:
- Complete test files following pytest conventions
- Fixtures for common test data
- Parametrized tests for multiple scenarios
- Mocking for external dependencies
- Coverage reports (terminal + HTML)
- Test execution results

### Example Transformation

**You say:**
```
"Create tests for my user authentication module in src/auth.py"
```

**You get:**
- `tests/test_auth.py` with:
  - Test fixtures for user data
  - Happy path tests
  - Edge case tests
  - Error handling tests
  - Parametrized tests for multiple inputs
  - Mock objects for database/API calls
- Coverage report showing 85%+ coverage
- HTML report you can browse

## 🔥 Key Features

### Intelligent Code Analysis
- Scans functions, classes, and methods
- Understands type hints and docstrings
- Detects dependencies and imports
- Identifies edge cases automatically

### Comprehensive Test Generation
- **Happy path tests**: Normal expected behavior
- **Edge cases**: Boundary conditions, empty inputs
- **Error cases**: Invalid inputs, exceptions
- **Parametrized tests**: Multiple input scenarios
- **Fixtures**: Reusable test data and objects
- **Mocking**: External dependencies (APIs, databases)

### Modern Package Management
- Uses `uv` for fast dependency installation
- Manages test dependencies separately
- Configures `pyproject.toml` automatically
- Handles virtual environments efficiently

### Coverage Reporting
- Terminal output with missing line numbers
- HTML reports with line-by-line highlighting
- Configurable coverage thresholds
- Identifies untested code paths

## 💡 Common Use Cases

### Generate Tests for New Code
```
"Create tests for the new payment processing module"
```

### Add Tests to Legacy Code
```
"Generate comprehensive tests for src/legacy/data_processor.py"
```

### Run Tests with Coverage
```
"Run all tests and show me what's not covered"
```

### Test Specific Functionality
```
"Create tests for error handling in the API client"
```

### Set Up Testing Infrastructure
```
"Set up pytest for this project with coverage and mocking"
```

## 📝 Test Patterns Included

### Basic Function Test
```python
def test_calculate_total_normal_case():
    """Test calculate_total with valid inputs."""
    result = calculate_total([10, 20, 30])
    assert result == 60
```

### Parametrized Test
```python
@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),
    ([0], 0),
    ([], 0),
])
def test_calculate_total_various_inputs(input, expected):
    """Test calculate_total with multiple scenarios."""
    assert calculate_total(input) == expected
```

### Exception Testing
```python
def test_divide_raises_error_on_zero():
    """Test that divide raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Fixture Usage
```python
@pytest.fixture
def user_data():
    """Provide sample user data for tests."""
    return {"username": "test", "email": "test@example.com"}

def test_create_user(user_data):
    """Test user creation with fixture data."""
    user = create_user(user_data)
    assert user.username == "test"
```

### Mocking External APIs
```python
def test_fetch_weather(mocker):
    """Test weather API call with mocked response."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"temp": 72}
    mocker.patch('requests.get', return_value=mock_response)

    weather = fetch_weather("Seattle")
    assert weather["temp"] == 72
```

## 🔧 How It Works

### For Test Generation
1. **Analyze**: Claude reads your source code
2. **Extract**: Identifies functions, classes, dependencies
3. **Generate**: Creates comprehensive test templates
4. **Enhance**: Adds fixtures, parametrization, mocking
5. **Validate**: Runs tests to ensure they work

### For Test Execution
1. **Setup**: Ensures pytest and coverage tools are installed
2. **Execute**: Runs pytest with optimal settings
3. **Report**: Generates coverage reports (terminal + HTML)
4. **Analyze**: Identifies gaps in test coverage
5. **Suggest**: Recommends additional tests needed

## 🎓 Learning Path

### Beginner
1. Start with simple function tests
2. Try the "Generate tests for <file>" command
3. Review generated tests to understand patterns

### Intermediate
1. Use fixtures for complex test data
2. Parametrize tests for multiple scenarios
3. Add mocking for external dependencies

### Advanced
1. Create custom fixtures
2. Write integration tests
3. Configure coverage thresholds
4. Set up CI/CD test automation

## 📚 Documentation Quick Links

| Need | See |
|------|-----|
| Quick commands | `QUICK_REFERENCE.md` |
| Pytest patterns | `references/pytest-patterns.md` (in package) |
| Mocking guide | `references/mocking-guide.md` (in package) |
| Coverage config | `references/coverage-config.md` (in package) |
| UV commands | `references/uv-commands.md` (in package) |

## ⚙️ Prerequisites

Before using this skill:

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Ensure Python 3.10+**:
   ```bash
   python --version
   ```

3. **Project structure** (recommended):
   ```
   your-project/
   ├── src/           # Source code
   ├── tests/         # Test files
   └── pyproject.toml # Project config
   ```

## 🛠️ What Gets Created

When Claude generates tests, you'll get:

### Test File Structure
```python
"""Tests for <module> module."""

import pytest
from src.module import MyClass, my_function

# Fixtures
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

# Function tests
def test_my_function_normal_case():
    """Test with valid input."""
    # Test implementation

def test_my_function_edge_cases():
    """Test with edge cases."""
    # Test implementation

# Class tests
class TestMyClass:
    """Test suite for MyClass."""

    def test_method(self, sample_data):
        """Test MyClass.method."""
        # Test implementation
```

### Configuration Files

**pyproject.toml** (pytest config):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = ["--strict-markers", "-ra"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
precision = 2
show_missing = true
```

## 💎 Best Practices Built In

### Test Naming
✅ Descriptive names explaining what's tested
✅ Follow pattern: `test_<function>_<scenario>()`
✅ Group related tests in classes

### Test Organization
✅ One test file per source module
✅ Use fixtures for common setup
✅ Keep tests independent
✅ Test one thing per test function

### Coverage Goals
✅ Aim for >80% code coverage
✅ Focus on critical business logic
✅ Test edge cases and error paths
✅ Don't over-test trivial code

### What to Test
✅ Business logic and algorithms
✅ Data transformations
✅ API endpoints and handlers
✅ Error handling and validation
✅ Edge cases and boundaries
❌ Third-party library internals
❌ Simple getters/setters
❌ Auto-generated code

## 🎯 Example Prompts

### Simple
```
"Create tests for my calculator.py file"
```

### Detailed
```
"Generate comprehensive tests for src/api/auth.py including
edge cases, error handling, and mocking for the database calls"
```

### With Coverage
```
"Run all tests and generate an HTML coverage report.
Show me which functions need more test coverage"
```

### Setup Request
```
"Set up pytest with coverage for this project using uv.
I want tests in a tests/ directory and coverage reports"
```

## 🤝 Getting Help

### From Claude
- "Show me pytest patterns from the references"
- "How do I mock this API call?"
- "What's the best way to test this async function?"
- "Explain this test failure"

### From Documentation
- Check `QUICK_REFERENCE.md` for commands
- See package references for advanced patterns
- Read pytest documentation for deep dives

## 📦 What's In The Skill Package

```
pytest-test-creator/
├── SKILL.md                      # Main skill instructions
├── scripts/
│   ├── generate_tests.py         # Test generation script
│   └── run_tests.py              # Test execution script
└── references/
    ├── pytest-patterns.md        # Comprehensive patterns
    ├── mocking-guide.md          # Mocking with pytest-mock
    ├── coverage-config.md        # Coverage configuration
    └── uv-commands.md            # UV package management
```

## 🚀 Next Steps

1. **Upload** `pytest-test-creator.zip` to Claude
2. **Try** generating tests for a simple module
3. **Review** the generated tests
4. **Run** tests with coverage
5. **Iterate** to improve coverage

## 📋 System Requirements

- Python 3.10 or higher
- uv package manager
- Git (recommended for version control)

## 🎉 Benefits

- ⚡ **Fast**: Generate comprehensive tests in seconds
- ✅ **Thorough**: Covers happy path, edge cases, and errors
- 🎯 **Smart**: Understands your code structure
- 📊 **Visual**: HTML coverage reports
- 🚀 **Modern**: Uses uv for speed
- 📚 **Educational**: Learn pytest best practices

## 🔗 Integration

### With CI/CD
Generated tests work seamlessly with:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

### With IDEs
Works great with:
- VS Code (Python extension)
- PyCharm
- Cursor
- Any editor with pytest support

### With Other Tools
Integrates with:
- pre-commit hooks
- Coverage.py
- pytest plugins (pytest-asyncio, pytest-django, etc.)

## 📜 License

Apache-2.0

## 🙋 Support

For issues or questions:
- Ask Claude to reference the skill documentation
- Check `QUICK_REFERENCE.md` for common commands
- Review the references in the skill package
- Consult pytest documentation

---

**Ready to get started?** Upload `pytest-test-creator.zip` to Claude and start testing!
