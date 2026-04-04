# Lesson 1: Basic Chat
# Goal: make a working chat call to a local Ollama model.
#
# Read README.md first, then fill in the 4 TODOs below.

# TODO 1: import the ollama library


MODEL = "llama3.1"

# TODO 2: build the messages list
# It needs at least two messages:
#   - a "system" message setting the model's behavior
#   - a "user" message asking something (e.g. "What is 2 + 2?")
messages = []  # replace this

# TODO 3: call ollama.chat() with MODEL and messages
# Store the return value in a variable called `response`


# TODO 4: print the assistant's reply
# The reply is at response.message.content
print("=== Assistant reply ===")
# your print here

# This line is already done — it lets you inspect the full response object
print("\n--- raw response ---")
print(response)
