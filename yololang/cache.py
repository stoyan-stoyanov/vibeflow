"""Global cache implementation for YOLO function decorator."""

from typing import Any, Dict
import json
import os


class YoloCache:
    """
    A cache that stores generated code on disk, organized by the file path
    of the function being decorated. This ensures that cache files are always
    co-located with the scripts that use them.
    """

    def __init__(self):
        self._caches = {}

    def _get_cache_file_path(self, func_file_path):
        """Determines the correct path for the yolo.cache.json file."""
        directory = os.path.dirname(os.path.abspath(func_file_path))
        return os.path.join(directory, "yolo.cache.json")

    def _load_cache_if_needed(self, cache_file):
        """Loads a specific cache file from disk if it's not already in memory."""
        if cache_file not in self._caches:
            try:
                with open(cache_file, "r") as f:
                    self._caches[cache_file] = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self._caches[cache_file] = {}

    def get(self, key: str, func_file_path: str):
        """Gets a value from the cache for a given function file."""
        cache_file = self._get_cache_file_path(func_file_path)
        self._load_cache_if_needed(cache_file)
        return self._caches[cache_file].get(key)

    def delete(self, key: str, func_file_path: str):
        """Deletes a key from the cache and saves the change to disk."""
        cache_file = self._get_cache_file_path(func_file_path)
        self._load_cache_if_needed(cache_file)
        if key in self._caches[cache_file]:
            del self._caches[cache_file][key]
            with open(cache_file, "w") as f:
                json.dump(self._caches[cache_file], f, indent=4)

    def set(self, key: str, value: str, func_file_path: str):
        """Sets a value in the cache and saves it to disk."""
        cache_file = self._get_cache_file_path(func_file_path)
        self._load_cache_if_needed(cache_file)
        self._caches[cache_file][key] = value
        with open(cache_file, "w") as f:
            json.dump(self._caches[cache_file], f, indent=4)

    def clear(self):
        """Clears all in-memory cache data."""
        self._caches = {}

    def stats(self):
        """Returns statistics about the on-disk cache."""
        total_items = sum(len(cache) for cache in self._caches.values())
        return {"total_items": total_items, "cached_files": len(self._caches)}


# Global cache instance used by all @yolo decorated functions
cache = YoloCache()
