"""Global cache implementation for YOLO function decorator."""

from typing import Any, Dict, Tuple
import time


class YoloCache:
    """A simple in-memory cache for YOLO functions with TTL support.

    This is a global cache that's shared across all @yolo decorated functions.
    It provides a dictionary-like interface with automatic expiration of entries.
    """

    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self.max_size = 1000  # Fixed max size
        self.ttl = None  # No TTL by default

    def __getitem__(self, key: str) -> Any:
        """Get an item from the cache."""
        if key not in self._cache:
            raise KeyError(key)

        value, timestamp = self._cache[key]

        # Check if the entry has expired
        if self.ttl is not None and (time.time() - timestamp) > self.ttl:
            del self._cache[key]
            raise KeyError(f"Key '{key}' has expired")

        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Store a value in the cache."""
        # Remove oldest item if we're at max size
        if len(self._cache) >= self.max_size:
            self._cache.pop(next(iter(self._cache)), None)

        self._cache[key] = (value, time.time())

    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from the cache with a default if not found."""
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()

    def __len__(self) -> int:
        """Get the current number of items in the cache."""
        return len(self._cache)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the cache and is not expired."""
        try:
            _ = self[key]
            return True
        except KeyError:
            return False


# Global cache instance used by all @yolo decorated functions
cache = YoloCache()
