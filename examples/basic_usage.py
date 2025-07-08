"""
Basic usage example for the YOLO decorator.

This script demonstrates how to use the @yolo decorator to generate
function implementations at runtime using AI.
"""

from yololang import yolo


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

    print("\n--- Using the function again won't generate new code but will use the cached version ---")

    result_subtract = subtract(20, 30)
    print(f"Result of subtract(20, 30) is: {result_subtract}")

    print("\n--- This is it. You can now use the functions as you would any other function. ---")
