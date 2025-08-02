import inspect
import hashlib
from functools import wraps
from vibeflow.client import get_code, async_get_code
from vibeflow.cache import cache as global_cache

# In-memory cache for materialized functions to avoid re-executing code
materialized_functions = {}


def vibe(func):
    """
    A decorator that inspects a function to determine if it's sync or async,
    then uses a corresponding wrapper to generate and cache its implementation.
    """

    def get_common_context(function_name, args):
        is_method = (
            args and hasattr(args[0], "__class__") and function_name in dir(args[0])
        )
        if not is_method:
            return "", None, None, None

        instance = args[0]
        cls = instance.__class__
        class_name = cls.__name__
        key_source_parts = []

        try:
            init_source = inspect.getsource(cls.__init__)
            key_source_parts.append(f"__init__:{init_source}:")
        except (AttributeError, TypeError, OSError):
            init_source = None

        other_methods = {
            name: {
                "signature": str(inspect.signature(meth)),
                "docstring": inspect.getdoc(meth) or "",
            }
            for name, meth in inspect.getmembers(cls, predicate=inspect.isfunction)
            if name not in (function_name, "__init__")
        }

        if other_methods:
            sorted_methods = sorted(other_methods.items())
            key_source_parts.append(f"methods:{str(sorted_methods)}")

        return "".join(key_source_parts), class_name, init_source, other_methods

    def _get_cache_key(args, is_async):
        function_name = func.__name__
        docstring = inspect.getdoc(func) or ""
        signature = str(inspect.signature(func))
        key_source_prefix, class_name, init_source, other_methods = get_common_context(
            function_name, args
        )

        prefix = "async:" if is_async else "sync:"
        source_components = [
            prefix,
            key_source_prefix,
            f"{func.__module__}.{func.__qualname__}:",
            f"{signature}:{docstring}",
        ]
        key_source = "".join(source_components)
        cache_key = hashlib.sha256(key_source.encode("utf-8")).hexdigest()
        return (
            cache_key,
            function_name,
            signature,
            docstring,
            class_name,
            init_source,
            other_methods,
        )

    def _materialize_function(python_code, function_name):
        local_scope = {}
        exec(python_code, globals(), local_scope)
        return local_scope[function_name]

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            (
                cache_key,
                function_name,
                signature,
                docstring,
                class_name,
                init_source,
                other_methods,
            ) = _get_cache_key(args, is_async=True)

            if cache_key in materialized_functions:
                return await materialized_functions[cache_key](*args, **kwargs)

            func_file_path = inspect.getfile(func)
            python_code = global_cache.get(cache_key, func_file_path)

            if python_code is None:
                python_code = await async_get_code(
                    function_name,
                    signature,
                    docstring,
                    class_name,
                    init_source,
                    other_methods,
                    is_async=True,
                )
                global_cache.set(cache_key, python_code, func_file_path)

            live_function = _materialize_function(python_code, function_name)
            live_function.vibe_info = {
                "cache_key": cache_key,
                "func_file_path": func_file_path,
            }
            materialized_functions[cache_key] = live_function
            return await live_function(*args, **kwargs)

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            (
                cache_key,
                function_name,
                signature,
                docstring,
                class_name,
                init_source,
                other_methods,
            ) = _get_cache_key(args, is_async=False)

            if cache_key in materialized_functions:
                return materialized_functions[cache_key](*args, **kwargs)

            func_file_path = inspect.getfile(func)
            python_code = global_cache.get(cache_key, func_file_path)

            if python_code is None:
                python_code = get_code(
                    function_name,
                    signature,
                    docstring,
                    class_name,
                    init_source,
                    other_methods,
                    is_async=False,
                )
                global_cache.set(cache_key, python_code, func_file_path)

            live_function = _materialize_function(python_code, function_name)
            live_function.vibe_info = {
                "cache_key": cache_key,
                "func_file_path": func_file_path,
            }
            materialized_functions[cache_key] = live_function
            return live_function(*args, **kwargs)

        return sync_wrapper

def clear_cache():
    """Clears all VIBE caches, including on-disk and in-memory."""
    global materialized_functions
    materialized_functions = {}
    global_cache.clear()

def get_cache_stats():
    """Returns statistics about the current state of the caches."""
    disk_stats = global_cache.stats()
    return {
        "in_memory_cache_size": len(materialized_functions),
        "disk_cache_files": disk_stats["cached_files"],
        "disk_cache_items": disk_stats["total_items"],
    }
