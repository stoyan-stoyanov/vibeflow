def get_system_prompt() -> str:
    return f'''
    You are a super smart assistant that creates function code based on a given function name, signature and docstring.
    For example:
    Name: greet
    Signature: def greet(name: str):
    Docstring: Provides a friendly greeting to the given name.

    Response:
    def sum(x: int, y: int) -> int:
        """Calculates the sum of two integers and returns the result."""
        return x + y
    '''


def get_function_prompt(
    function_name: str,
    signature: str,
    docstring: str,
    class_name: str = None,
    init_source_code: str = None,
    other_methods: dict = None,
    is_async: bool = False,
) -> str:
    """Generates the prompt for the AI to create a function."""
    async_prefix = "an async " if is_async else ""
    prompt = f"""
    Generate the Python code for {async_prefix}the following function:
    Name: {function_name}
    Signature: {signature}
    Description: {docstring}
    """

    if is_async:
        prompt += "\nThe function should be defined with `async def`."

    if class_name and init_source_code:
        prompt += (
            f"\n\nNote: This is a method in the '{class_name}' class. "
            f"The class's __init__ method is implemented as follows:\n\n```python\n{init_source_code}```\n"
        )

    if other_methods:
        prompt += "The class also has the following methods. You can call them using 'self.method_name(...)':\n"
        for name, definition in other_methods.items():
            prompt += f"- `def {name}{definition['signature']}`: {definition['docstring']}\n"

    return prompt
