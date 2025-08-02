# Getting Started with Vibeflow

Welcome to Vibeflow! This guide will walk you through the basic usage of the `@vibe` decorator to generate function implementations from just a signature and a docstring.

## Basic Usage

The core of Vibeflow is the `@vibe` decorator. You can apply it to any function stub that has a type-hinted signature and a descriptive docstring. Vibeflow will automatically generate the Python code to make it work.

### Example: `basic_usage.py`

Here is a simple example demonstrating how to create several functions with `@vibe`:

```python
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
    print("Decorators have already replaced the stub functions with AI-generated code.")

    # --- Now, we can use the dynamically defined functions directly ---
    print("\n--- Calling the VIBE Functions ---")

    greet("John Doe")

    result_add = add(25, 17)
    print(f"Result of add(25, 17) is: {result_add}")

    result_subtract = subtract(100, 55)
    print(f"Result of subtract(100, 55) is: {result_subtract}")

    print("\n--- Using the function again won't generate new code but will use the cached version ---")

    result_subtract = subtract(20, 30)
    print(f"Result of subtract(20, 30) is: {result_subtract}")

    print("\n--- This is it. You can now use the functions as you would any other function. ---")
```

When you run this script, Vibeflow calls an LLM to generate the code for `greet`, `add`, and `subtract` based on their definitions. The generated code is then cached in `vibe.cache.json`, so subsequent runs will be much faster.

## Async Support

Vibeflow also provides full support for `async` functions. You can decorate an `async def` function, and Vibeflow will generate a proper awaitable coroutine.

```python
@vibe
async def fetch_data(url: str) -> dict:
    """Fetches JSON data from a URL and returns it as a dictionary.""" 
    pass
```

For more details on using Vibeflow in asynchronous applications, see the [Async Functions](./Async%20Functions.md) documentation.
