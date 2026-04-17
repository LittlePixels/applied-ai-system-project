# 🎮 Game Glitch Investigator — Applied AI System Project

## Original Project (Modules 1–3): Game Glitch Investigator

The original project was **Game Glitch Investigator: The Impossible Guesser**, a Streamlit number-guessing game that was intentionally shipped with seven hidden bugs — inverted hint messages, wrong difficulty ranges, string-vs-integer comparison errors, and broken session state. The goal was to use AI tools (Claude, ChatGPT) as debugging teammates to identify and fix each bug, then verify the fixes using pytest. By the end, students had a fully working game and a hands-on understanding of how AI can assist — and sometimes mislead — during real debugging work.

---

## Title and Summary

**Game Glitch Investigator** is a Streamlit-based number guessing game extended with an **agentic AI workflow**: two Claude-powered agents play the game autonomously — one proposes a secret number, the other guesses it using hints and binary search reasoning. This matters because it demonstrates how AI agents can be composed into a multi-step pipeline where outputs from one agent become inputs to another, mirroring real-world agentic system design.

---

## Architecture Overview

The system has three layers:

| Layer | Files | Role |
| --- | --- | --- |
| Game Logic | `logic_utils.py` | Pure functions: generate secret, validate guess, check outcome, update score |
| UI | `app.py` | Two Streamlit tabs — Human Game and Agent Battle |
| Agents | `agents.py` | `ProposerAgent` picks a secret; `GuesserAgent` narrows it down via conversation history |

**Data flow:**

```text
[Human Game Tab]
  User input → parse_guess() → check_guess() → hint + score → win/loss display

[Agent Battle Tab]
  ProposerAgent (Claude) → picks secret number
        ↓
  GuesserAgent (Claude) → makes a guess
        ↓
  check_guess() → returns hint ("Go HIGHER!" / "Go LOWER!")
        ↓
  hint fed back into GuesserAgent conversation history
        ↓
  loop until Win or attempts exhausted → play-by-play displayed
```

See [`assets/short_diagram.md`](assets/short_diagram.md) for the full Mermaid flowchart.

---

## Setup Instructions

**Prerequisites:** Python 3.11+, an Anthropic API key

```bash
# 1. Clone the repo
git clone https://github.com/LittlePixels/applied-ai-system-project
cd applied-ai-system-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here   # macOS / Linux
set ANTHROPIC_API_KEY=your_key_here      # Windows CMD

# 4. Run the app
streamlit run app.py

# 5. (Optional) Run unit tests
pytest
```

Open your browser to `http://localhost:8501`. Use the **👤 Human Game** tab to play manually, or switch to **🤖 Agent Battle** to watch the agents compete.

---

## Sample Interactions

### 1 — Human Game (Normal difficulty, range 1–100)

| Attempt | Guess | Result |
| --- | --- | --- |
| 1 | 50 | 📉 Go LOWER! |
| 2 | 25 | 📈 Go HIGHER! |
| 3 | 37 | 📉 Go LOWER! |
| 4 | 31 | 🎉 Correct! |

> **Output:** "You won! The secret was 31. Final score: 60"  
> Balloons animation fires. 🎈

---

### 2 — Agent Battle (Easy difficulty, range 1–20, 10 attempts)

```text
Secret number chosen by Proposer: 14

Attempt 1 — Guesser guesses 10 → 🔼 Go HIGHER!
Attempt 2 — Guesser guesses 15 → 🔽 Go LOWER!
Attempt 3 — Guesser guesses 12 → 🔼 Go HIGHER!
Attempt 4 — Guesser guesses 13 → 🔼 Go HIGHER!
Attempt 5 — Guesser guesses 14 → ✅ 🎉 Correct!

🎉 Guesser Agent won in 5 attempt(s)!
```

---

### 3 — Agent Battle (Hard difficulty, range 1–200, 5 attempts)

