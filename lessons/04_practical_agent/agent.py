# Lesson 4: Practical Agent
# Goal: implement three real tools and wire them into a working agent.
#
# The agent loop below is complete — your job is the 6 TODOs above it.
# Read README.md first.

import ast
import operator
import os
import ollama

MODEL = "llama3.1"
MAX_ITERATIONS = 10

# ---------------------------------------------------------------------------
# TODO 1: implement read_file(path: str) -> str
# Read the file at `path` and return its contents as a string.
# If the file doesn't exist, return an error string instead of raising.
# ---------------------------------------------------------------------------
def read_file(path: str) -> str:
    pass  # replace this


# ---------------------------------------------------------------------------
# TODO 2: implement list_files(directory: str) -> str
# List the files in `directory`, one filename per line, returned as a string.
# If the directory doesn't exist, return an error string.
# ---------------------------------------------------------------------------
def list_files(directory: str) -> str:
    pass  # replace this


# ---------------------------------------------------------------------------
# TODO 3: implement calculate(expression: str) -> str
# Safely evaluate a math expression and return the result as a string.
# Use the ast-based approach from README.md — do NOT use eval() directly.
# If the expression is invalid, return an error string.
# ---------------------------------------------------------------------------
def calculate(expression: str) -> str:
    pass  # replace this


# ---------------------------------------------------------------------------
# TODO 4: write tool schemas for all three functions.
# Follow the same format as Lesson 2/3.
# read_file    → one required string param: "path"
# list_files   → one required string param: "directory"
# calculate    → one required string param: "expression"
# ---------------------------------------------------------------------------

read_file_schema = {}      # replace this
list_files_schema = {}     # replace this
calculate_schema = {}      # replace this

# ---------------------------------------------------------------------------
# TODO 5: register your tools
# Add all three functions to TOOL_REGISTRY and all three schemas to TOOLS.
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict = {}   # replace this

TOOLS: list = []           # replace this


# ---------------------------------------------------------------------------
# Agent loop — already complete, do not modify
# ---------------------------------------------------------------------------

def run_agent(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]

    for iteration in range(MAX_ITERATIONS):
        print(f"\n--- iteration {iteration + 1} ---")
        response = ollama.chat(model=MODEL, messages=messages, tools=TOOLS)
        messages.append(response.message)

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                name = tool_call.function.name
                args = tool_call.function.arguments
                fn = TOOL_REGISTRY.get(name)
                if fn is None:
                    result = f"Error: unknown tool '{name}'"
                else:
                    try:
                        result = fn(**args)
                    except Exception as e:
                        result = f"Error running {name}: {e}"
                print(f"  tool {name}({args}) → {str(result)[:120]}")
                messages.append({"role": "tool", "content": str(result)})
        else:
            print("  model gave final answer")
            break
    else:
        return "Agent hit iteration limit without a final answer."

    return response.message.content


# ---------------------------------------------------------------------------
# TODO 6: write a prompt below that makes the agent use at least 2 tools.
# Run this file and watch the loop work end-to-end.
# ---------------------------------------------------------------------------

prompt = "TODO: write your prompt here"

answer = run_agent(prompt)
print(f"\n=== Final answer ===\n{answer}")
