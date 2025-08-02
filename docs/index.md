# ✨ vibeflow
## From docstrings to done. Sometimes.

![License](https://img.shields.io/github/license/stoyan-stoyanov/vibeflow)
![PyPi](https://img.shields.io/pypi/v/vibeflow)
![Stars](https://img.shields.io/github/stars/stoyan-stoyanov/vibeflow?style=social)
![Release date](https://img.shields.io/github/release-date/stoyan-stoyanov/vibeflow?style=social)

***
Source code: [https://github.com/stoyan-stoyanov/vibeflow](https://github.com/stoyan-stoyanov/vibeflow)<br/>
***

## 🤖 About vibeflow
Life's too short for boilerplate. `vibeflow` is a python package for developers who have too much trust in AI and are not afraid to move fast and break things with AI slop. 
`vibeflow` generates function implementations from stubs, using your type hints and docstrings. Stop implementing, start believing. It's the ultimate tool for rapid prototyping when your need for speed outweighs your fear of beautifully crafted AI spaghetti code.

## 📦 Installation

1. Install the package:
```
pip install vibeflow
```

2. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY='your-api-key-here'
```

## ▶️ Example Usage

```python
from vibeflow import vibe

@vibe
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass

# Use the functions as you would any other function
print(f"2 + 2 = {add(2, 2)}")
```

## 🧪 Test-Driven Generation

`vibeflow` supports a powerful **Test-Driven Generation (TDG)** workflow that allows you to validate, generate, and cache functions all in one go using `pytest`.

By adding the `@vibe_test` decorator to your tests, you can ensure that only functions that pass your assertions are saved to the cache, keeping your project's code reliable.

For a complete walkthrough, see the [Testing Guide](Testing.md).

## 🚀 Getting Started
After installing `vibeflow` with `pip`, your go-to destination should be our [User 
Guide](user_guide/Getting Started.md). Each page shows different common use-cases 
and how to implement them with `vibeflow`. Examples range from basic function generation
to creating methods in classes, usage in FastAPI endpoints function-calling for agents.

If you have any questions check out our [FAQ](user_guide/Agents.md) section or feel free to join our 
[Github Discussions](https://github.com/stoyan-stoyanov/vibeflow/discussions) page.

We hope you find this documentation helpful and look forward to your feedback on how 
we can improve it.

## 🛠️ Features
- **AI-Powered Function Generation**: Automatically generate function implementations using LLMs
- **Persistent Caching**: Generated functions are cached locally to avoid redundant API calls between runs.
- **Async and Sync Support**: Works seamlessly with both `def` and `async def` functions.
- **Simple API**: Just add the `@vibe` decorator to your function stubs
- **Test-Driven Generation**: Use the `@vibe_test` decorator to validate, generate, and cache functions in a single step.

## 📃 License
`vibeflow` is covered by the MIT license. For more information, check 
[`LICENCE`](https://github.com/stoyan-stoyanov/vibeflow/blob/main/LICENSE).

## ❤️ How you can help?
If you like the project please consider giving it a star, sharing it with friends or on social media.

If you've tried `vibeflow` and have some issues, feedback or ideas feel free to open an issue or reach out!

If you find `vibeflow` exciting and you are considering contributing, please check [`CONTRIBUTING.md`](https://github.com/stoyan-stoyanov/vibeflow/blob/main/CONTRIBUTING.md).