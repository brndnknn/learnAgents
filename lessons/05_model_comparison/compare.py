# Lesson 05: Model Comparison — Agent Tasks (Capstone)
# Goal: compare local Ollama models on agentic tasks — tool calling, multi-step
#       reasoning, and accuracy — building on patterns from lessons 2–4.
#
# Run with:
#   python compare.py                           # auto-discover all local models
#   python compare.py --models llama3.1 mistral
#   python compare.py --task math              # run only the math task

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

# --- Tool implementations ---

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
        # Return as int if it's a whole number
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

# --- Tool registry and schemas ---

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
# Each task has a prompt, an expected keyword to look for in the response,
# and a filter for which tools should be called.

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


def run_agent_task(model: str, task: dict) -> dict:
    """
    Run a single agent task using the full agent loop (lesson 03 pattern).
    Returns timing, iteration count, tool call count, and the final response.
    """
    messages = [{"role": "user", "content": task["prompt"]}]
    start = time.perf_counter()
    tool_calls_count = 0
    iterations = 0

    for iteration in range(MAX_ITERATIONS):
        iterations += 1
        response = ollama.chat(model=model, messages=messages, tools=TOOLS)
        messages.append(response.message)

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments
                fn = TOOL_REGISTRY[name]
                result = fn(**args)
                tool_calls_count += 1
                messages.append({"role": "tool", "content": str(result)})
        else:
            break

    end = time.perf_counter()
    final_text = response.message.content or ""

    return {
        "task_name": task["name"],
        "prompt": task["prompt"],
        "response_text": final_text.strip(),
        "latency_total_ms": round((end - start) * 1000, 1),
        "iterations": iterations,
        "tool_calls_count": tool_calls_count,
        "accuracy": 1 if score_task(final_text, task["expected"]) else 0,
    }


def score_task(response: str, expected: str) -> bool:
    """Return True if the expected keyword appears in the response."""
    return expected.lower() in response.lower()


def benchmark_agent(model: str, tasks: list[dict]) -> dict:
    """Run all agent tasks against a model and return aggregated results."""
    print(f"  Benchmarking {model}...", flush=True)
    runs = []
    for task in tasks:
        print(f"    task: {task['description']}", flush=True)
        result = run_agent_task(model, task)
        runs.append(result)

    avg_latency = sum(r["latency_total_ms"] for r in runs) / len(runs)
    avg_iterations = sum(r["iterations"] for r in runs) / len(runs)
    total_tool_calls = sum(r["tool_calls_count"] for r in runs)
    correct = sum(r["accuracy"] for r in runs)
    task_success_rate = correct / len(runs)

    return {
        "model": model,
        "avg_latency_total_ms": round(avg_latency, 1),
        "avg_iterations": round(avg_iterations, 1),
        "total_tool_calls": total_tool_calls,
        "tasks_correct": correct,
        "task_count": len(runs),
        "task_success_rate": round(task_success_rate, 2),
        "runs": runs,
    }


def print_table(results: list[dict]) -> None:
    """Print a formatted ASCII comparison table to stdout."""
    model_col = max(len("Model"), max(len(r["model"]) for r in results))

    header = (
        f"{'Model':<{model_col}}  "
        f"{'Avg Latency':>13}  "
        f"{'Avg Iters':>10}  "
        f"{'Tool Calls':>11}  "
        f"{'Accuracy':>10}"
    )
    sep = "-" * len(header)

    print("\n" + sep)
    print(header)
    print(sep)
    for r in results:
        accuracy_str = f"{r['tasks_correct']}/{r['task_count']}"
        print(
            f"{r['model']:<{model_col}}  "
            f"{r['avg_latency_total_ms']:>12.1f}ms  "
            f"{r['avg_iterations']:>10.1f}  "
            f"{r['total_tool_calls']:>11}  "
            f"{accuracy_str:>10}"
        )
    print(sep)

    # Per-task accuracy breakdown
    print("\n--- Per-task accuracy ---")
    task_names = [run["task_name"] for run in results[0]["runs"]]
    for task_name in task_names:
        row = f"  {task_name:<20}"
        for r in results:
            run = next(run for run in r["runs"] if run["task_name"] == task_name)
            row += f"  [{r['model']}: {'PASS' if run['accuracy'] else 'FAIL'}]"
        print(row)
    print()


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
