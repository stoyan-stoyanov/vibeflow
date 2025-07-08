# 🚀💥 yololang
## From docstrings to done. Sometimes.
Life's too short for boilerplate. `yololang` is a python package for developers who have too much trust in AI and are not afraid to move fast and break things with AI slop. 
`yololang` generates function implementations from stubs, using your type hints and docstrings. Stop implementing, start believing. It's the ultimate tool for rapid prototyping when your need for speed outweighs your fear of beautifully crafted AI spaghetti code.

## Features
- **AI-Powered Function Generation**: Automatically generate function implementations using AI
- **Persistent Caching**: Generated functions are cached locally to avoid redundant API calls between runs.
- **Type-Aware**: Leverages Python type hints for better code generation
- **Simple API**: Just add the `@yolo` decorator to your function stubs
- **Async and Sync Support**: Works seamlessly with both `def` and `async def` functions.

## Installation
```bash
pip install yololang
```

## Use Cases
`yololang` is versatile and can be used in a variety of scenarios, from simple function generation to more complex applications. Here are some of the main use cases:
*   **Basic Functions**: The most straightforward use case is to generate simple synchronous functions. Just define a stub with type hints and a docstring, and `@yolo` will do the rest. [Learn more](docs/Getting%20Started.md).
*   **Asynchronous Operations**: Seamlessly generate `async` functions for use in modern asynchronous applications, such as with `asyncio` or web frameworks like FastAPI. [Learn more](docs/Async%20Functions.md).
*   **Class Methods**: Decorate methods within your classes to give them AI-powered capabilities. `yolo` is context-aware and can use other methods and `__init__` properties of the class. [Learn more](docs/Classes.md).
*   **Function Calling for Agents**: `yolo` can be used to dynamically define tools for AI agents, allowing them to perform complex tasks by generating and executing code on the fly. [Learn more](docs/Agents.md).

## Quick Start

1. Install the package:
```bash
pip install yololang
```

2. Create a Python file with your function stubs:
```python

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

@yolo
async def fetch_data(url: str) -> dict:
    """Fetches JSON data from a URL and returns it as a dictionary."""
    pass

# Use the functions
print(greet("John Doe"))
print(f"2 + 2 = {add(2, 2)}")
```

3. Run it:
```bash
python basic_usage.py
```

Example output:
```
Hello, John Doe!
2 + 2 = 4
```
*(The exact greeting may vary depending on the AI model's response)*

## Cache Management
YOLO features a persistent cache to avoid regenerating functions across multiple runs. Here’s how it works:
- **Persistent Storage**: Generated function source code is saved in a `yolo.cache.json` file. This file is created in the same directory as the script you are running, making the cache local to your project.
- **Intelligent Invalidation**: The cache is smart. If you change a function's signature (arguments or type hints) or its docstring, YOLO will automatically detect the change, invalidate the old entry, and regenerate the function on the next call.
- **How to Clear**: To clear the cache, simply delete the `yolo.cache.json` file from your project directory.

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