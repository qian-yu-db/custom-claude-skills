# Testing Databricks Python Notebooks

Guide for creating tests for Databricks notebooks (.py format) that work with both local IDE and Databricks workspace environments.

## Databricks Notebook Structure

Databricks `.py` notebooks have special structure:

```python
# Databricks notebook source

# MAGIC %md
# MAGIC # Notebook Title

# COMMAND ----------

# Python code in cells
from pyspark.sql import SparkSession

# COMMAND ----------

def process_data(df):
    """Process dataframe."""
    return df.filter(df.value > 0)

# COMMAND ----------

# More code
```

## Challenges for Testing

### 1. Cell Separators
- `# COMMAND ----------` markers break standard Python parsing
- Can't directly import notebook code into tests

### 2. Databricks-Specific Objects
- `spark` - SparkSession (available in workspace)
- `dbutils` - Databricks utilities
- `display()` - Display function

### 3. Environment Detection
- Notebooks check if running in Databricks vs local IDE
- Different setup code for each environment

### 4. Mixed Content
- Markdown cells (`# MAGIC %md`)
- Magic commands
- Not standard Python code

## Testing Strategies

### Strategy 1: Extract Testable Functions (Recommended)

**Extract business logic into separate Python modules:**

#### Project Structure
```
project/
├── src/
│   └── etl/
│       ├── __init__.py
│       ├── transformations.py    # Testable functions
│       └── utils.py               # Helper functions
├── notebooks/
│   └── etl_pipeline.py           # Databricks notebook
└── tests/
    └── etl/
        ├── test_transformations.py
        └── test_utils.py
```

#### transformations.py (Testable Module)
```python
"""ETL transformation functions."""
from pyspark.sql import DataFrame
import pyspark.sql.functions as F

def filter_active_users(df: DataFrame) -> DataFrame:
    """Filter for active users only."""
    return df.filter(F.col("is_active") == True)

def enrich_with_metadata(df: DataFrame, metadata_df: DataFrame) -> DataFrame:
    """Enrich data with metadata."""
    return df.join(metadata_df, on="user_id", how="left")

def calculate_metrics(df: DataFrame) -> DataFrame:
    """Calculate user metrics."""
    return df.groupBy("user_id").agg(
        F.count("*").alias("event_count"),
        F.sum("value").alias("total_value"),
        F.avg("value").alias("avg_value")
    )
```

#### Notebook (etl_pipeline.py)
```python
# Databricks notebook source

# MAGIC %md
# MAGIC # ETL Pipeline

# COMMAND ----------

from src.etl.transformations import (
    filter_active_users,
    enrich_with_metadata,
    calculate_metrics
)

# COMMAND ----------

# Environment setup
from src.utils.dev_utils import is_running_in_databricks

if not is_running_in_databricks():
    from databricks.connect import DatabricksSession
    spark = DatabricksSession.builder.profile("my_profile").getOrCreate()

# COMMAND ----------

# Load data
users_df = spark.table("catalog.schema.users")
metadata_df = spark.table("catalog.schema.user_metadata")

# COMMAND ----------

# Apply transformations (testable functions)
active_users = filter_active_users(users_df)
enriched = enrich_with_metadata(active_users, metadata_df)
metrics = calculate_metrics(enriched)

# COMMAND ----------

# Save results
metrics.write.mode("overwrite").saveAsTable("catalog.schema.user_metrics")
```

#### test_transformations.py
```python
"""Tests for ETL transformations."""
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, IntegerType
from src.etl.transformations import (
    filter_active_users,
    enrich_with_metadata,
    calculate_metrics
)

@pytest.fixture(scope="session")
def spark():
    """Provide Spark session for tests."""
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

@pytest.fixture
def sample_users(spark):
    """Provide sample user data."""
    schema = StructType([
        StructField("user_id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("is_active", BooleanType(), True),
    ])
    data = [
        (1, "Alice", True),
        (2, "Bob", False),
        (3, "Charlie", True),
    ]
    return spark.createDataFrame(data, schema)

def test_filter_active_users(sample_users):
    """Test filtering for active users only."""
    result = filter_active_users(sample_users)

    assert result.count() == 2
    assert set(result.select("name").rdd.flatMap(lambda x: x).collect()) == {"Alice", "Charlie"}

def test_filter_active_users_empty(spark):
    """Test with no active users."""
    schema = StructType([
        StructField("user_id", IntegerType(), False),
        StructField("is_active", BooleanType(), True),
    ])
    df = spark.createDataFrame([(1, False), (2, False)], schema)

    result = filter_active_users(df)
    assert result.count() == 0

@pytest.fixture
def sample_metadata(spark):
    """Provide sample metadata."""
    schema = StructType([
        StructField("user_id", IntegerType(), False),
        StructField("region", StringType(), True),
    ])
    data = [(1, "US"), (2, "EU"), (3, "APAC")]
    return spark.createDataFrame(data, schema)

def test_enrich_with_metadata(sample_users, sample_metadata):
    """Test metadata enrichment."""
    result = enrich_with_metadata(sample_users, sample_metadata)

    assert result.count() == 3
    assert "region" in result.columns

    alice = result.filter(result.name == "Alice").first()
    assert alice.region == "US"
```

