# Async Function Support

Vibeflow provides full support for `async` functions, allowing you to use the `@vibe` decorator in modern asynchronous Python applications, including with web frameworks like FastAPI.

## Standalone Async Functions

You can decorate `async` functions in the same way you decorate synchronous ones. Vibeflow will detect the `async def` signature and generate an awaitable coroutine.

### Example: `async_functions.py`

Here is a basic example of a standalone `async` function managed by Vibeflow.

```python
import asyncio
from vibeflow import vibe

@vibe
async def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass

async def main():
    """Main function to run the async function add."""
    print("Adding 25 and 17...")
    result = await add(25, 17)
    print(f"Result of add(25, 17) is: {result}")

if __name__ == "__main__":
    # This allows the async function to be run from the command line.
    asyncio.run(main())
```

To run this, you simply execute the script, and `asyncio.run()` handles the event loop.
