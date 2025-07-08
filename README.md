# 🚀💥 yololang: from Docstring to Done. Sometimes.
Life's too short for boilerplate. `yololang` is a python package for developers who have too much trust in AI and are not afraid to move fast and break things with AI slop. 
`yololang` generates function implementations from stubs, using your type hints and docstrings as the absolute, unquestionable truth. Stop implementing, start believing. It's the ultimate tool for rapid prototyping when your need for speed outweighs your fear of beautifully crafted AI slop.

## Features

- **AI-Powered Function Generation**: Automatically generate function implementations using AI
- **Intelligent Global Caching**: Generated functions are cached in memory to avoid redundant API calls
- **Type-Aware**: Leverages Python type hints for better code generation
- **Simple API**: Just add the `@yolo` decorator to your function stubs

## Installation

```bash
pip install yololang
```

## Quick Start

1. Install the package:
```bash
pip install yololang
```

2. Create a Python file with your function stubs:
```python
# basic_usage.py
from yololang import yolo

@yolo
def greet(name: str) -> str:
    """Return a friendly greeting to the given name.
    
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

# Use the functions
print(greet("John Doe"))
print(f"2 + 2 = {add(2, 2)}")
```

3. Run it:
```bash
python basic_usage.py
```

## Error Handling

YOLO provides clear error messages when something goes wrong:

- **Missing Docstring**: Raises `ValueError` if a function is missing a docstring
- **Missing Type Hints**: Raises `ValueError` if function parameters lack type annotations
- **Code Generation Errors**: Raises `RuntimeError` if the AI-generated code fails to execute

## Cache Management

YOLO includes a simple global cache to avoid regenerating the same function multiple times:

```python
from yololang import get_cache_stats, clear_cache

# Get cache statistics
stats = get_cache_stats()
print(stats)  # {'size': 2, 'max_size': 1000, 'ttl': None}

# Clear the cache if needed
clear_cache()
```

## How It Works

1. When you decorate a function with `@yolo`, it:
   - Extracts the function's name, signature, and docstring
   - Validates that all parameters have type hints and a docstring is present
   - Sends this information to an AI model to generate an implementation
   - Executes the generated code in a secure way
   - Caches the generated function for future use
   - Returns the generated function

2. On subsequent calls, the cached implementation is used instead of generating a new one

3. If anything goes wrong during code generation or execution, a descriptive error is raised

## Requirements

- Python 3.7+
- An OpenAI API key

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Example Project

Check out the `examples/` directory for more usage examples, including how to handle different types of functions and error cases.

## License

MIT