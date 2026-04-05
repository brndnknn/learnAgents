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

    # TODO 1: Initialize the messages list with the user's prompt.
    messages = []  # replace this

    for iteration in range(MAX_ITERATIONS):
        print(f"\n--- iteration {iteration + 1} ---")

        # TODO 2: Call the model with the current messages and available tools.

        # Append the model's message to history so it sees its own reasoning
        messages.append(response.message)

        # TODO 3: Decide what to do based on the model's response —
        #         did it request a tool call, or provide a final answer?

        # TODO 4 (inside the "yes" branch):
        # Dispatch any tool calls and append their results to messages.
        # Hint: tool_call.function gives you the name and arguments dict;
        #       tool results go back as "tool" role messages.

        # TODO 5 (inside the "no" branch):
        # break

    # TODO 6: Return the model's final answer (or a fallback if MAX_ITERATIONS was hit).
    pass  # replace this


# --- Run it ---
answer = run_agent(
    "What's the weather in Paris and London? Also, what is 42 + 58?"
)
print(f"\n=== Final answer ===\n{answer}")
