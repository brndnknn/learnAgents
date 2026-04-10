# Lesson 1: Basic Chat
# Goal: make a working chat call to a local Ollama model.
#
# Read README.md first, then fill in the 4 TODOs below.

# TODO 1: import the ollama library
import ollama

MODEL = "llama3.1"

# TODO 2: Build the messages list for the conversation.
# Hint: ollama expects a list of dicts with "role" and "content" keys.
#       Include at least a system message and a user message.
messages = [
    {"role": "system", "content": "You are a helpful but sarcastic assistant. Answer questions correctly with helpful details as well as a healthy heap of snark and salty language."},
    {"role": "user", "content": "Why is the sky blue?"}
]  # replace this

# TODO 3: Send the messages to the model and store the response.
response = ollama.chat(model=MODEL, messages=messages)

# TODO 4: Print the assistant's reply.
# Hint: it's nested a couple of levels inside the response object.
print("=== Assistant reply ===")
# your print here
print(response.message.content)

# This line is already done — it lets you inspect the full response object
print("\n--- raw response ---")
print(response)
