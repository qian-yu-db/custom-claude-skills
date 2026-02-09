# UV Package Management Commands

Complete reference for using `uv` with Python projects and pytest.

## Installation

### Install UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv

# With pipx
pipx install uv
```

### Verify Installation

```bash
uv --version
```

## Project Setup

### Initialize New Project

```bash
# Create new project
uv init my-project
cd my-project

# With specific Python version
uv init my-project --python 3.11
```

### Initialize in Existing Project

```bash
# In project directory
uv init

# Creates:
# - pyproject.toml
# - .python-version (optional)
```

## Dependency Management

### Add Dependencies

```bash
# Add production dependency
uv add requests

# Add multiple dependencies
uv add requests pandas numpy

# Add with version constraint
uv add "requests>=2.28.0"
uv add "requests~=2.28.0"
uv add "requests==2.31.0"

# Add from specific source
uv add requests --index-url https://pypi.org/simple
```

### Add Development Dependencies

```bash
# Add dev dependencies
uv add --dev pytest pytest-cov pytest-mock

# Add to specific group
uv add --group test pytest pytest-cov
uv add --group lint ruff mypy
```

### Remove Dependencies

```bash
# Remove dependency
uv remove requests

# Remove dev dependency
uv remove --dev pytest
```

### Update Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package requests

# Update to latest compatible versions
uv sync --upgrade
```

## Installing Dependencies

### Install All Dependencies

```bash
# Install from pyproject.toml
uv sync

# Install only production dependencies
uv sync --no-dev

# Install specific group
uv sync --group test
```

### Install from Requirements File

```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Generate requirements.txt from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt
```

### Install Package in Editable Mode

```bash
# Install current project
uv pip install -e .

# With test dependencies
uv pip install -e ".[test]"

# With multiple extras
uv pip install -e ".[test,dev,docs]"
```

## Running Commands

### Run Python Scripts

```bash
# Run script with uv
uv run python script.py

# Run with arguments
uv run python script.py --arg value

# Run module
uv run python -m module_name
```

### Run Pytest

```bash
# Basic test run
uv run pytest

# With coverage
uv run pytest --cov=src

# Specific test file
uv run pytest tests/test_auth.py

# With custom options
uv run pytest -v --cov=src --cov-report=html
```

### Run Other Tools

```bash
# Run ruff
uv run ruff check .

# Run mypy
uv run mypy src/

# Run black
uv run black .

# Run custom script
uv run python scripts/deploy.py
```

## Virtual Environments

### Create Virtual Environment

```bash
# Create with uv
uv venv

# Custom name
uv venv .venv

# Specific Python version
uv venv --python 3.11
```

### Activate Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

### Using Without Activation

```bash
# uv run uses the venv automatically
uv run python script.py
uv run pytest
```

## Python Version Management

### Install Python Version

```bash
# Install specific version
uv python install 3.11

# Install multiple versions
uv python install 3.10 3.11 3.12
```

### List Python Versions

```bash
# List installed versions
uv python list

# List available versions
uv python list --all
```

### Set Python Version

```bash
# Set for project
uv python pin 3.11

# Creates/updates .python-version file
```

## Lock File

### Generate Lock File

```bash
# Create uv.lock
uv lock

# Update lock file
uv lock --upgrade

# Lock specific package
uv lock --upgrade-package requests
```

### Use Lock File

```bash
# Install from lock file
uv sync

# Install dev dependencies
uv sync --dev
```

## PyPI Index Configuration

### Use Custom Index

```bash
# Add package from custom index
uv add package --index-url https://custom-pypi.org/simple

# Configure in pyproject.toml
```

```toml
[[tool.uv.index]]
name = "custom"
url = "https://custom-pypi.org/simple"
```

### Private Package Repositories

```bash
# With authentication
uv add package --index-url https://user:token@private-pypi.org/simple

# From environment variable
export UV_INDEX_URL=https://private-pypi.org/simple
uv add package
```

## Testing Workflow

### Complete Test Setup

```bash
# 1. Initialize project
uv init my-project
cd my-project

# 2. Add test dependencies
uv add --dev pytest pytest-cov pytest-mock

# 3. Install project
uv pip install -e .

# 4. Run tests
uv run pytest --cov=src --cov-report=html
```

### Test Commands

```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x

# Run specific test
uv run pytest tests/test_auth.py::test_login

# Run with keyword
uv run pytest -k "auth"

# Run with markers
uv run pytest -m "slow"

# Parallel execution (with pytest-xdist)
uv add --dev pytest-xdist
uv run pytest -n auto
```

### Coverage Commands

```bash
# Basic coverage
uv run pytest --cov=src

# With missing lines
uv run pytest --cov=src --cov-report=term-missing

# HTML report
uv run pytest --cov=src --cov-report=html

# Multiple reports
uv run pytest --cov=src --cov-report=term --cov-report=html --cov-report=xml

# Minimum coverage threshold
uv run pytest --cov=src --cov-fail-under=80
```

