# Lesson 05: Model Comparison — Agent Tasks (Capstone)
# Goal: compare local Ollama models on agentic tasks — tool calling, multi-step
#       reasoning, and accuracy — building on patterns from lessons 2–4.
#
# Read README.md first, then fill in the 5 TODOs below.
#
# Run with:
#   python lesson.py                           # auto-discover all local models
#   python lesson.py --models llama3.1 mistral
#   python lesson.py --task math              # run only the math task

import argparse
import ast
import json
import operator
import os
import time

import ollama

MAX_ITERATIONS = 10
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results.json")
SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample.txt")

# --- Tool implementations (already done) ---

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def calculate(expression: str) -> str:
    """Safely evaluate a math expression and return the result as a string."""
    try:
        tree = ast.parse(expression, mode="eval")
        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp):
                return _SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
            raise ValueError(f"Unsupported expression: {ast.dump(node)}")
        result = _eval(tree)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def read_file(path: str) -> str:
    """Read a file and return its contents."""
    try:
        full_path = path if os.path.isabs(path) else os.path.join(os.path.dirname(__file__), path)
        with open(full_path) as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: file not found: {path}"

# --- Tool registry and schemas (already done) ---

TOOL_REGISTRY = {
    "calculate": calculate,
    "read_file": read_file,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression and return the numeric result",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression, e.g. '7 * 8' or '144 / 12'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file by path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute path to the file",
                    }
                },
                "required": ["path"],
            },
        },
    },
]

# --- Agent tasks ---

TASKS = [
    {
        "name": "math",
        "prompt": "What is 144 divided by 12?",
        "expected": "12",
        "description": "Single tool call — math",
    },
    {
        "name": "file_read",
        "prompt": "Read the file sample.txt and tell me the first word.",
        "expected": "Hello",
        "description": "Single tool call — file I/O",
    },
    {
        "name": "multi_step",
        "prompt": "Calculate 7 * 8, then tell me: is the result greater than 50?",
        "expected": "56",
        "description": "Multi-step reasoning with tool call",
    },
]


def list_local_models() -> list[str]:
    """Return names of all models currently available in Ollama."""
    response = ollama.list()
    return [m.model for m in response.models]


# TODO 1: Implement run_agent_task()
# Build the full agent loop (same pattern as lesson 03) for a single task.
#
# Steps:
#   1. Initialize messages = [{"role": "user", "content": task["prompt"]}]
#   2. Record start = time.perf_counter()
#   3. Loop up to MAX_ITERATIONS:
#        a. Call ollama.chat(model=model, messages=messages, tools=TOOLS)
#        b. Append response.message to messages
#        c. If response.message.tool_calls is non-empty → dispatch tools (TODO 2)
#        d. Otherwise → break (model gave final answer)
#   4. Compute latency_total_ms = (end - start) * 1000
#   5. Return a dict with: task_name, prompt, response_text, latency_total_ms,
#                          iterations, tool_calls_count, accuracy (call score_task)
def run_agent_task(model: str, task: dict) -> dict:
    raise NotImplementedError("TODO 1: implement the agent loop in run_agent_task()")


# TODO 2: Implement tool dispatch (inside run_agent_task above)
# When response.message.tool_calls is non-empty, loop over each tool_call:
#   name   = tool_call.function.name
#   args   = tool_call.function.arguments
#   fn     = TOOL_REGISTRY[name]
#   result = fn(**args)
#   tool_calls_count += 1
#   append to messages: {"role": "tool", "content": str(result)}
#
# This is a reminder stub — the actual code goes inside run_agent_task().
_TODO_2_REMINDER = "See TODO 2 comment — add tool dispatch inside run_agent_task()"


# TODO 3: Implement score_task()
# Return True if the expected string appears anywhere in the response (case-insensitive).
# Hint: use `expected.lower() in response.lower()`
def score_task(response: str, expected: str) -> bool:
    raise NotImplementedError("TODO 3: implement score_task()")


# TODO 4: Implement benchmark_agent()
# Run run_agent_task() for each task, then aggregate results:
#   - avg_latency_total_ms: average of latency_total_ms across runs
#   - avg_iterations: average iterations
#   - total_tool_calls: sum of tool_calls_count
#   - tasks_correct: sum of accuracy scores
#   - task_success_rate: tasks_correct / len(runs)
#
# Return a dict with: model, avg_latency_total_ms, avg_iterations,
#                     total_tool_calls, tasks_correct, task_count, task_success_rate, runs
def benchmark_agent(model: str, tasks: list[dict]) -> dict:
    print(f"  Benchmarking {model}...", flush=True)
    runs = []
    for task in tasks:
        print(f"    task: {task['description']}", flush=True)
        result = run_agent_task(model, task)
        runs.append(result)

    raise NotImplementedError("TODO 4: aggregate runs and return stats dict")


# TODO 5: Implement print_table()
# Print an ASCII table with these columns:
#   Model | Avg Latency | Avg Iters | Tool Calls | Accuracy (e.g. "3/3")
#
# After the table, print a per-task accuracy breakdown showing PASS/FAIL
# for each model on each task.
#
# Hint: look at lesson 00's print_table() in compare.py for the column-width pattern.
def print_table(results: list[dict]) -> None:
    raise NotImplementedError("TODO 5: implement print_table()")


def save_json(results: list[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full results saved to: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare local Ollama models on agentic tasks"
    )
    parser.add_argument(
        "--models", nargs="+",
        help="Model names to compare (default: all local models)"
    )
    parser.add_argument(
        "--task",
        choices=[t["name"] for t in TASKS],
        help="Run only a specific task instead of all tasks"
    )
    args = parser.parse_args()

    models = args.models or list_local_models()
    if not models:
        print("No models found. Run `ollama pull llama3.1` to get started.")
        return

    tasks = [t for t in TASKS if t["name"] == args.task] if args.task else TASKS

    print(f"Comparing {len(models)} model(s) across {len(tasks)} agent task(s):\n")
    for m in models:
        print(f"  * {m}")
    print()

    all_results = []
    for model in models:
        result = benchmark_agent(model, tasks)
        all_results.append(result)

    print_table(all_results)
    save_json(all_results, RESULTS_FILE)


if __name__ == "__main__":
    main()
