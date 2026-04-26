import random
import re
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv(Path(__file__).parent / ".env")

client = anthropic.Anthropic()

PROPOSER_SYSTEM = (
    "You are the Proposer in a number guessing game. "
    "Your job is to choose a secret number that will be tricky for the Guesser to find — "
    "avoid obvious choices like the exact midpoint of the range. "
    "Respond with ONLY the integer — no words, no punctuation."
)

GUESSER_SYSTEM = (
    "You are the Guesser in a number guessing game. "
    "Use binary search: after each hint narrow your range and pick the new midpoint. "
    "Respond with ONLY the integer — no words, no punctuation."
)


class ProposerAgent:
    """Claude agent that picks a secret number for the Guesser to find."""

    def propose(self, low: int, high: int) -> int:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=20,
            system=PROPOSER_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": f"Choose a secret number between {low} and {high} inclusive.",
                }
            ],
        )
        text = response.content[0].text.strip()
        try:
            num = int(text)
            if low <= num <= high:
                return num
        except ValueError:
            pass
        return random.randint(low, high)


class GuesserAgent:
    """Claude agent that guesses the secret number using hints from the game."""

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high
        self._history: list[dict] = []

    def guess(self, hint: str | None = None) -> int:
        if hint is None:
            user_msg = (
                f"The secret number is between {self.low} and {self.high}. "
                "Make your first guess."
            )
        else:
            user_msg = f"Hint: {hint}. Make your next guess."

        self._history.append({"role": "user", "content": user_msg})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=20,
            system=GUESSER_SYSTEM,
            messages=self._history,
        )
        reply = response.content[0].text.strip()
        self._history.append({"role": "assistant", "content": reply})

        try:
            return int(reply)
        except ValueError:
            nums = re.findall(r"\d+", reply)
            if nums:
                return int(nums[0])
            return (self.low + self.high) // 2


def run_agent_battle(difficulty: str) -> dict:
    """
    Run a full Proposer-vs-Guesser battle and return the play-by-play.

    Returns:
        {
          "secret": int,
          "low": int,
          "high": int,
          "rounds": [{"attempt": int, "guess": int, "outcome": str, "message": str}],
          "winner": "Guesser" | "Proposer",
        }
    """
    from logic_utils import check_guess, get_attempt_limit, get_range_for_difficulty

    low, high = get_range_for_difficulty(difficulty)
    attempt_limit = get_attempt_limit(difficulty)

    proposer = ProposerAgent()
    guesser = GuesserAgent(low, high)

    secret = proposer.propose(low, high)
    rounds = []
    hint = None

    for attempt in range(1, attempt_limit + 1):
        g = guesser.guess(hint)
        outcome, message = check_guess(g, secret)
        rounds.append(
            {"attempt": attempt, "guess": g, "outcome": outcome, "message": message}
        )
        if outcome == "Win":
            return {
                "secret": secret,
                "low": low,
                "high": high,
                "rounds": rounds,
                "winner": "Guesser",
            }
        hint = message

    return {
        "secret": secret,
        "low": low,
        "high": high,
        "rounds": rounds,
        "winner": "Proposer",
    }
