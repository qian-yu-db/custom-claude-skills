# Comprehensive Pytest Patterns

This reference provides detailed pytest patterns for various testing scenarios.

## Table of Contents

1. [Basic Test Patterns](#basic-test-patterns)
2. [Fixtures](#fixtures)
3. [Parametrization](#parametrization)
4. [Mocking](#mocking)
5. [Exception Testing](#exception-testing)
6. [Async Testing](#async-testing)
7. [Class-Based Tests](#class-based-tests)
8. [Integration Testing](#integration-testing)

## Basic Test Patterns

### Simple Assertion
```python
def test_addition():
    """Test basic addition."""
    assert 1 + 1 == 2
```

### Multiple Assertions
```python
def test_user_creation():
    """Test user object creation."""
    user = User("alice", "alice@example.com")
    assert user.name == "alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True
```

### Assertion with Message
```python
def test_calculation():
    """Test calculation with custom message."""
    result = calculate(10, 5)
    assert result == 15, f"Expected 15, got {result}"
```

### Approximate Comparisons
```python
def test_float_comparison():
    """Test floating point numbers."""
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)

def test_float_with_tolerance():
    """Test with custom tolerance."""
    assert 1.001 == pytest.approx(1.0, abs=0.01)
```

## Fixtures

### Basic Fixture
```python
@pytest.fixture
def sample_user():
    """Provide a sample user for tests."""
    return User("alice", "alice@example.com")

def test_user_name(sample_user):
    """Test user name."""
    assert sample_user.name == "alice"
```

### Fixture with Setup and Teardown
```python
@pytest.fixture
def database():
    """Provide database connection."""
    db = Database()
    db.connect()
    yield db  # Test runs here
    db.disconnect()

def test_query(database):
    """Test database query."""
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Fixture Scope
```python
# Function scope (default) - runs for each test
@pytest.fixture
def function_fixture():
    return "new for each test"

# Class scope - runs once per test class
@pytest.fixture(scope="class")
def class_fixture():
    return "shared across class"

# Module scope - runs once per module
@pytest.fixture(scope="module")
def module_fixture():
    return "shared across module"

# Session scope - runs once per session
@pytest.fixture(scope="session")
def session_fixture():
    return "shared across session"
```

### Fixture Dependencies
```python
@pytest.fixture
def database():
    """Database connection."""
    return Database()

@pytest.fixture
def user_repository(database):
    """User repository with database dependency."""
    return UserRepository(database)

def test_find_user(user_repository):
    """Test finding a user."""
    user = user_repository.find("alice")
    assert user is not None
```

### Parametrized Fixtures
```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Provide different database types."""
    return Database(request.param)

def test_connection(database):
    """Test will run 3 times with different databases."""
    assert database.connect()
```

### Autouse Fixtures
```python
@pytest.fixture(autouse=True)
def reset_state():
    """Automatically reset state before each test."""
    State.reset()
    yield
    # Cleanup after test
```

## Parametrization

### Basic Parametrization
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    """Test doubling numbers."""
    assert double(input) == expected
```

### Multiple Parameters
```python
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (0, 10, 10),
])
def test_addition(x, y, expected):
    """Test addition with multiple inputs."""
    assert add(x, y) == expected
```

### Parametrize with IDs
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (5, 10),
    (0, 0),
], ids=["one", "five", "zero"])
def test_multiply(input, expected):
    """Test with custom test IDs."""
    assert multiply(input, 2) == expected
```

### Nested Parametrization
```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_combinations(x, y):
    """Test all combinations (6 tests total)."""
    assert x + y > 0
```

### Parametrize with Complex Objects
```python
@pytest.mark.parametrize("user_data", [
    {"name": "alice", "age": 30},
    {"name": "bob", "age": 25},
])
def test_user_creation(user_data):
    """Test user creation with different data."""
    user = User(**user_data)
    assert user.name == user_data["name"]
```

## Mocking

### Basic Mock
```python
def test_api_call(mocker):
    """Test function that calls external API."""
    mock = mocker.patch('module.api_client.get')
    mock.return_value = {"status": "ok"}

    result = fetch_data()
    assert result["status"] == "ok"
    mock.assert_called_once()
```

### Mock with Side Effects
```python
def test_retry_logic(mocker):
    """Test retry on failure."""
    mock = mocker.patch('module.api_call')
    mock.side_effect = [
        Exception("Network error"),
        Exception("Timeout"),
        {"status": "ok"}
    ]

    result = api_with_retry()
    assert result["status"] == "ok"
    assert mock.call_count == 3
```

### Mock Attributes
```python
def test_config(mocker):
    """Test with mocked configuration."""
    mock_config = mocker.Mock()
    mock_config.api_key = "test-key"
    mock_config.timeout = 30

    mocker.patch('module.get_config', return_value=mock_config)

    client = ApiClient()
    assert client.api_key == "test-key"
```

### Spy (Partial Mock)
```python
def test_with_spy(mocker):
    """Test with spy to track real function calls."""
    spy = mocker.spy(module, 'process_data')

    result = workflow()

    spy.assert_called_once_with(expected_data)
    assert result is not None
```

### Mock Class Methods
```python
def test_class_method(mocker):
    """Test mocking class method."""
    mocker.patch.object(Database, 'connect', return_value=True)

    db = Database()
    assert db.connect()
```

### Mock Context Manager
```python
def test_file_operations(mocker):
    """Test with mocked file operations."""
    mock_file = mocker.mock_open(read_data="file content")
    mocker.patch('builtins.open', mock_file)

    result = read_config("config.txt")
    assert result == "file content"
```

## Exception Testing

### Basic Exception
```python
def test_raises_value_error():
    """Test that function raises ValueError."""
    with pytest.raises(ValueError):
        invalid_function()
```

### Exception with Message Match
```python
def test_error_message():
    """Test exception message."""
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input("bad")
```

### Capture Exception for Inspection
```python
def test_exception_details():
    """Test and inspect exception."""
    with pytest.raises(CustomError) as exc_info:
        risky_operation()

    assert exc_info.value.code == 400
    assert "error" in str(exc_info.value)
```

### Test No Exception
```python
def test_no_exception():
    """Test that function doesn't raise."""
    try:
        safe_function()
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
```

## Async Testing

### Basic Async Test
```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_fetch_data()
    assert result is not None
```

### Async Fixture
```python
@pytest.fixture
async def async_database():
    """Async database fixture."""
    db = AsyncDatabase()
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_async_query(async_database):
    """Test async database query."""
    result = await async_database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Mock Async Function
```python
@pytest.mark.asyncio
async def test_async_with_mock(mocker):
    """Test async function with mock."""
    mock = mocker.patch('module.async_api_call',
                        new_callable=mocker.AsyncMock)
    mock.return_value = {"data": "value"}

    result = await fetch_async()
    assert result["data"] == "value"
```

## Class-Based Tests

### Basic Test Class
```python
class TestCalculator:
    """Test suite for Calculator."""

    def test_add(self):
        """Test addition."""
        calc = Calculator()
        assert calc.add(1, 2) == 3

    def test_subtract(self):
        """Test subtraction."""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
```

### Class with Fixture
```python
class TestUserService:
    """Test suite for UserService."""

    @pytest.fixture
    def service(self):
        """Provide UserService instance."""
        return UserService()

    def test_create_user(self, service):
        """Test user creation."""
        user = service.create("alice")
        assert user.name == "alice"

    def test_find_user(self, service):
        """Test finding user."""
        service.create("alice")
        user = service.find("alice")
        assert user is not None
```

### Class Setup/Teardown
```python
class TestDatabase:
    """Test suite with setup/teardown."""

    @classmethod
    def setup_class(cls):
        """Run once before all tests in class."""
        cls.db = Database()
        cls.db.connect()

    @classmethod
    def teardown_class(cls):
        """Run once after all tests in class."""
        cls.db.disconnect()

    def setup_method(self):
        """Run before each test method."""
        self.db.clear()

    def test_insert(self):
        """Test insertion."""
        self.db.insert({"name": "alice"})
        assert len(self.db.all()) == 1
```

## Integration Testing

### API Integration Test
```python
@pytest.fixture
def api_client():
    """Provide API client."""
    return TestClient(app)

def test_user_endpoint(api_client):
    """Test user API endpoint."""
    response = api_client.post("/users", json={"name": "alice"})
    assert response.status_code == 201
    assert response.json()["name"] == "alice"

    response = api_client.get("/users/alice")
    assert response.status_code == 200
```

### Database Integration Test
```python
@pytest.fixture(scope="module")
def test_database():
    """Provide test database."""
    db = Database("test.db")
    db.create_tables()
    yield db
    db.drop_tables()

def test_user_crud(test_database):
    """Test user CRUD operations."""
    # Create
    user_id = test_database.users.create({"name": "alice"})

    # Read
    user = test_database.users.get(user_id)
    assert user["name"] == "alice"

    # Update
    test_database.users.update(user_id, {"name": "alice2"})
    assert test_database.users.get(user_id)["name"] == "alice2"

    # Delete
    test_database.users.delete(user_id)
    assert test_database.users.get(user_id) is None
```

### Multi-Component Integration
```python
@pytest.fixture
def app_stack():
    """Provide full application stack."""
    database = Database()
    cache = Cache()
    service = UserService(database, cache)
    api = API(service)

    yield {
        "database": database,
        "cache": cache,
        "service": service,
        "api": api,
    }

    database.cleanup()
    cache.clear()

def test_user_workflow(app_stack):
    """Test complete user workflow."""
    api = app_stack["api"]
    cache = app_stack["cache"]

    # Create user via API
    response = api.create_user({"name": "alice"})
    user_id = response["id"]

    # Verify cached
    assert cache.has(f"user:{user_id}")

    # Fetch user
    user = api.get_user(user_id)
    assert user["name"] == "alice"
```

## Best Practices Summary

1. **One assertion per test** (when possible)
2. **Use descriptive test names**
3. **Keep tests independent**
4. **Use fixtures for common setup**
5. **Parametrize instead of loops**
6. **Mock external dependencies**
7. **Test edge cases and errors**
8. **Keep tests fast**
9. **Write readable tests**
10. **Document test intent**
