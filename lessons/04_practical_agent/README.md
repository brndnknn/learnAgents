# Lesson 4: Practical Agent

## What you'll learn
How to add real tools to a working agent. You'll implement three tools from
scratch, write their schemas, and wire them into a complete agent.

## The pattern for any new tool

1. **Implement** — write a Python function that does the work
2. **Schema** — write a tool schema dict describing it to the model
3. **Register** — add it to `TOOL_REGISTRY` (name → function) and `TOOLS` (schema list)

That's it. The agent loop in this file is already complete — you only touch the tools.

---

## Your tools

### `read_file(path: str) -> str`
Read and return the contents of a file. The model will use this to look
at code or data files you point it toward.

### `list_files(directory: str) -> str`
List the files in a directory, one per line. Return the result as a string.
The model will use this to explore before deciding what to read.

### `calculate(expression: str) -> str`
Evaluate a math expression and return the result as a string.

**Safety note:** Do not use `eval()` directly — it can run arbitrary code.
Use the `ast` module to safely parse the expression:

```python
import ast, operator

SAFE_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        return SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return SAFE_OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsupported expression: {node}")

def calculate(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")
    return str(_eval(tree.body))
```

---

## Your task

Open `agent.py`. There are 6 TODOs:

1. Implement `read_file(path)`
2. Implement `list_files(directory)`
3. Implement `calculate(expression)` — use the safe `ast`-based approach above
4. Write tool schemas for all three
5. Register all three in `TOOL_REGISTRY` and add schemas to `TOOLS`
6. Write a prompt at the bottom that makes the agent use at least 2 tools

**Suggested test prompts:**
- `"List the Python files in lessons/03_agent_loop, read agent.py, and tell me what the run_agent function does."`
- `"What is (123 * 456) + 789? Also list the files in the lessons directory."`

Run it with:
```
python lessons/04_practical_agent/agent.py
```

---

## Where to go from here

- Add a `web_search(query)` tool using the `httpx` library
- Add a `run_shell(command)` tool (be careful with sandboxing!)
- Persist the messages list to a JSON file for multi-session memory
- Swap `ollama.chat` for the OpenAI client — the pattern is identical
