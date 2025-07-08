"""
Basic usage example for the YOLO decorator.

This script demonstrates how to use the @yolo decorator to generate
function implementations at runtime using AI.
"""

from yololang import yolo, get_cache_stats, clear_cache


@yolo
def greet(name: str) -> str:
    """Greet the given name with a friendly message.
    
    Args:
        name: The name to greet
        
    Returns:
        A friendly greeting message
    """
    pass


@yolo
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass


@yolo
def subtract(a: int, b: int) -> int:
    """Subtract b from a and return the result."""
    pass


if __name__ == "__main__":
    print("--- YOLO is running ---")
    print("Decorators have already replaced the stub functions with AI-generated code.")

    # --- Now, we can use the dynamically defined functions directly ---
    print("\n--- Calling the YOLO Functions ---")

    greet("John Doe")

    result_add = add(25, 17)
    print(f"Result of add(25, 17) is: {result_add}")

    result_subtract = subtract(100, 55)
    print(f"Result of subtract(100, 55) is: {result_subtract}")

    # Show cache statistics
    print("\n--- YOLO Cache Statistics ---")
    stats = get_cache_stats()
    print(f"Cached functions: {stats['size']}")
    print(f"Max cache size: {stats['max_size']}")
    print(f"Cache TTL: {stats['ttl'] or 'No expiration'}")
