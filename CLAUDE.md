# Claude Rules for This Project

## Mobile / Remote Prompting

The user controls this session remotely via the Claude Code iPhone app. Follow these rules whenever you need to ask for permission, confirmation, or a decision:

### Always use `.claude/ask.sh` for yes/no confirmations

Instead of asking freeform questions, run the script:

```bash
.claude/ask.sh "Short question under 10 words?" "what you are about to do" "why you need to do it"
```

**Exit codes:**
- `0` — user said yes → proceed
- `1` — user said no → stop and acknowledge
- `2` — no response after two 20-second attempts → see below

### On exit code 2 (no response)

Do NOT proceed with the action. Output a clear message to the session that includes:
- What action was being attempted
- Why it was needed
- That it was cancelled due to no response
- An offer to continue if the user replies now

### Question format rules

- Keep questions **under 10 words** — small screen
- **Binary only** — if you have a multi-option decision, break it into yes/no sub-questions
- Put the most important word first in the question

### What requires `.claude/ask.sh` vs. what is auto-allowed

See `.claude/settings.json` for the full permission list. Any `Bash` command not in the allow list should go through `.claude/ask.sh` before running.
