import sys
import traceback
from functools import wraps
from vibeflow.cache import cache as global_cache


def vibe_test(test_func):
    """
    A decorator for test functions that run vibe-generated functions.
    If the test fails, it finds the generated function in the traceback
    and removes it from the cache to prevent caching faulty code.
    """

    @wraps(test_func)
    def wrapper(*args, **kwargs):
        try:
            test_func(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            try:
                # Walk the traceback to find the frame where the vibe function was called
                tb = exc_tb
                vibe_func = None
                while tb is not None:
                    frame = tb.tb_frame
                    # Check local variables in the frame for a vibe-generated function
                    for var in frame.f_locals.values():
                        if hasattr(var, "vibe_info"):
                            vibe_func = var
                            break
                    if vibe_func:
                        break
                    tb = tb.tb_next

                if vibe_func:
                    info = vibe_func.vibe_info
                    cache_key = info["cache_key"]
                    func_file_path = info["func_file_path"]
                    print(
                        f"\nTest failed. Deleting function '{(vibe_func.__name__)}' from cache."
                    )
                    global_cache.delete(cache_key, func_file_path)

            finally:
                # Re-raise the original exception to ensure the test is still reported as failed
                # Use traceback.print_exc() to ensure the traceback is not lost
                traceback.print_exc()
                raise exc_type(exc_value).with_traceback(exc_tb)

    return wrapper
