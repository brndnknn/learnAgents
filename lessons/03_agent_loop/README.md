# Lesson 3: The Agent Loop

## What you'll learn
How to build the core agent loop — the pattern that turns a single LLM call
into a system that reasons, uses tools, and keeps going until it has an answer.

## Why a loop?

In Lesson 2, you made one tool call. But real tasks need multiple steps:

1. Model decides it needs a tool → you run it
2. Model sees the result → decides it needs another tool → you run it
3. Model has enough info → gives a final answer

The agent loop handles this automatically by:
- Keeping the full conversation history (messages list)
- Re-calling the model after each tool result
- Stopping when the model replies with text instead of a tool call

**The messages list is the agent's memory.** The model itself is stateless —
it only knows what's in the messages you send it.

---

## The `role="tool"` message

After you run a tool, you append its result to messages with `role="tool"`:

```python
messages.append({
    "role": "tool",
    "content": str(result),
})
```

The model reads this on the next iteration and continues reasoning.

---

## Stopping condition

```
if response.message.tool_calls:
    # dispatch tools, append results, continue loop
else:
    # model gave a text answer — we're done
    return response.message.content
```

Always add a `max_iterations` guard (e.g. 10) to prevent runaway loops if the
model keeps calling tools unexpectedly.

---

## Your task

Open `agent.py`. There are 6 TODOs inside `run_agent()`. Fill them in:

1. Initialize `messages` with the user's prompt
2. Call `ollama.chat()` with `messages` and `TOOLS`
3. If there are tool calls, dispatch each one
4. Append tool results to `messages` with `role="tool"`
5. If no tool calls, break the loop and return the final content
6. Add a `max_iterations` guard

The tool registry, tool functions, and debug prints are already wired up.

Run it with:
```
python lessons/03_agent_loop/agent.py
```

Watch the printed output — you should see the loop iterate, tools fire, and
a final answer arrive.
