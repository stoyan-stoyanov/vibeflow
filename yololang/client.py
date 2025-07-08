from openai import OpenAI
from pydantic import BaseModel
from yololang.prompts import get_system_prompt, get_function_prompt

client = OpenAI()


class FunctionCode(BaseModel):
    code: str


def get_code(function_name: str, signature: str, docstring: str) -> str:
    completion = client.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {
                "role": "user",
                "content": get_function_prompt(function_name, signature, docstring),
            },
        ],
        response_format=FunctionCode,
    )
    return completion.choices[0].message.parsed.code
