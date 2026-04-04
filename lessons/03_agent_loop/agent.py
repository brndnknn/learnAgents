# Lesson 3: The Agent Loop
# Goal: build the loop that calls tools repeatedly until the model has an answer.
#
# Read README.md first, then fill in the 6 TODOs inside run_agent().

import ollama

MODEL = "llama3.1"
MAX_ITERATIONS = 10

# --- Tool implementations (already done) ---

def get_weather(city: str) -> str:
    return f"The weather in {city} is 22°C and sunny."

def add_numbers(a: float, b: float) -> float:
    return a + b

# --- Tool registry: name → function ---
TOOL_REGISTRY = {
    "get_weather": get_weather,
    "add_numbers": add_numbers,
}

# --- Tool schemas (already done — same as Lesson 2) ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    },
]


def run_agent(prompt: str) -> str:
    """Run the agent loop until the model gives a final text answer."""

    # TODO 1: initialize `messages` as a list with one dict:
    # role="user", content=prompt
    messages = []  # replace this

    for iteration in range(MAX_ITERATIONS):
        print(f"\n--- iteration {iteration + 1} ---")

        # TODO 2: call ollama.chat() with MODEL, messages, and tools=TOOLS
        # Store the result in `response`

        # Append the model's message to history so it sees its own reasoning
        messages.append(response.message)

        # TODO 3: check if response.message.tool_calls is non-empty
        # If yes: dispatch the tools (see TODO 4)
        # If no:  break out of the loop (see TODO 5)

        # TODO 4 (inside the "yes" branch):
        # Loop over response.message.tool_calls. For each tool_call:
        #   name = tool_call.function.name
        #   args = tool_call.function.arguments
        #   fn   = TOOL_REGISTRY[name]
        #   result = fn(**args)
        #   print(f"  tool {name}({args}) → {result}")
        #   append to messages: role="tool", content=str(result)

        # TODO 5 (inside the "no" branch):
        # print("  model gave final answer")
        # break

    # TODO 6: return the final assistant content
    # It's in the last message. If the loop hit MAX_ITERATIONS without a
    # text answer, return a fallback string like "Agent hit iteration limit."
    pass  # replace this


# --- Run it ---
answer = run_agent(
    "What's the weather in Paris and London? Also, what is 42 + 58?"
)
print(f"\n=== Final answer ===\n{answer}")
