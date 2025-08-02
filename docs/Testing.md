# Testing Vibe-Generated Functions

`vibeflow` introduces a powerful new approach to software development: **Test-Driven Generation (TDG)**. Instead of writing tests for code you've already implemented, you write tests for function stubs, and `vibeflow` generates the code for you. This workflow not only validates the AI-generated code but also pre-compiles and caches it, ensuring that only tested, working functions are used in your application.

## The `@vibe_test` Decorator

The key to this workflow is the `@vibe_test` decorator. When you apply this decorator to a test function, it enables a special "safe-caching" mode:

- **On Test Success**: If your test passes, the `@vibe`-decorated function that was generated during the test is saved to the `vibe.cache.json` file.
- **On Test Failure**: If your test fails for any reason (e.g., an `AssertionError`), `@vibe_test` intercepts the failure, **deletes the newly generated function from the cache**, and then reports the test as failed.

This ensures that your cache is never polluted with faulty or unexpected code.

## Example: Test-Driven Generation

Let's walk through an example of how to use this feature.

### 1. Define Your Function Stub

First, create a file with your `@vibe`-decorated function stub. For this example, we'll use a simple `add` function.

**`helpers.py`**:
```python
from vibeflow import vibe

@vibe
def add(a: int, b: int) -> int:
    """Adds two integers and returns their sum."""
    pass
```

### 2. Write Your Tests

Next, create a test file using `pytest`. Import your function and the `@vibe_test` decorator. Write tests to validate the behavior of the generated function.

**`tests/test_add.py`**:
```python
import pytest
from vibeflow import vibe_test
from helpers import add

@vibe_test
def test_add_function_caching():
    """
    Tests the successful generation and caching of the 'add' function.
    When this test passes, the generated function will be saved to the cache.
    """
    assert add(2, 2) == 4
    assert add(-1, 1) == 0

@vibe_test
def test_failing_add_function_is_not_cached():
    """
    Tests that a failing function is not cached.
    This test is designed to fail to demonstrate that the faulty
    function implementation is deleted from the cache.
    """
    with pytest.raises(AssertionError):
        # This assertion is intentionally incorrect to trigger a test failure.
        # The @vibe_test decorator will catch the failure and ensure
        # the generated 'add' function is not saved to the cache.
        assert add(5, 5) == 999  # This will fail
```

### 3. Run Your Tests

Now, run `pytest` from your terminal:

```bash
pytest
```

You will see one test pass and one test fail. The passing test generates and caches the `add` function, while the failing test demonstrates that `@vibe_test` catches the failure and removes the function from the cache.

After running the tests, your `vibe.cache.json` file will be clean, containing no trace of the faulty function, but it will be ready for future successful runs.