### Strategy 2: Test Notebook Cells Directly

**For notebooks with minimal business logic:**

#### parse_notebook.py (Helper)
```python
"""Parse Databricks notebook cells."""
import re
from typing import List, Dict

def extract_code_cells(notebook_path: str) -> List[str]:
    """Extract code cells from Databricks notebook."""
    with open(notebook_path, 'r') as f:
        content = f.read()

    # Split by cell separator
    cells = re.split(r'# COMMAND ----------', content)

    # Filter out markdown cells and empty cells
    code_cells = []
    for cell in cells:
        # Skip header
        if '# Databricks notebook source' in cell:
            continue
        # Skip markdown cells
        if '# MAGIC %md' in cell or '# MAGIC' in cell:
            continue
        # Skip empty cells
        cell = cell.strip()
        if cell:
            code_cells.append(cell)

    return code_cells

def extract_functions(notebook_path: str) -> Dict[str, str]:
    """Extract function definitions from notebook."""
    code_cells = extract_code_cells(notebook_path)
    full_code = '\n'.join(code_cells)

    # Parse and extract functions
    functions = {}
    current_func = None
    func_lines = []

    for line in full_code.split('\n'):
        if line.strip().startswith('def '):
            if current_func:
                functions[current_func] = '\n'.join(func_lines)
            current_func = line.split('(')[0].replace('def ', '').strip()
            func_lines = [line]
        elif current_func:
            if line and not line[0].isspace() and not line.strip().startswith('#'):
                # Function ended
                functions[current_func] = '\n'.join(func_lines)
                current_func = None
                func_lines = []
            else:
                func_lines.append(line)

    if current_func:
        functions[current_func] = '\n'.join(func_lines)

    return functions
```

#### test_notebook_functions.py
```python
"""Test functions extracted from notebook."""
import pytest
from tests.helpers.parse_notebook import extract_functions

@pytest.fixture(scope="module")
def notebook_functions():
    """Extract functions from notebook."""
    return extract_functions("notebooks/etl_pipeline.py")

def test_transform_function_exists(notebook_functions):
    """Test that transform function is defined."""
    assert "transform_data" in notebook_functions

def test_transform_function_signature(notebook_functions):
    """Test transform function signature."""
    func_code = notebook_functions["transform_data"]
    assert "def transform_data(df)" in func_code
```

### Strategy 3: Integration Testing with Databricks

**Test entire notebook execution:**

#### test_notebook_execution.py
```python
"""Integration tests for notebook execution."""
import pytest
import subprocess
import json

@pytest.fixture
def databricks_token():
    """Get Databricks token from environment."""
    import os
    return os.getenv("DATABRICKS_TOKEN")

@pytest.mark.integration
def test_notebook_runs_successfully(databricks_token):
    """Test that notebook executes without errors."""
    # Using Databricks CLI to run notebook
    cmd = [
        "databricks", "runs", "submit",
        "--json",
        json.dumps({
            "run_name": "Test ETL Pipeline",
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "i3.xlarge",
                "num_workers": 2
            },
            "notebook_task": {
                "notebook_path": "/Workspace/notebooks/etl_pipeline",
                "base_parameters": {"env": "test"}
            }
        })
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    # Parse run ID and check status
    run_info = json.loads(result.stdout)
    run_id = run_info["run_id"]

    # Wait for completion and verify
    # (implementation depends on your setup)
```

## Mock Databricks Objects

### Mock Spark Session

```python
"""Fixtures for mocking Databricks objects."""
import pytest
from unittest.mock import Mock, MagicMock

@pytest.fixture
def mock_spark():
    """Mock Spark session."""
    spark = Mock()

    # Mock table method
    spark.table = Mock()

    # Mock createDataFrame
    spark.createDataFrame = Mock()

    # Mock SQL
    spark.sql = Mock()

    return spark

@pytest.fixture
def mock_dbutils():
    """Mock dbutils."""
    dbutils = Mock()

    # Mock widgets
    dbutils.widgets.get = Mock(return_value="test_value")

    # Mock secrets
    dbutils.secrets.get = Mock(return_value="test_secret")

    # Mock fs
    dbutils.fs.ls = Mock(return_value=[])

    return dbutils

def test_with_mocked_databricks(mock_spark, mock_dbutils):
    """Test code that uses Databricks objects."""
    # Your test code using mocked objects
    df = mock_spark.table("catalog.schema.table")
    assert mock_spark.table.called
```

