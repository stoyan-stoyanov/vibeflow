import asyncio
from yololang import yolo

@yolo
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
