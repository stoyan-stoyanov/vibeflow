from pydantic import BaseModel
from vibeflow.prompts import get_system_prompt, get_function_prompt
import os
import re

class FunctionCode(BaseModel):
    code: str


def _extract_code_block_from_response(text: str) -> str:
    """Extracts code from markdown fences if present; otherwise returns text."""
    if not isinstance(text, str):
        return ""
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else text


def get_code(
    function_name: str,
    signature: str,
    docstring: str,
    class_name: str = None,
    init_source_code: str = None,
    other_methods: dict = None,
    is_async: bool = False,
) -> str:
    """Calls the AI model to generate function code based on the provided context."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The 'openai' package is required to generate code. Install it via 'pip install openai'."
        ) from exc

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {
                "role": "user",
                "content": get_function_prompt(
                    function_name,
                    signature,
                    docstring,
                    class_name,
                    init_source_code,
                    other_methods,
                    is_async,
                ),
            },
        ],
    )
    content = completion.choices[0].message.content
    return _extract_code_block_from_response(content)


async def async_get_code(
    function_name: str,
    signature: str,
    docstring: str,
    class_name: str = None,
    init_source_code: str = None,
    other_methods: dict = None,
    is_async: bool = False,
) -> str:
    """Calls the AI model asynchronously to generate function code."""
    try:
        from openai import AsyncOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The 'openai' package is required to generate code. Install it via 'pip install openai'."
        ) from exc

    async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = await async_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {
                "role": "user",
                "content": get_function_prompt(
                    function_name,
                    signature,
                    docstring,
                    class_name,
                    init_source_code,
                    other_methods,
                    is_async,
                ),
            },
        ],
    )
    content = completion.choices[0].message.content
    return _extract_code_block_from_response(content)
