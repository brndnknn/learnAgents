# Lesson 05: Model Comparison — Agent Tasks (Capstone)

## What you'll learn
How to systematically compare local Ollama models on real agentic tasks:
tool calling accuracy, multi-step reasoning, and latency under a full
agent loop. This builds directly on the patterns from lessons 2–4.

## Prereqs

1. Complete lessons 01–04 (or at least skim them)
2. Have at least two Ollama models pulled:
   ```
   ollama pull llama3.1
   ollama pull llama3.2
   ```
3. `pip install -r requirements.txt` from the repo root

---

## Just want to run it?

Use the fully working tool:
```
python lessons/05_model_comparison/compare.py
```

Options:
```
python compare.py --models llama3.1 mistral    # compare specific models
python compare.py --task math                  # run only the math task
```

Output: terminal table with accuracy + latency, plus `results.json`.

---

## Key concepts

### Agent loop (recap from lesson 03)
The model is given tools and runs in a loop: call → check for tool use →
dispatch tools → call again → repeat until a final text answer.

```
User prompt
    ↓
ollama.chat(tools=TOOLS)
    ↓
model wants to call a tool?  →  YES  →  dispatch → append result → loop
    ↓ NO
final answer
```

### Why agent comparison is harder than chat comparison
- A slow model that always calls the right tool may be better than a fast
  model that skips tool calls and guesses.
- **Accuracy** matters: does the model actually use the tool and return the
  correct answer?
- **Iterations** tells you if a model is confused (many loops) or decisive.

### Agent tasks in this lesson

| Task | What it tests |
|---|---|
| `math` | Does the model call `calculate` instead of computing in its head? |
| `file_read` | Does the model call `read_file` with the correct path? |
| `multi_step` | Does the model chain a tool call + reasoning correctly? |

---

## Your task (lesson.py)

Open `lesson.py`. There are 5 TODOs:

1. **TODO 1** — Implement `run_agent_task()`: the full agent loop
2. **TODO 2** — Inside the loop: dispatch tool calls via `TOOL_REGISTRY`
3. **TODO 3** — Implement `score_task()`: keyword match on the response
4. **TODO 4** — Implement `benchmark_agent()`: aggregate stats across tasks
5. **TODO 5** — Implement `print_table()`: ASCII table with accuracy column

Run it with:
```
python lessons/05_model_comparison/lesson.py
```

**Expected output:**
```
Comparing 2 model(s) across 3 agent task(s):

  * llama3.1
  * llama3.2

  Benchmarking llama3.1...
    task: Single tool call — math
    task: Single tool call — file I/O
    task: Multi-step reasoning with tool call
  ...

------------------------------------------------------------
Model       Avg Latency   Avg Iters   Tool Calls   Accuracy
------------------------------------------------------------
llama3.1       1823.4ms         1.7            3        3/3
llama3.2       1102.6ms         1.3            3        3/3
------------------------------------------------------------

--- Per-task accuracy ---
  math                  [llama3.1: PASS]  [llama3.2: PASS]
  file_read             [llama3.1: PASS]  [llama3.2: PASS]
  multi_step            [llama3.1: PASS]  [llama3.2: FAIL]

Full results saved to: .../results.json
```
