import inspect
import hashlib
from functools import wraps
from yololang.client import get_code
from yololang.cache import cache as global_cache

# In-memory cache for materialized functions to avoid re-executing code
materialized_functions = {}


def yolo(func):
    """
    A decorator that takes a function stub (with types and a docstring),
    uses an LLM to generate the function code,
    and caches the result for future use.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        docstring = inspect.getdoc(func) or ""
        signature = inspect.signature(func)

        # Basic validation
        if not docstring:
            raise ValueError(f"{function_name} is missing a docstring.")
        params_to_check = [p for p in signature.parameters.values() if p.name != 'self']
        if params_to_check and not any(p.annotation != p.empty for p in params_to_check):
            raise ValueError(f"{function_name} is missing types.")

        # Check if this is a class method to build a context-aware cache key
        is_method = args and hasattr(args[0], '__class__') and func.__name__ in dir(args[0])

        key_source_prefix = ""
        class_name, init_source, other_methods = None, None, None
        if is_method:
            instance = args[0]
            cls = instance.__class__
            class_name = cls.__name__

            # Get __init__ source
            try:
                init_method = cls.__init__
                init_source = inspect.getsource(init_method)
                key_source_prefix += f"__init__:{init_source}:"
            except (AttributeError, TypeError, OSError):
                pass  # No custom __init__ or source not found

            # Get other method definitions
            other_methods = {}
            for name, meth in inspect.getmembers(cls, predicate=inspect.isfunction):
                if name == function_name or name == '__init__':
                    continue
                meth_sig = str(inspect.signature(meth))
                meth_doc = inspect.getdoc(meth) or ""
                other_methods[name] = {"signature": meth_sig, "docstring": meth_doc}
            
            if other_methods:
                # Sort for cache key consistency
                sorted_methods = sorted(other_methods.items())
                key_source_prefix += f"methods:{str(sorted_methods)}"

        key_source = f"{key_source_prefix}{func.__module__}.{func.__qualname__}:{str(signature)}:{docstring}"
        cache_key = hashlib.sha256(key_source.encode("utf-8")).hexdigest()

        # 1. Check in-memory cache for the materialized function
        if cache_key in materialized_functions:
            return materialized_functions[cache_key](*args, **kwargs)

        # 2. Check persistent cache for the source code
        python_code = global_cache.get(cache_key)

        # 3. If not in any cache, generate the code and save to persistent cache
        if python_code is None:
            python_code = get_code(
                function_name, signature, docstring, class_name, init_source, other_methods
            )
            global_cache[cache_key] = python_code

        # 4. Execute the code and cache the materialized function in memory
        temp_scope = {}
        try:
            exec(python_code, temp_scope)
        except Exception as e:
            raise RuntimeError(
                f"Failed to execute AI-generated code for '{function_name}': {str(e)}"
            ) from e

        newly_defined_func = temp_scope.get(function_name)

        if newly_defined_func is not None:
            materialized_functions[cache_key] = newly_defined_func
            return newly_defined_func(*args, **kwargs)

        raise RuntimeError(
            f"Could not find implementation for '{function_name}' in received code."
        )

    return wrapper