```text
Secret number chosen by Proposer: 173

Attempt 1 — Guesser guesses 100 → 🔼 Go HIGHER!
Attempt 2 — Guesser guesses 150 → 🔼 Go HIGHER!
Attempt 3 — Guesser guesses 175 → 🔽 Go LOWER!
Attempt 4 — Guesser guesses 162 → 🔼 Go HIGHER!
Attempt 5 — Guesser guesses 168 → 🔼 Go HIGHER!

💀 Proposer Agent wins! Guesser couldn't crack it in 5 attempts.
```

---

## Design Decisions

**Why two separate agent classes?**  
Separating `ProposerAgent` and `GuesserAgent` into distinct classes mirrors real agentic system design — each agent has a single responsibility, its own system prompt, and its own conversation history. This makes them independently testable and swappable.

**Why keep `logic_utils.py` unchanged?**  
The game logic functions (`check_guess`, `parse_guess`, etc.) are pure and already tested. Reusing them inside `run_agent_battle()` meant the agent workflow got the same validated logic as the human game — no duplication, no drift.

**Why Streamlit tabs instead of a separate page?**  
A second tab keeps the difficulty selector shared between both modes. The user can switch modes without losing their settings, and it avoids `st.stop()` from blocking the agent tab from rendering.

**Trade-offs:**

- The `ProposerAgent` calls the Claude API just to pick a number, which could be done with `random.randint`. The cost is a small latency hit; the benefit is demonstrating a full agentic pipeline where both sides are AI-driven.
- The `GuesserAgent` passes full conversation history on every turn. This keeps the agent's reasoning coherent but means token usage grows with each guess.

---

## Testing Summary

The project has **15 automated tests** across two files, all passing (`pytest tests/ -v`).

| File | Tests | What is covered |
| --- | --- | --- |
| `tests/test_game_logic.py` | 5 | `check_guess` outcomes and hint direction correctness |
| `tests/test_agents.py` | 10 | `ProposerAgent`, `GuesserAgent`, and `run_agent_battle` orchestration |

**Agent tests use mocks** — `unittest.mock.patch` replaces the live Anthropic API client so tests run instantly with no network access or API key. This lets the tests verify the logic (conversation history growth, fallback on bad output, battle loop termination) without depending on external services.

**What worked:**

- All 5 game-logic tests pass, covering win, too-high, too-low, and both hint directions.
- `ProposerAgent` correctly falls back to `random.randint` when Claude returns non-numeric or out-of-range text.
- `GuesserAgent` appends each guess/reply pair to its conversation history and injects hints into the next user message.
- The battle orchestrator correctly declares `"Guesser"` when a win occurs and `"Proposer"` when attempts run out.

**What didn't work at first:**

- The original `test_game_logic.py` compared `check_guess()` return values to plain strings (`== "Win"`), but the function returns a tuple. Tests failed until the assertions were updated to unpack the tuple.
- On Hard difficulty (range 1–200, 5 attempts), the `GuesserAgent` loses more often than it wins — binary search needs ~8 steps for a 200-wide range. This is by design: Hard is meant to favor the Proposer.

**What was learned:**

Bugs in tests are as dangerous as bugs in code — a passing test with the wrong assertion gives false confidence. Mocking the API client was essential: it made the agent tests deterministic, fast, and repeatable without burning API credits on every `pytest` run.

---

## Reflection

This project shifted how I think about AI from a tool that answers questions to a system component that can hold state, reason across turns, and collaborate with other agents. The `GuesserAgent` doesn't just call Claude once — it maintains a conversation, learns from each hint, and adjusts its strategy. That feedback loop between agent output and game logic is the same pattern used in production AI systems.

The debugging work in Modules 1–3 was equally important: it taught me to read AI suggestions critically. When Claude or ChatGPT suggested a fix, I learned to trace the logic myself — check what `outcome` drives downstream, not just what the hint message says — before accepting the change. AI accelerates development but doesn't replace the developer's need to understand what the code is actually doing.

---

> See [model_card.md](model_card.md) for the full Responsible AI reflection — limitations, misuse prevention, reliability surprises, and AI collaboration notes.
