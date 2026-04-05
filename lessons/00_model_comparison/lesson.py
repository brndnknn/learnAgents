# Lesson 00: Model Comparison — Basic Chat
# Goal: benchmark local Ollama models on chat speed and output quality
#       so you can pick the best model before starting the other lessons.
#
# Read README.md first, then fill in the 5 TODOs below.
#
# Run with:
#   python lesson.py                           # auto-discover all local models
#   python lesson.py --models llama3.1 mistral
#   python lesson.py --prompt "Your question here"

import argparse
import json
import os
import time

import ollama

DEFAULT_PROMPTS = [
    "What is 17 * 23?",
    "Name the capital of France.",
    "Explain async/await in Python in 2 sentences.",
]

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results.json")


# TODO 1: Implement list_local_models()
# Call ollama.list() and return a list of model name strings.
# Hint: the response has a .models attribute; each model object has a .model attribute.
def list_local_models() -> list[str]:
    
    models = ollama.list().models

    model_names = []

    for model in models:
        model_names.append(model.model)

    return model_names


def run_timed_chat(model: str, prompt: str) -> dict:
    """
    Send a single chat message via streaming and capture timing + output.
    Returns a dict with latency, throughput, token count, and response text.
    """
    messages = [{"role": "user", "content": prompt}]
    start = time.perf_counter()
    first_token_time = None
    full_text = ""
    token_count = 0

    # TODO 2: Start a streaming chat and record the time of the first token.
    # Call ollama.chat(model=model, messages=messages, stream=True).
    # Iterate over the stream with `for chunk in stream:`.
    # For each chunk:
    #   - If chunk.message.content is non-empty and first_token_time is None:
    #       set first_token_time = time.perf_counter()
    #   - Append chunk.message.content to full_text
    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.message.content != '':
            if first_token_time is None:
                first_token_time = time.perf_counter()
            full_text += chunk.message.content
    # TODO 3: Capture token_count from the final stream chunk.
    # Inside your loop from TODO 2, add:
    #   if chunk.done and chunk.eval_count:
    #       token_count = chunk.eval_count
    # Then compute tokens_per_second below.
        if chunk.done and chunk.eval_count:
            token_count = chunk.eval_count

    end = time.perf_counter()
    total_ms = (end - start) * 1000
    first_token_ms = (first_token_time - start) * 1000 if first_token_time else total_ms
    tokens_per_second = token_count / (end - start)  # replace: token_count / (end - start)

    return {
        "prompt": prompt,
        "response_text": full_text.strip(),
        "latency_first_token_ms": round(first_token_ms, 1),
        "latency_total_ms": round(total_ms, 1),
        "token_count": token_count,
        "tokens_per_second": round(tokens_per_second, 1),
    }


# TODO 4: Implement benchmark_model()
# Run run_timed_chat() for each prompt, then compute and return averaged stats.
#
# Steps:
#   1. Loop over prompts, call run_timed_chat(model, prompt), collect results in a list
#   2. Average these fields across all runs:
#        avg_latency_first_token_ms, avg_latency_total_ms, avg_tokens_per_second
#   3. Sum token_count across all runs into total_tokens
#   4. Return a dict with keys:
#        model, avg_latency_first_token_ms, avg_latency_total_ms,
#        avg_tokens_per_second, total_tokens, runs
#
# The print statements below are already provided — add your code after them.
def benchmark_model(model: str, prompts: list[str]) -> dict:
    print(f"  Benchmarking {model}...", flush=True)
    runs = []
    for prompt in prompts:
        print(f"    prompt: {prompt[:60]}", flush=True)
        result = run_timed_chat(model, prompt)
        runs.append(result)

    first_token_total = 0
    response_time_total = 0
    total_tokens = 0
    for run in runs:
        first_token_total += run["latency_first_token_ms"]
        response_time_total += run["latency_total_ms"]
        total_tokens += run["token_count"]
    
    run_count = len(prompts)

    return {
        "model": model,
        "avg_latency_first_token_ms": round(first_token_total/run_count, 1),
        "avg_latency_total_ms": round(response_time_total/run_count, 1),
        "avg_tokens_per_second": round((total_tokens / response_time_total) * 1000, 1),
        "total_tokens": total_tokens,
        "runs": runs
    }

# TODO 5: Implement print_table()
# Print a formatted ASCII table comparing all models.
#
# Columns: Model | First Token (avg ms) | Total Time (avg ms) | Tokens/sec | Tokens
#
# Steps:
#   1. Compute column widths (model name column should fit the longest name)
#   2. Print a separator line, header row, separator line
#   3. For each result dict in `results`, print one row
#   4. After the table, print the last prompt and each model's response (first 120 chars)
#
# Hint: use f-string alignment: f"{'text':<width}" (left) or f"{'text':>width}" (right)
def print_table(results: list[dict]) -> None:

    final_prompt_runs = []
    print('-' * 80)
    print(f"{'Model':^14} | First Token (avg ms) | Total Time (avg ms) | Tokens/sec | Tokens")
    print('-' * 80)
    for result in results:
        print(f"{result["model"][:13]:<14} | {result["avg_latency_first_token_ms"]:<20} | {result["avg_latency_total_ms"]:>19} | {result["avg_tokens_per_second"]:<10} | {result["total_tokens"]:<6}")
        print('-' * 80)
        final_prompt_runs.append({
            "model": result["model"],
            "response": result["runs"][-1]["response_text"]
        })
    final_prompt = results[0]["runs"][-1]["prompt"]
    print(final_prompt)
    for run in final_prompt_runs:
        print(run["model"])
        print(run["response"][:120])

def save_json(results: list[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full results saved to: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare local Ollama models on chat benchmarks"
    )
    parser.add_argument(
        "--models", nargs="+",
        help="Model names to compare (default: all local models)"
    )
    parser.add_argument(
        "--prompt",
        help="Use a single custom prompt instead of the default set"
    )
    args = parser.parse_args()

    models = args.models or list_local_models()
    if not models:
        print("No models found. Run `ollama pull llama3.1` to get started.")
        return

    prompts = [args.prompt] if args.prompt else DEFAULT_PROMPTS
    print(f"Comparing {len(models)} model(s) across {len(prompts)} prompt(s):\n")
    for m in models:
        print(f"  * {m}")
    print()

    all_results = []
    for model in models:
        result = benchmark_model(model, prompts)
        all_results.append(result)

    print_table(all_results)
    save_json(all_results, RESULTS_FILE)


if __name__ == "__main__":
    main()
