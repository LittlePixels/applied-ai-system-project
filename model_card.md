# Model Card — Game Glitch Investigator

## Limitations and Biases

The `GuesserAgent` is instructed to use binary search, but Claude sometimes deviates — choosing a number that "feels" strategic rather than the true midpoint. This means guess quality is non-deterministic and depends on how the model interprets the system prompt on a given run. The `ProposerAgent` is told to avoid "obvious" choices like the midpoint, but what counts as obvious is subjective to the model, so the secret number distribution is not truly uniform. Neither agent has memory across separate battle runs, so there is no learning over time — each battle starts from scratch regardless of past outcomes.

## Potential Misuse and Prevention

This system is a toy game, but the underlying pattern — two agents communicating in a loop with one holding hidden information — applies to higher-stakes contexts (negotiations, adversarial probing, automated social engineering). In this project, misuse is limited because both agents only operate within the number-guessing game logic and cannot act on external systems. In a real deployment, the safeguards that matter most are: constraining agent outputs to a defined schema (here, a single integer), keeping humans in the loop for consequential decisions, and rate-limiting API calls so runaway agent loops cannot accumulate large costs silently.

## What Surprised Us During Reliability Testing

The most surprising result was how often the `GuesserAgent` beats Hard difficulty even though binary search mathematically requires more steps than the attempt limit allows. Claude occasionally skips straight to a near-correct guess on the second or third attempt, seemingly because the hint messages ("Go HIGHER!" with an emoji) give it enough signal to make an educated leap rather than a strict midpoint calculation. This makes the agent look smarter than the algorithm — but it also means results are less predictable and harder to reason about.

## Collaboration with AI During This Project

**Helpful suggestion:** When writing `test_agents.py`, Claude suggested using `unittest.mock.patch("agents.client")` to intercept the module-level Anthropic client rather than patching the class constructor. This was the correct approach — patching at the point of use in the `agents` module rather than in the `anthropic` library itself — and it made all 10 agent tests work without any network calls or API keys.

**Flawed suggestion:** During the original Module 1–3 debugging, Claude (and ChatGPT) suggested fixing the inverted hint bug by swapping only the emoji strings while leaving the outcome labels (`"Too High"` / `"Too Low"`) unchanged. That looked correct on the surface — the hints displayed the right text — but the `update_score()` function keys off the outcome label, not the message string. Accepting that fix would have left the scoring logic penalizing players for correct directional guesses. The bug was only caught by tracing what downstream code consumed the `outcome` value, not just what the UI displayed.
