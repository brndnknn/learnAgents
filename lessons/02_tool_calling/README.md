# Lesson 2: Tool Calling

## What you'll learn
How to define tools (functions the model can request), pass them to the model,
and dispatch the model's tool calls back to real Python functions.

## Key concept: tools in LLMs

Normally a model replies with text. With tool calling, you give the model a
list of tools it *can* call. When it needs one, instead of answering it
responds with a **tool call** — a structured request for you to run a function
and return the result.

The model never runs code. You do. The model just asks.

---

## Tool schema format

Each tool is a dict with this shape:

```python
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. 'London'"
                }
            },
            "required": ["city"]
        }
    }
}
```

The `description` fields matter — the model reads them to decide when to call
the tool and what arguments to pass.

---

## The response when a tool is called

When the model wants to use a tool, `response.message.content` is empty and
`response.message.tool_calls` is a list:

```python
[
    ToolCall(
        function=Function(
            name='get_weather',
            arguments={'city': 'London'}
        )
    )
]
```

You loop over `tool_calls`, call the matching Python function with
`tool_call.function.arguments`, and print (or store) the result.

---

## Your task

Open `tools.py`. There are 5 TODOs. Fill them in so the script:

1. Writes the tool schema dict for `get_weather`
2. Writes the tool schema dict for `add_numbers`
3. Calls `ollama.chat()` with both schemas in `tools=[...]`
4. Checks whether `response.message.tool_calls` is non-empty
5. Loops over tool calls, dispatches to the right Python function, prints results

**Tip:** Use a dict to map tool names to functions:
```python
DISPATCH = {"get_weather": get_weather, "add_numbers": add_numbers}
fn = DISPATCH[tool_call.function.name]
result = fn(**tool_call.function.arguments)
```

Try different user prompts to trigger different tools.

Run it with:
```
python lessons/02_tool_calling/tools.py
```
