"""Global cache implementation for YOLO function decorator."""

from typing import Any, Dict, Tuple
import time
import os
import json
import sys
from pathlib import Path


class YoloCache:
    """A simple in-memory cache for YOLO functions with TTL support and persistence.

    This is a global cache that's shared across all @yolo decorated functions.
    It provides a dictionary-like interface with automatic expiration of entries
    and persists the cache to disk.
    """

    def __init__(self, cache_dir: Path = None):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self.max_size = 1000  # Fixed max size
        self.ttl = None  # No TTL by default

        if cache_dir is None:
            # Default to the directory of the executed script
            main_script_path = os.path.abspath(sys.argv[0])
            cache_dir = Path(os.path.dirname(main_script_path))
        self.cache_file = cache_dir / "yolo.cache.json"

        self._load_from_disk()

    def _load_from_disk(self):
        """Load the cache from a JSON file if it exists."""
        if not self.cache_file.exists():
            return

        try:
            with open(self.cache_file, "r") as f:
                self._cache = json.load(f)
        except (IOError, json.JSONDecodeError):
            # If file is corrupted or unreadable, start with an empty cache
            self._cache = {}

    def _save_to_disk(self):
        """Save the current cache state to a JSON file."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w") as f:
                json.dump(self._cache, f)
        except IOError:
            # Handle cases where the file cannot be written
            pass

    def __getitem__(self, key: str) -> Any:
        """Get an item from the cache."""
        if key not in self._cache:
            raise KeyError(key)

        value, timestamp = self._cache[key]

        # Check if the entry has expired
        if self.ttl is not None and (time.time() - timestamp) > self.ttl:
            del self._cache[key]
            self._save_to_disk()  # Persist the removal
            raise KeyError(f"Key '{key}' has expired")

        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Store a value in the cache."""
        # Remove oldest item if we're at max size
        if len(self._cache) >= self.max_size:
            self._cache.pop(next(iter(self._cache)), None)

        self._cache[key] = (value, time.time())
        self._save_to_disk()  # Persist the new state

    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from the cache with a default if not found."""
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()
        self._save_to_disk()  # Persist the cleared state

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
