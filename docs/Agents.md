# Building Agents with YoloLang

One of the most powerful applications of `yolo` is creating simple, LLM-powered "agents." An agent is a function that, instead of performing a task itself, intelligently calls other functions (or "tools") based on a user's query.

With YoloLang, you can define a set of tool functions and an agent function, and the LLM will generate the routing logic to connect them.

## Function-Calling Agent Example

In this example, we define two tools: `get_weather` and `get_top_news_headline`. The `run_agent` function is our agent. Its docstring instructs the LLM on how to choose the correct tool based on the user's query.

```python
from openai import OpenAI
import json
from yololang import yolo

client = OpenAI()

@yolo
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
```