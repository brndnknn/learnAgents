# Lesson 2: Tool Calling
# Goal: define tools, get the model to call one, dispatch it yourself.
#
# Read README.md first, then fill in the 5 TODOs below.

import ollama

MODEL = "llama3.2:3b"
#"granite4:350m"

# --- Tool implementations (already done) ---

def get_weather(city: str) -> str:
    """Fake weather tool — returns a hardcoded response."""
    return f"The weather in {city} is 22°C and sunny."

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

# --- Tool schemas ---
# Each schema tells the model: what the tool is called, what it does,
# and what arguments it takes. See README.md for the full format.

# TODO 1: Write the JSON Schema dict for get_weather.
# Hint: tool schemas follow OpenAI-style function schema format —
#       look at the TOOLS list structure in the README.
get_weather_schema = {
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
}  # replace this

# TODO 2: Write the JSON Schema dict for add_numbers.
add_numbers_schema = {
    "type": "function",
    "function": {
        "name": "add_numbers",
        "description": "adds two numbers together",
        "parameters":{
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to add"
                },
                "b": {
                    "type": "number",
                    "description": "The second number to add"
                }
            },
            "required": ["a", "b"]
        }
    }
} 

# Collect schemas into a list to pass to ollama.chat()
TOOLS = [
    # TODO (part of 1 & 2): add your two schema dicts here — one per tool
    get_weather_schema,
    add_numbers_schema
]

# --- Dispatch map: tool name → Python function ---
DISPATCH = {
    "get_weather": get_weather,
    "add_numbers": add_numbers,
}

# --- Main ---

# Try a prompt that should trigger one of the tools.
# Change this to trigger the other tool too.
user_prompt = "What's the weather in Tokyo?"
# "What's 12.2 plus -44.5"

print(f"User: {user_prompt}\n")

client = ollama.Client()

# TODO 3: Send the user prompt to the model with your tool schemas attached.
response = client.chat(
    model=MODEL,
    tools=TOOLS,
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": user_prompt }
    ]
    
    
    
)

# TODO 4: Check whether the model chose to call a tool or reply directly,
#         and print the outcome.
if response.message.content:

    print(f"Response: {response.message.content}")
    print()
if response.message.tool_calls:
    print(f"Model called a tool\n")
    # TODO 5: Dispatch any requested tool calls using DISPATCH and print each result.
    # Hint: each tool_call has a .function attribute with .name and .arguments.
    for tool_called in response.message.tool_calls:
        print(tool_called.function.arguments)
        fn = DISPATCH[tool_called.function.name]
        if tool_called.function.name == 'add_numbers':
            args = {k: float(v) for k, v in tool_called.function.arguments.items()}
        else:
            args = tool_called.function.arguments
        result = fn(**args)
        print(result)
    