# Lesson 1: Basic Chat

## What you'll learn
How to send a message to a local Ollama model and read the response.

## Prereqs

1. Install Ollama: https://ollama.com/download
2. Pull a model that supports tool calling:
   ```
   ollama pull llama3.1
   ```
3. Install Python deps from the repo root:
   ```
   pip install -r requirements.txt
   ```

---

## Key concept: `ollama.chat()`

`ollama.chat()` sends a conversation to the model and returns its reply.
It takes two required arguments:

```python
response = ollama.chat(
    model="llama3.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": "What is 2 + 2?"},
    ]
)
```

**Message roles:**
| Role       | Purpose                                      |
|------------|----------------------------------------------|
| `system`   | Sets the model's behavior/persona            |
| `user`     | A message from the human                     |
| `assistant`| A reply from the model (for conversation history) |

**The response object:**
The reply lives at `response.message.content`. The raw object also has
fields like `model`, `done`, and timing info — `chat.py` prints the raw
response so you can explore it.

---

## Your task

Open `chat.py`. There are 4 TODOs. Fill them in so the script:

1. Imports the `ollama` library
2. Builds a `messages` list with a system prompt and a user question
3. Calls `ollama.chat()` to get a response
4. Prints the assistant's reply

**Expected output** (content will vary):
```
=== Assistant reply ===
2 + 2 equals 4.

--- raw response ---
ChatResponse(model='llama3.1', ...)
```

Run it with:
```
python lessons/01_basic_chat/chat.py
```
