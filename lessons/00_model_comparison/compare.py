# Lesson 00: Model Comparison — Basic Chat
# Goal: benchmark local Ollama models on chat speed and output quality
#       so you can pick the best model before starting the other lessons.
#
# Run with:
#   python compare.py                           # auto-discover all local models
#   python compare.py --models llama3.1 mistral
#   python compare.py --prompt "Your question here"

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


def list_local_models() -> list[str]:
    """Return names of all models currently available in Ollama."""
    response = ollama.list()
    return [m.model for m in response.models]


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

    stream = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in stream:
        if chunk.message.content:
            if first_token_time is None:
                first_token_time = time.perf_counter()
            full_text += chunk.message.content
        if chunk.done and chunk.eval_count:
            token_count = chunk.eval_count

    end = time.perf_counter()
    total_ms = (end - start) * 1000
    first_token_ms = (first_token_time - start) * 1000 if first_token_time else total_ms

    return {
        "prompt": prompt,
        "response_text": full_text.strip(),
        "latency_first_token_ms": round(first_token_ms, 1),
        "latency_total_ms": round(total_ms, 1),
        "token_count": token_count,
        "tokens_per_second": round(token_count / (end - start), 1) if token_count else 0.0,
    }


def benchmark_model(model: str, prompts: list[str]) -> dict:
    """Run all prompts against a model and return averaged stats."""
    print(f"  Benchmarking {model}...", flush=True)
    runs = []
    for prompt in prompts:
        print(f"    prompt: {prompt[:60]}", flush=True)
        result = run_timed_chat(model, prompt)
        runs.append(result)

    avg_first = sum(r["latency_first_token_ms"] for r in runs) / len(runs)
    avg_total = sum(r["latency_total_ms"] for r in runs) / len(runs)
    avg_tps = sum(r["tokens_per_second"] for r in runs) / len(runs)
    total_tokens = sum(r["token_count"] for r in runs)

    return {
        "model": model,
        "avg_latency_first_token_ms": round(avg_first, 1),
        "avg_latency_total_ms": round(avg_total, 1),
        "avg_tokens_per_second": round(avg_tps, 1),
        "total_tokens": total_tokens,
        "runs": runs,
    }


def print_table(results: list[dict]) -> None:
    """Print a formatted ASCII comparison table to stdout."""
    model_col = max(len("Model"), max(len(r["model"]) for r in results))

    header = (
        f"{'Model':<{model_col}}  "
        f"{'First Token':>14}  "
        f"{'Total Time':>12}  "
        f"{'Tokens/sec':>11}  "
        f"{'Tokens':>8}"
    )
    sep = "-" * len(header)

    print("\n" + sep)
    print(header)
    print(sep)
    for r in results:
        print(
            f"{r['model']:<{model_col}}  "
            f"{r['avg_latency_first_token_ms']:>13.1f}ms  "
            f"{r['avg_latency_total_ms']:>11.1f}ms  "
            f"{r['avg_tokens_per_second']:>11.1f}  "
            f"{r['total_tokens']:>8}"
        )
    print(sep)

    print("\n--- Sample output (last prompt) ---")
    last_prompt = results[0]["runs"][-1]["prompt"]
    print(f"Prompt: {last_prompt}\n")
    for r in results:
        preview = r["runs"][-1]["response_text"][:120].replace("\n", " ")
        print(f"[{r['model']}]\n  {preview}\n")


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
