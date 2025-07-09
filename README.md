<p align="center">
  <img src="https://github.com/stoyan-stoyanov/yololang/blob/main/docs/yololang.png"/>
</p>

Documentation: <a href="https://yololang.readthedocs.io/" target="_blank">https://yololang.readthedocs.io</a></br>

![License](https://img.shields.io/github/license/stoyan-stoyanov/yololang)
![PyPi](https://img.shields.io/pypi/v/yololang)
![Stars](https://img.shields.io/github/stars/stoyan-stoyanov/yololang?style=social)
![Release date](https://img.shields.io/github/release-date/stoyan-stoyanov/yololang?style=social)

## From docstrings to done. Sometimes.
Life's too short for boilerplate. `yololang` is a python package for developers who have too much trust in AI and are not afraid to move fast and break things with AI slop. 
`yololang` generates function implementations from function definitions, using your type hints and docstrings. Stop implementing, start believing. Just define a function stub with type hints and a docstring, and `@yolo` will do the rest. It's the ultimate tool when your need for speed outweighs your fear of beautifully crafted AI spaghetti code.

## 🛠️ Features
- **AI-Powered Function Generation**: Automatically generate function implementations using LLMs
- **Persistent Caching**: Generated functions are cached locally to avoid redundant API calls between runs.
- **Async and Sync Support**: Works seamlessly with both `def` and `async def` functions.
- **Simple API**: Just add the `@yolo` decorator to your function stubs
- **Test-Driven Generation**: Use the `@yolo_test` decorator to validate, generate, and cache functions in a single step.

## 🚀 Quick Start

1. Install the package:
```bash
pip install yololang
```

2. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

3. Create a Python file with your function stubs:
```python

from yololang import yolo

@yolo
def greet(name: str) -> str:
    """Return a friendly greeting to the given name."""
    pass

@yolo
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass

# Use the functions as you would any other function
# yolo will generate the function implementation at runtime
print(greet("John Doe"))
print(f"2 + 2 = {add(2, 2)}")
```

4. Run it:
```bash
python basic_usage.py
```

Example output:
```
Hello, John Doe!
2 + 2 = 4
```
*(The exact greeting may vary depending on the AI model's response)*

## 📚 Use Cases and Examples
`yololang` is quite versatile and can be used in different scenarios. Here are a few examples:
*   **Basic sync and async functions**: The most straightforward use case is to generate simple synchronous and asynchronous functions. Just define a stub with type hints and a docstring, and `@yolo` will do the rest. [Examples](https://yololang.readthedocs.io/en/latest/Getting%20Started/).
*   **Class methods**: Yolo can also decorate methods within your classes to give them AI-powered capabilities. `yolo` is context-aware and can use other methods and `__init__` properties of the class. [Examples](https://yololang.readthedocs.io/en/latest/Classes/).
*   **Building APIs**: Because `yolo` can generate async functions, it can be used to dynamically define functions for API endpoints in FastAPI. [Examples](https://yololang.readthedocs.io/en/latest/FastAPI/).
*   **Function Calling for Agents**: `yolo` can be used to dynamically define tools for AI agents, allowing them to perform complex tasks by generating and executing code on the fly. [Examples](https://yololang.readthedocs.io/en/latest/Agents/).
*   **Test-Driven Generation**: Validate your AI-generated functions and pre-populate your cache with battle-tested code before you even run your main application. [Examples](https://yololang.readthedocs.io/en/latest/Testing%20Functions/).

For all examples check our [examples](examples) directory. 

Our full documentation is available at [Read the Docs](https://yololang.readthedocs.io/en/latest/).

## 🧪 Test-Driven Generation
`yololang` supports a powerful **Test-Driven Generation (TDG)** workflow. By using the `@yolo_test` decorator in your `pytest` tests, you can ensure that only validated, working code is cached and used in your application.

Here’s how it works:
- Write a test for your `@yolo`-decorated function stub.
- Add the `@yolo_test` decorator to your test function.
- Run `pytest`.

If the test passes, the generated function is saved to the cache. If it fails, `@yolo_test` automatically deletes the faulty function from the cache, keeping your project clean.

For a full guide, check out the [Testing documentation](docs/Testing.md).

## 🤖 How Yolo Works

1. When you decorate a function with `@yolo`, it:
   - Extracts the function's name, signature, and docstring
   - Validates that all parameters have type hints and a docstring is present
   - Sends this information to an AI model to generate an implementation
   - Executes the generated code in a secure way
   - Caches the generated function for future use
   - Returns the generated function

2. On subsequent calls, the cached implementation is used instead of generating a new one

3. If anything goes wrong during code generation or execution, a descriptive error is raised

## Cache Management
YOLO features a persistent cache to avoid regenerating functions across multiple runs. Here’s how it works:
- **Persistent Storage**: Generated function source code is saved in a `yolo.cache.json` file. This file is created in the same directory as the script you are running, making the cache local to your project.
- **Intelligent Invalidation**: The cache is smart. If you change a function's signature (arguments or type hints) or its docstring, YOLO will automatically detect the change, invalidate the old entry, and regenerate the function on the next call.
- **How to Clear**: To clear the cache, simply delete the `yolo.cache.json` file from your project directory.

## Requirements and Configuration

Requires:
- Python 3.7+
- An OpenAI API key

To set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```


## 📃 License

MIT

## ❤️ How you can help?
Thank you for spending time going over our README! 

If you like the project please consider giving it a star, sharing it with friends or on social media.

If you've tried yololang and have some issues, feedback or ideas feel free to open an issue or reach out!

If you find yololang exciting and you are considering contributing, please check [`CONTRIBUTING.md`](https://github.com/stoyan-stoyanov/yololang/blob/main/CONTRIBUTING.md).

## ✉️ Contact
If you want to reach out please don't hesitate to connect on the following social media:

[Threads](https://www.threads.net/@sptstoyanov)<br/>
[LinkedIn](https://www.linkedin.com/in/spstoyanov/)<br/>
[Twitter](https://twitter.com/stoyanpstoyanov)<br/>

I would love to hear from you!