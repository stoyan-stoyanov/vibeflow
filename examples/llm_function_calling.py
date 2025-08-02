from openai import OpenAI
import json
from vibeflow import vibe

client = OpenAI()

@vibe
def add(a: int, b: int) -> int:
    """Add two numbers together and return the result."""
    pass

tools = [{
    "type": "function",
    "function": {
        "name": "add",
        "description": "Add two numbers together and return the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": [
                "a",
                "b"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Add 25 and 17"}],
    tools=tools
)

tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

result = add(args["a"], args["b"])
print(f"Result of add({args['a']}, {args['b']}) is: {result}")
