"""Tests for the YOLO package."""
import unittest
import time
from yololang import yolo, YoloCache, clear_cache, get_cache_stats

class TestYOLO(unittest.TestCase):
    def setUp(self):
        # Clear the cache before each test
        clear_cache()

    def test_basic_function(self):
        @yolo
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            pass
            
        result = add(2, 3)
        self.assertEqual(result, 5)
        
        # Should use cached version
        result2 = add(2, 3)
        self.assertEqual(result2, 5)
        
        # Check cache stats
        stats = get_cache_stats()
        self.assertEqual(stats['size'], 1)

    def test_cache_ttl(self):
        # Create a cache with 1-second TTL
        cache = YoloCache(ttl=1)
        
        @yolo(cache=cache)
        def greet(name: str) -> str:
            """Return a greeting."""
            pass
            
        # First call - should be cached
        result1 = greet("Alice")
        self.assertIn("Alice", result1)
        
        # Should still be cached
        result2 = greet("Alice")
        self.assertEqual(result1, result2)
        
        # Wait for cache to expire
        time.sleep(1.1)
        
        # Should generate a new version
        result3 = greet("Alice")
        self.assertIn("Alice", result3)
        # The exact text might be different, but it should still contain the name

    def test_clear_cache(self):
        @yolo
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            pass
            
        # Call to populate cache
        multiply(3, 4)
        
        # Clear cache
        clear_cache()
        
        # Cache should be empty
        stats = get_cache_stats()
        self.assertEqual(stats['size'], 0)

if __name__ == '__main__':
    unittest.main()
