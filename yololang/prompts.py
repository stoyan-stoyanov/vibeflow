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


def get_function_prompt(function_name: str, signature: str, docstring: str) -> str:
    return f"""
    Generate the Python code for the following function:
    Name: {function_name}
    Signature: {signature}
    Description: {docstring}
    """
