# Lesson 2: Tool Calling
# Goal: define tools, get the model to call one, dispatch it yourself.
#
# Read README.md first, then fill in the 5 TODOs below.

import ollama

MODEL = "llama3.1"

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
get_weather_schema = {}  # replace this

# TODO 2: Write the JSON Schema dict for add_numbers.
add_numbers_schema = {}  # replace this

# Collect schemas into a list to pass to ollama.chat()
TOOLS = [
    # TODO (part of 1 & 2): add your two schema dicts here — one per tool
]

# --- Dispatch map: tool name → Python function ---
DISPATCH = {
    "get_weather": get_weather,
    "add_numbers": add_numbers,
}

# --- Main ---

# Try a prompt that should trigger one of the tools.
# Change this to trigger the other tool too.
user_prompt = "What's the weather like in Tokyo?"

print(f"User: {user_prompt}\n")

# TODO 3: Send the user prompt to the model with your tool schemas attached.


# TODO 4: Check whether the model chose to call a tool or reply directly,
#         and print the outcome.


# TODO 5: Dispatch any requested tool calls using DISPATCH and print each result.
# Hint: each tool_call has a .function attribute with .name and .arguments.
