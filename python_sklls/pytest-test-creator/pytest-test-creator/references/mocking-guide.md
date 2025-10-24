# Mocking Guide with pytest-mock

Complete guide to mocking in pytest using the pytest-mock plugin.

## Installation

```bash
uv add --dev pytest-mock
```

## Basic Concepts

### What is Mocking?

Mocking replaces real objects with fake ones that:
- Simulate behavior of real objects
- Don't have side effects (no actual API calls, file writes, etc.)
- Allow verification of calls
- Speed up tests

### When to Mock

✅ **Do Mock:**
- External APIs and services
- Database connections
- File system operations
- Network requests
- Time-dependent code
- Random number generation
- Email sending
- Payment processing

❌ **Don't Mock:**
- Simple functions in your code
- Data structures
- Pure functions
- Code you're specifically testing

## Mocker Fixture

The `mocker` fixture is provided by pytest-mock:

```python
def test_example(mocker):
    """mocker is automatically injected by pytest-mock."""
    mock = mocker.patch('module.function')
    # Use the mock
```

## Patching Functions

### Basic Patch

```python
def test_api_call(mocker):
    """Replace real API call with mock."""
    # Patch the function
    mock_get = mocker.patch('requests.get')

    # Configure return value
    mock_get.return_value.json.return_value = {"status": "ok"}

    # Call code that uses requests.get
    result = fetch_weather("Seattle")

    # Verify
    assert result["status"] == "ok"
    mock_get.assert_called_once_with("Seattle")
```

### Patch with Return Value

```python
def test_simple_return(mocker):
    """Patch with simple return value."""
    mocker.patch('module.get_config', return_value={"key": "value"})

    config = load_config()
    assert config["key"] == "value"
```

### Patch Multiple Calls

```python
def test_multiple_returns(mocker):
    """Mock returns different values on each call."""
    mock = mocker.patch('module.random_number')
    mock.side_effect = [1, 2, 3]

    assert generate() == 1
    assert generate() == 2
    assert generate() == 3
```

## Patching Methods

### Patch Object Method

```python
def test_method_patch(mocker):
    """Patch a method on a class."""
    mocker.patch.object(Database, 'connect', return_value=True)

    db = Database()
    result = db.connect()

    assert result is True
```

### Patch Instance Method

```python
def test_instance_method(mocker):
    """Patch method on specific instance."""
    db = Database()
    mocker.patch.object(db, 'query', return_value=[{"id": 1}])

    result = db.query("SELECT * FROM users")
    assert len(result) == 1
```

## Side Effects

### Exception Side Effect

```python
def test_exception_handling(mocker):
    """Test how code handles exceptions."""
    mock = mocker.patch('module.api_call')
    mock.side_effect = ConnectionError("Network error")

    with pytest.raises(ConnectionError):
        call_api()
```

### Function Side Effect

```python
def test_side_effect_function(mocker):
    """Use function as side effect."""
    def custom_behavior(arg):
        return arg * 2

    mock = mocker.patch('module.transform')
    mock.side_effect = custom_behavior

    assert process(5) == 10
```

### Multiple Side Effects

```python
def test_retry_logic(mocker):
    """Test retry with mixed results."""
    mock = mocker.patch('module.unreliable_call')
    mock.side_effect = [
        ConnectionError(),
        ConnectionError(),
        {"data": "success"}
    ]

    result = call_with_retry()
    assert result["data"] == "success"
    assert mock.call_count == 3
```

## Mock Attributes and Properties

### Mock Attributes

```python
def test_mock_attributes(mocker):
    """Mock object with attributes."""
    mock_user = mocker.Mock()
    mock_user.name = "alice"
    mock_user.email = "alice@example.com"
    mock_user.is_active = True

    assert mock_user.name == "alice"
```

### Mock Property

```python
def test_property(mocker):
    """Mock a property."""
    mock_config = mocker.Mock()
    type(mock_config).timeout = mocker.PropertyMock(return_value=30)

    assert mock_config.timeout == 30
```

