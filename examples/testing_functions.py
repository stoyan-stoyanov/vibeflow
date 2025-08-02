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
