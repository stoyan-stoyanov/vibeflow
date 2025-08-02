"""
Basic usage example for the VIBE decorator.

This script demonstrates how to use the @vibe decorator to generate
function implementations at runtime using AI.
"""

from vibeflow import vibe


@vibe
def greet(name: str) -> str:
    """Greet the given name with a friendly message.
    
    Args:
        name: The name to greet
        
    Returns:
        A friendly greeting message
    """
    pass


@vibe
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass


@vibe
def subtract(a: int, b: int) -> int:
    """Subtract b from a and return the result."""
    pass


if __name__ == "__main__":
    print("--- VIBE is running ---")

    # --- Now, we can use the dynamically defined functions directly ---
    print("\n--- Calling the VIBE Functions ---")
    print("\n--- the @vibe decorator is generating code for the functions on the fly ---")

    greeting = greet("John Doe")
    print(f"Result of greet('John Doe') is: {greeting}")

    result_add = add(25, 17)
    print(f"Result of add(25, 17) is: {result_add}")

    result_subtract = subtract(100, 55)
    print(f"Result of subtract(100, 55) is: {result_subtract}")

    print("\n--- Using the function again won't generate new code but will use the cached version ---")

    result_subtract = subtract(20, 30)
    print(f"Result of subtract(20, 30) is: {result_subtract}")

    print("\n--- This is it. You can now use the functions as you would any other function. ---")
