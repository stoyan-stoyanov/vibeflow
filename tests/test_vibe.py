"""Tests for the VIBE package."""
import unittest
import os
from vibeflow import vibe, clear_cache, get_cache_stats

# Define a dummy cache file path for cleanup
TEST_CACHE_FILE = os.path.join(os.path.dirname(__file__), "vibe.cache.json")

class TestVIBESync(unittest.TestCase):
    def setUp(self):
        """Clear caches before each test."""
        clear_cache()
        if os.path.exists(TEST_CACHE_FILE):
            os.remove(TEST_CACHE_FILE)

    def tearDown(self):
        """Clean up cache files after tests."""
        clear_cache()
        if os.path.exists(TEST_CACHE_FILE):
            os.remove(TEST_CACHE_FILE)

    def test_sync_function_and_caching(self):
        """Tests a basic synchronous function and verifies caching."""
        @vibe
        def add(a: int, b: int) -> int:
            """Adds two integers together."""
            pass

        # First call, should generate and cache
        result1 = add(5, 10)
        self.assertEqual(result1, 15)
        stats1 = get_cache_stats()
        self.assertEqual(stats1["in_memory_cache_size"], 1)
        self.assertEqual(stats1["disk_cache_items"], 1)

        # Second call, should use in-memory cache
        result2 = add(5, 10)
        self.assertEqual(result2, 15)
        stats2 = get_cache_stats()
        self.assertEqual(stats2["in_memory_cache_size"], 1)

    def test_clear_cache_sync(self):
        """Tests that the cache is cleared properly for sync functions."""
        @vibe
        def subtract(a: int, b: int) -> int:
            """Subtracts b from a."""
            pass

        subtract(10, 3)
        stats_before = get_cache_stats()
        self.assertEqual(stats_before["in_memory_cache_size"], 1)

        clear_cache()
        stats_after = get_cache_stats()
        self.assertEqual(stats_after["in_memory_cache_size"], 0)
        self.assertEqual(stats_after["disk_cache_items"], 0)


class TestVIBEAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Clear caches before each test."""
        clear_cache()
        if os.path.exists(TEST_CACHE_FILE):
            os.remove(TEST_CACHE_FILE)

    def tearDown(self):
        """Clean up cache files after tests."""
        clear_cache()
        if os.path.exists(TEST_CACHE_FILE):
            os.remove(TEST_CACHE_FILE)

    async def test_async_function_and_caching(self):
        """Tests a basic asynchronous function and verifies caching."""
        @vibe
        async def multiply(a: int, b: int) -> int:
            """Multiplies two integers."""
            pass

        # First call, should generate and cache
        result1 = await multiply(4, 5)
        self.assertEqual(result1, 20)
        stats1 = get_cache_stats()
        self.assertEqual(stats1["in_memory_cache_size"], 1)
        self.assertEqual(stats1["disk_cache_items"], 1)

        # Second call, should use in-memory cache
        result2 = await multiply(4, 5)
        self.assertEqual(result2, 20)
        stats2 = get_cache_stats()
        self.assertEqual(stats2["in_memory_cache_size"], 1)


if __name__ == '__main__':
    unittest.main()