## Verification

### Assert Called

```python
def test_assert_called(mocker):
    """Verify function was called."""
    mock = mocker.patch('module.send_email')

    notify_user("alice@example.com")

    mock.assert_called()  # Called at least once
    mock.assert_called_once()  # Called exactly once
```

### Assert Called With

```python
def test_assert_called_with(mocker):
    """Verify function was called with specific arguments."""
    mock = mocker.patch('module.log')

    process_data({"id": 1})

    mock.assert_called_with("Processing", id=1)
    mock.assert_called_once_with("Processing", id=1)
```

### Assert Any Call

```python
def test_assert_any_call(mocker):
    """Verify specific call among many."""
    mock = mocker.patch('module.log')

    log("Starting")
    log("Processing")
    log("Done")

    mock.assert_any_call("Processing")
```

### Call Count

```python
def test_call_count(mocker):
    """Check number of calls."""
    mock = mocker.patch('module.validate')

    process_batch([1, 2, 3])

    assert mock.call_count == 3
```

### Check Call Arguments

```python
def test_call_args(mocker):
    """Inspect call arguments."""
    mock = mocker.patch('module.api_call')

    call_api("endpoint", timeout=30)

    # Last call arguments
    args, kwargs = mock.call_args
    assert args[0] == "endpoint"
    assert kwargs["timeout"] == 30

    # All calls
    assert len(mock.call_args_list) == 1
```

## Spy

A spy wraps a real function and tracks calls while allowing the real function to execute.

```python
def test_spy(mocker):
    """Spy on real function."""
    spy = mocker.spy(math, 'sqrt')

    result = calculate_hypotenuse(3, 4)

    assert result == 5
    spy.assert_called_with(25)
```

## Mock Context Managers

### Mock File Operations

```python
def test_file_read(mocker):
    """Mock file reading."""
    mock_open = mocker.mock_open(read_data="line1\nline2\nline3")
    mocker.patch('builtins.open', mock_open)

    content = read_file("data.txt")

    assert "line1" in content
    mock_open.assert_called_once_with("data.txt")
```

### Mock Database Transaction

```python
def test_transaction(mocker):
    """Mock database transaction."""
    mock_transaction = mocker.MagicMock()
    mocker.patch.object(Database, 'transaction', return_value=mock_transaction)

    with Database().transaction() as txn:
        save_user(txn, {"name": "alice"})

    mock_transaction.__enter__.assert_called_once()
    mock_transaction.__exit__.assert_called_once()
```

## Async Mocking

### Mock Async Function

```python
@pytest.mark.asyncio
async def test_async_mock(mocker):
    """Mock async function."""
    mock = mocker.patch('module.async_fetch', new_callable=mocker.AsyncMock)
    mock.return_value = {"data": "value"}

    result = await fetch_data()

    assert result["data"] == "value"
    mock.assert_awaited_once()
```

### Mock Async Context Manager

```python
@pytest.mark.asyncio
async def test_async_context(mocker):
    """Mock async context manager."""
    mock_session = mocker.AsyncMock()
    mocker.patch('aiohttp.ClientSession', return_value=mock_session)

    async with aiohttp.ClientSession() as session:
        await session.get("http://example.com")

    mock_session.__aenter__.assert_awaited_once()
```

## Common Patterns

### Mock Environment Variables

```python
def test_env_vars(mocker):
    """Mock environment variables."""
    mocker.patch.dict('os.environ', {
        'API_KEY': 'test-key',
        'DEBUG': 'true'
    })

    assert os.getenv('API_KEY') == 'test-key'
```

### Mock Time

```python
def test_mock_time(mocker):
    """Mock datetime."""
    fake_now = datetime(2024, 1, 1, 12, 0, 0)
    mocker.patch('datetime.datetime')
    datetime.datetime.now.return_value = fake_now

    result = get_current_time()
    assert result == fake_now
```

### Mock Random

