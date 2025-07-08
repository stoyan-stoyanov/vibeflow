import inspect
import hashlib
from functools import wraps
from yololang.client import get_code
from yololang.cache import cache as global_cache

# In-memory cache for materialized functions to avoid re-executing code
materialized_functions = {}

def yolo(func):
    """
    A decorator that inspects a function to determine if it's sync or async,
    then uses a corresponding wrapper to generate and cache its implementation.
    """
    def get_common_context(function_name, signature, docstring, args):
        is_method = args and hasattr(args[0], '__class__') and function_name in dir(args[0])
        key_source_prefix = ""
        class_name, init_source, other_methods = None, None, None

        if is_method:
            instance = args[0]
            cls = instance.__class__
            class_name = cls.__name__

            try:
                init_method = cls.__init__
                init_source = inspect.getsource(init_method)
                key_source_prefix += f"__init__:{init_source}:"
            except (AttributeError, TypeError, OSError):
                pass

            other_methods = {}
            for name, meth in inspect.getmembers(cls, predicate=inspect.isfunction):
                if name in (function_name, '__init__'):
                    continue
                meth_sig = str(inspect.signature(meth))
                meth_doc = inspect.getdoc(meth) or ""
                other_methods[name] = {"signature": meth_sig, "docstring": meth_doc}
            
            if other_methods:
                sorted_methods = sorted(other_methods.items())
                key_source_prefix += f"methods:{str(sorted_methods)}"
        
        return key_source_prefix, class_name, init_source, other_methods

    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            function_name = func.__name__
            docstring = inspect.getdoc(func) or ""
            signature = inspect.signature(func)

            key_source_prefix, class_name, init_source, other_methods = get_common_context(function_name, signature, docstring, args)
            key_source = f"async:{key_source_prefix}{func.__module__}.{func.__qualname__}:{str(signature)}:{docstring}"
            cache_key = hashlib.sha256(key_source.encode("utf-8")).hexdigest()

            func_file_path = inspect.getfile(func)

            if cache_key in materialized_functions:
                return await materialized_functions[cache_key](*args, **kwargs)

            python_code = global_cache.get(cache_key, func_file_path)
            if python_code is None:
                python_code = get_code(
                    function_name, str(signature), docstring, class_name, init_source, other_methods, is_async=True
                )
                global_cache.set(cache_key, python_code, func_file_path)

            local_scope = {}
            exec(python_code, globals(), local_scope)
            live_function = local_scope[function_name]
            materialized_functions[cache_key] = live_function

            return await live_function(*args, **kwargs)
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            function_name = func.__name__
            docstring = inspect.getdoc(func) or ""
            signature = inspect.signature(func)

            key_source_prefix, class_name, init_source, other_methods = get_common_context(function_name, signature, docstring, args)
            key_source = f"sync:{key_source_prefix}{func.__module__}.{func.__qualname__}:{str(signature)}:{docstring}"
            cache_key = hashlib.sha256(key_source.encode("utf-8")).hexdigest()

            func_file_path = inspect.getfile(func)

            if cache_key in materialized_functions:
                return materialized_functions[cache_key](*args, **kwargs)

            python_code = global_cache.get(cache_key, func_file_path)
            if python_code is None:
                python_code = get_code(
                    function_name, str(signature), docstring, class_name, init_source, other_methods, is_async=False
                )
                global_cache.set(cache_key, python_code, func_file_path)

            local_scope = {}
            exec(python_code, globals(), local_scope)
            live_function = local_scope[function_name]
            materialized_functions[cache_key] = live_function

            return live_function(*args, **kwargs)
        return sync_wrapper