### Mock with pytest-mock

```python
def test_notebook_logic(mocker):
    """Test notebook logic with mocked Databricks."""
    # Mock spark session
    mock_spark = mocker.Mock()
    mock_df = mocker.Mock()
    mock_spark.table.return_value = mock_df

    # Patch in the notebook's namespace
    mocker.patch('notebook_module.spark', mock_spark)

    # Test your logic
    from notebook_module import process_pipeline
    result = process_pipeline()

    mock_spark.table.assert_called_once()
```

## PySpark Testing Best Practices

### 1. Use Local Spark for Tests

```python
@pytest.fixture(scope="session")
def spark():
    """Create local Spark session for testing."""
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .appName("pytest") \
        .master("local[2]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.default.parallelism", "2") \
        .getOrCreate()

    yield spark

    spark.stop()
```

### 2. Create Sample DataFrames

```python
@pytest.fixture
def sample_data(spark):
    """Create sample DataFrame for testing."""
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("value", IntegerType(), True),
    ])

    data = [
        (1, "Alice", 100),
        (2, "Bob", 200),
        (3, "Charlie", 150),
    ]

    return spark.createDataFrame(data, schema)
```

### 3. Assert DataFrame Contents

```python
def test_transformation(sample_data):
    """Test DataFrame transformation."""
    result = transform_function(sample_data)

    # Assert row count
    assert result.count() == 3

    # Assert column exists
    assert "new_column" in result.columns

    # Assert specific values
    first_row = result.first()
    assert first_row.name == "Alice"

    # Convert to list for detailed assertions
    rows = result.collect()
    assert len(rows) == 3

    # Assert using pandas for easier comparison
    result_pdf = result.toPandas()
    assert result_pdf["value"].sum() == 450
```

### 4. Test Schema Validation

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def test_output_schema():
    """Test that transformation produces correct schema."""
    expected_schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("processed_name", StringType(), True),
        StructField("doubled_value", IntegerType(), True),
    ])

    result = transform_function(sample_data)

    assert result.schema == expected_schema
```

## Configuration for pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "unit: Unit tests (fast, no external dependencies)",
    "integration: Integration tests (require Databricks)",
    "slow: Slow tests (PySpark operations)",
]
addopts = [
    "-v",
    "-m not integration",  # Skip integration tests by default
]

[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "pyspark>=3.5.0",  # For local testing
]
databricks = [
    "databricks-connect>=13.0.0",
    "databricks-cli>=0.18.0",
]
```

## Running Tests

### Local Unit Tests (Fast)
```bash
# Test extracted functions with local Spark
uv run pytest tests/ -m unit

# With coverage
uv run pytest tests/ -m unit --cov=src
```

### Integration Tests (Databricks)
```bash
# Run integration tests (requires Databricks connection)
uv run pytest tests/ -m integration

# Run all tests including slow PySpark tests
uv run pytest tests/
```

## Best Practices Summary

1. **Extract Logic**: Move business logic to testable Python modules
2. **Use Local Spark**: Test PySpark code with local Spark session
3. **Mock Databricks Objects**: Mock `spark`, `dbutils` for unit tests
4. **Separate Concerns**: Keep notebook as orchestration, logic in modules
5. **Mark Tests**: Use markers (`unit`, `integration`, `slow`)
6. **Small Test Data**: Use small DataFrames for fast tests
7. **Test Schema**: Verify output schemas match expectations
8. **Integration Tests**: Test full notebook execution in CI/CD

## Example Project Structure

```
databricks-project/
├── src/
│   ├── etl/
│   │   ├── __init__.py
│   │   ├── transformations.py    # Pure functions
│   │   ├── validators.py         # Data validation
│   │   └── utils.py               # Helpers
│   └── utils/
│       └── dev_utils.py           # Environment detection
├── notebooks/
│   ├── bronze_to_silver.py       # Databricks notebook
│   └── silver_to_gold.py         # Databricks notebook
├── tests/
│   ├── etl/
│   │   ├── test_transformations.py
│   │   ├── test_validators.py
│   │   └── test_utils.py
│   ├── integration/
│   │   └── test_notebooks.py
│   └── conftest.py                # Shared fixtures
├── pyproject.toml
└── README.md
```

This approach gives you:
- ✅ Fast unit tests with local Spark
- ✅ Integration tests for full notebook execution
- ✅ Good code organization
- ✅ Easy to maintain and debug
- ✅ Works with standard pytest tooling