## pyproject.toml Configuration

### Basic Configuration

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
]
dev = [
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### UV-Specific Configuration

```toml
[tool.uv]
# Development dependencies
dev-dependencies = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]

# Custom PyPI index
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"

# Environment variables
[tool.uv.env]
UV_INDEX_URL = "https://pypi.org/simple"
```

## Common Workflows

### New Project from Scratch

```bash
# 1. Create project
uv init my-project
cd my-project

# 2. Add dependencies
uv add requests pandas

# 3. Add test dependencies
uv add --dev pytest pytest-cov pytest-mock

# 4. Create source structure
mkdir -p src/myproject tests
touch src/myproject/__init__.py

# 5. Install project
uv pip install -e .

# 6. Run tests
uv run pytest
```

### Clone Existing Project

```bash
# 1. Clone repository
git clone https://github.com/user/project.git
cd project

# 2. Install dependencies
uv sync

# 3. Run tests
uv run pytest
```

### Update Dependencies

```bash
# 1. Check outdated packages
uv pip list --outdated

# 2. Update lock file
uv lock --upgrade

# 3. Install updated packages
uv sync

# 4. Run tests
uv run pytest
```

### Add New Dependency

```bash
# 1. Add dependency
uv add new-package

# 2. Update tests if needed
# ... edit tests ...

# 3. Run tests
uv run pytest

# 4. Commit changes
git add pyproject.toml uv.lock
git commit -m "Add new-package dependency"
```

## Comparison with Other Tools

### pip → uv

```bash
# pip
pip install requests
pip install -r requirements.txt
python -m pytest

# uv
uv add requests
uv sync
uv run pytest
```

### poetry → uv

```bash
# poetry
poetry add requests
poetry install
poetry run pytest

# uv
uv add requests
uv sync
uv run pytest
```

### pipenv → uv

```bash
# pipenv
pipenv install requests
pipenv install --dev pytest
pipenv run pytest

# uv
uv add requests
uv add --dev pytest
uv run pytest
```

## Advanced Features

### Build Package

```bash
# Build wheel and sdist
uv build

# Build only wheel
uv build --wheel

# Build only sdist
uv build --sdist
```

### Publish Package

```bash
# Publish to PyPI
uv publish

# Publish to test PyPI
uv publish --index-url https://test.pypi.org/legacy/
```

### Cache Management

```bash
# Show cache directory
uv cache dir

# Clear cache
uv cache clean

# Clear specific package
uv cache clean requests
```

## Environment Variables

### Configuration

```bash
# Set custom index
export UV_INDEX_URL=https://custom-pypi.org/simple

# Set cache directory
export UV_CACHE_DIR=/path/to/cache

# Disable cache
export UV_NO_CACHE=1

# Set Python version
export UV_PYTHON_VERSION=3.11

# Verbose output
export UV_VERBOSE=1
```

## Troubleshooting

### Dependency Conflicts

```bash
# Show dependency tree
uv pip list --tree

# Force reinstall
uv sync --reinstall

# Clear cache and reinstall
uv cache clean && uv sync
```

### Missing Package

```bash
# Verify pyproject.toml
cat pyproject.toml

# Reinstall
uv sync --reinstall

# Check lock file
cat uv.lock
```

### Import Errors

```bash
# Install in editable mode
uv pip install -e .

# Verify package location
uv run python -c "import mypackage; print(mypackage.__file__)"
```

## Best Practices

### 1. Use Lock Files

```bash
# Always commit uv.lock
git add uv.lock
git commit -m "Update dependencies"
```

### 2. Pin Python Version

```bash
# Create .python-version
uv python pin 3.11

# Commit it
git add .python-version
```

### 3. Separate Dependencies

```toml
[project]
dependencies = [  # Production
    "requests",
]

[project.optional-dependencies]
test = [  # Testing
    "pytest",
]
dev = [  # Development
    "ruff",
]
```

### 4. Use Editable Install

```bash
# For development
uv pip install -e ".[test,dev]"
```

### 5. Regular Updates

```bash
# Weekly/monthly
uv lock --upgrade
uv sync
uv run pytest
```

## Quick Reference

| Task | Command |
|------|---------|
| Init project | `uv init` |
| Add package | `uv add package` |
| Add dev package | `uv add --dev package` |
| Install deps | `uv sync` |
| Install project | `uv pip install -e .` |
| Run tests | `uv run pytest` |
| Run with coverage | `uv run pytest --cov=src` |
| Update deps | `uv lock --upgrade` |
| Create venv | `uv venv` |
| Run script | `uv run python script.py` |
| Clean cache | `uv cache clean` |

## Resources

- UV Documentation: https://github.com/astral-sh/uv
- PyPI: https://pypi.org
- Python Packaging: https://packaging.python.org
