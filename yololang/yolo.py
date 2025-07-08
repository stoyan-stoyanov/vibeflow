import types
import inspect
from functools import wraps
from yololang.client import get_code
from yololang.cache import cache as global_cache


def generate_fn_code(func: types.FunctionType) -> str:
    """
    Takes a function object, inspects its signature and docstring,
    and uses and calls an LLM to generate the function code.
    """
    function_name = func.__name__
    docstring = inspect.getdoc(func)
    signature = inspect.signature(func)

    if not docstring:
        raise ValueError(f"{function_name} is missing a docstring.")

    if not any(
        [param.annotation != param.empty for param in signature.parameters.values()]
    ):
        raise ValueError(f"{function_name} is missing types.")

    return get_code(function_name, signature, docstring)


def yolo(func):
    """
    A decorator that takes a function stub (with types and a docstring),
    uses an LLM to generate the function code,
    and caches the result for future use.

    Args:
        func: The function to create

    Returns:
        An LLM-generated function with the same signature as the original function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = f"{func.__module__}.{func.__qualname__}"

        try:
            return global_cache[cache_key](*args, **kwargs)
        except KeyError:
            pass

        python_code = generate_fn_code(func)

        temp_scope = {}
        try:
            exec(python_code, temp_scope)
        except Exception as e:
            error_msg = (
                f"Failed to execute AI-generated code for '{func.__name__}': {str(e)}"
            )
            raise RuntimeError(error_msg) from e

        newly_defined_func = temp_scope.get(func.__name__)

        if newly_defined_func is not None:
            global_cache[cache_key] = newly_defined_func
            return newly_defined_func(*args, **kwargs)

        error_msg = (
            f"Could not find implementation for '{func.__name__}' in received code."
        )
        raise RuntimeError(error_msg)

    wrapper._is_yolo_wrapper = True

    return wrapper
