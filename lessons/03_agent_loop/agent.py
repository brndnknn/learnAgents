# Lesson 3: The Agent Loop
# Goal: build the loop that calls tools repeatedly until the model has an answer.
#
# Read README.md first, then fill in the 6 TODOs inside run_agent().

import ollama

MODEL = "llama3.2:3b"
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

client = ollama.Client()

def run_agent(prompt: str) -> str:
    """Run the agent loop until the model gives a final text answer."""

    # TODO 1: Initialize the messages list with the user's prompt.
    messages = [
        {"role": "system", "content": "you are a helpful AI assistant with the ability to use tools"},
        {"role": "user", "content": prompt}
    ]  # replace this

    for iteration in range(MAX_ITERATIONS):
        print(f"\n--- iteration {iteration + 1} ---")

        # TODO 2: Call the model with the current messages and available tools.
        response = client.chat(
            model=MODEL,
            tools=TOOLS,
            messages=messages
        )

        # Append the model's message to history so it sees its own reasoning
        messages.append(response.message)
        print(response.message)

        # TODO 3: Decide what to do based on the model's response —
        #         did it request a tool call, or provide a final answer?
        if response.message.tool_calls:
            print("model called a tool")
            for tool_called in response.message.tool_calls:
                print(tool_called)
                fn = TOOL_REGISTRY[tool_called.function.name]
                if tool_called.function.name == 'add_numbers':
                    args = {k: float(v) for k, v in tool_called.function.arguments.items()}
                else:
                    args = tool_called.function.arguments
        # TODO 4 (inside the "yes" branch):
        # Dispatch any tool calls and append their results to messages.
        # Hint: tool_call.function gives you the name and arguments dict;
        #       tool results go back as "tool" role messages.
                result = fn(**args)
                messages.append({
                    "role": "tool",
                    "content": str(result),
                })
                print(result)
                print(messages)
        # TODO 5 (inside the "no" branch):
        else:
            break

    # TODO 6: Return the model's final answer (or a fallback if MAX_ITERATIONS was hit).
    if iteration == MAX_ITERATIONS:
        return "Max Interations met before model stopped calling tools"
    else:
        return response.message.content


# --- Run it ---
answer = run_agent(
    "What's the weather in Paris and London? Also, what is 42 + 58?"
)
print(f"\n=== Final answer ===\n{answer}")
