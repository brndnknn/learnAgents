# Lesson 00: Model Comparison — Basic Chat

## What you'll learn
How to benchmark local Ollama models on speed and output quality so you can
choose which model to use for the rest of the lessons.

## Prereqs

1. Install Ollama: https://ollama.com/download
2. Pull at least two models to compare:
   ```
   ollama pull llama3.1
   ollama pull llama3.2
   ```
3. Install Python deps from the repo root:
   ```
   pip install -r requirements.txt
   ```

---

## Just want to run it?

Use the fully working tool:
```
python lessons/00_model_comparison/compare.py
```

Options:
```
python compare.py --models llama3.1 mistral        # compare specific models
python compare.py --prompt "What is entropy?"      # use a custom prompt
```

Output: a terminal table + `results.json` in this directory.

---

## Key concepts

### Streaming inference
Instead of waiting for the full response, `ollama.chat(stream=True)` returns
chunks as they are generated. This lets you measure **time-to-first-token** —
how long until the model starts responding — separately from total latency.

```python
stream = ollama.chat(model=model, messages=messages, stream=True)
for chunk in stream:
    print(chunk.message.content, end="", flush=True)
```

The final chunk has `chunk.done == True` and `chunk.eval_count` (token count).

### Metrics
| Metric | What it tells you |
|---|---|
| First token latency | How quickly the model "wakes up" — important for interactive use |
| Total latency | Total wall-clock time for the full response |
| Tokens/sec | Generation speed — higher is better |
| Token count | How verbose the model is for a given prompt |

---

## Your task (lesson.py)

Open `lesson.py`. There are 5 TODOs:

1. **TODO 1** — Call `ollama.list()` and return model names
2. **TODO 2** — Set up streaming and capture the first-token timestamp
3. **TODO 3** — Read `eval_count` from the final chunk and compute tokens/sec
4. **TODO 4** — Average stats across multiple prompt runs
5. **TODO 5** — Format and print the ASCII comparison table

Run it with:
```
python lessons/00_model_comparison/lesson.py
```

**Expected output:**
```
Comparing 2 model(s) across 3 prompt(s):

  * llama3.1
  * llama3.2

  Benchmarking llama3.1...
    prompt: What is 17 * 23?
    ...

-------------------------------------------------------------
Model       First Token    Total Time   Tokens/sec    Tokens
-------------------------------------------------------------
llama3.1        412.3ms      1823.4ms         38.2        70
llama3.2        287.1ms      1102.6ms         54.9        60
-------------------------------------------------------------

--- Sample output (last prompt) ---
Prompt: Explain async/await in Python in 2 sentences.

[llama3.1]
  Async/await is a syntax for writing asynchronous code...

[llama3.2]
  Async/await allows Python to run concurrent tasks...

Full results saved to: .../results.json
```
