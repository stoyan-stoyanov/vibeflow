from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from vibeflow.prompts import get_system_prompt, get_function_prompt

client = OpenAI()
async_client = AsyncOpenAI()


class FunctionCode(BaseModel):
    code: str


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
    return completion.choices[0].message.content


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
    return completion.choices[0].message.content