```python
def test_mock_random(mocker):
    """Mock random number generation."""
    mocker.patch('random.randint', return_value=42)

    result = generate_id()
    assert result == 42
```

### Mock Class Constructor

```python
def test_constructor(mocker):
    """Mock class instantiation."""
    mock_instance = mocker.Mock()
    mock_instance.connect.return_value = True

    mocker.patch('module.Database', return_value=mock_instance)

    db = Database()
    assert db.connect() is True
```

### Partial Mocking

```python
def test_partial_mock(mocker):
    """Mock some methods, keep others real."""
    db = Database()

    # Mock only the query method
    mocker.patch.object(db, 'query', return_value=[{"id": 1}])

    # connect() still works normally
    db.connect()

    # query() is mocked
    result = db.query("SELECT * FROM users")
    assert result == [{"id": 1}]
```

## Best Practices

### 1. Patch at the Right Level

❌ **Bad** - Patch where function is defined:
```python
mocker.patch('requests.get')  # If imported with: from requests import get
```

✅ **Good** - Patch where function is used:
```python
mocker.patch('module.get')  # Patch in the module that uses it
```

### 2. Use Specific Assertions

❌ **Bad**:
```python
mock.assert_called()  # Too vague
```

✅ **Good**:
```python
mock.assert_called_once_with(expected_arg, key=expected_value)
```

### 3. Don't Over-Mock

❌ **Bad** - Mocking simple functions:
```python
mocker.patch('module.add', return_value=5)  # Don't mock simple math!
```

✅ **Good** - Mock external dependencies:
```python
mocker.patch('requests.post')  # Mock external API
```

### 4. Reset Mocks Between Tests

Mocks are automatically reset between tests, but be aware of module-scoped fixtures.

### 5. Verify Expected Behavior

Always verify your mocks were called as expected:

```python
def test_with_verification(mocker):
    mock = mocker.patch('module.send_notification')

    process_order(order_id=123)

    # Verify the notification was sent
    mock.assert_called_once_with(
        user_id=456,
        message="Order processed"
    )
```

## Troubleshooting

### Mock Not Working

**Problem**: Mock doesn't affect code
**Solution**: Patch where object is used, not where it's defined

```python
# In module.py:
from requests import get

# In test:
mocker.patch('module.get')  # Not 'requests.get'
```

### Attribute Error

**Problem**: `AttributeError: Mock object has no attribute 'x'`
**Solution**: Configure the mock's return value structure

```python
mock = mocker.Mock()
mock.user.name = "alice"  # Set nested attributes
```

### Async Mock Not Awaited

**Problem**: Mock async function not awaited
**Solution**: Use `AsyncMock`

```python
mock = mocker.patch('module.async_func', new_callable=mocker.AsyncMock)
```

## Examples by Use Case

### Testing API Client

```python
def test_api_client(mocker):
    """Test API client with mocked requests."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"users": []}

    mocker.patch('requests.get', return_value=mock_response)

    client = ApiClient()
    users = client.get_users()

    assert users == []
```

### Testing Database Operations

```python
def test_save_user(mocker):
    """Test saving user to database."""
    mock_db = mocker.Mock()
    mock_db.insert.return_value = 123

    service = UserService(mock_db)
    user_id = service.create_user("alice")

    assert user_id == 123
    mock_db.insert.assert_called_once()
```

### Testing Email Sending

```python
def test_send_welcome_email(mocker):
    """Test welcome email is sent."""
    mock_send = mocker.patch('module.send_email')

    register_user("alice@example.com")

    mock_send.assert_called_once()
    args = mock_send.call_args[1]
    assert args['to'] == "alice@example.com"
    assert "Welcome" in args['subject']
```

## Summary

- Use `mocker` fixture for all mocking needs
- Patch at the import location, not definition
- Verify calls with `assert_called_*` methods
- Use side effects for exceptions and dynamic behavior
- Spy for tracking calls to real functions
- Use `AsyncMock` for async code
- Keep mocks simple and focused
