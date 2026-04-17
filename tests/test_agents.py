"""
Tests for the two-agent system (ProposerAgent, GuesserAgent, run_agent_battle).
The Anthropic API client is mocked so these run without network access or an API key.
"""

from unittest.mock import MagicMock, call, patch

import pytest


def _mock_response(text: str) -> MagicMock:
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    return resp


# ── ProposerAgent ─────────────────────────────────────────────────────────────

class TestProposerAgent:
    def test_returns_integer_in_range(self):
        with patch("agents.client") as mock_client:
            mock_client.messages.create.return_value = _mock_response("42")
            from agents import ProposerAgent
            secret = ProposerAgent().propose(1, 100)
            assert isinstance(secret, int)
            assert 1 <= secret <= 100

    def test_fallback_when_claude_returns_garbage(self):
        """If Claude replies with non-numeric text, propose() falls back to random.randint."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.return_value = _mock_response("I cannot choose a number.")
            from agents import ProposerAgent
            secret = ProposerAgent().propose(1, 20)
            assert isinstance(secret, int)
            assert 1 <= secret <= 20

    def test_fallback_when_number_out_of_range(self):
        """If Claude returns a number outside the range, propose() falls back to random.randint."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.return_value = _mock_response("999")
            from agents import ProposerAgent
            secret = ProposerAgent().propose(1, 100)
            assert 1 <= secret <= 100


# ── GuesserAgent ──────────────────────────────────────────────────────────────

class TestGuesserAgent:
    def test_first_guess_returns_integer(self):
        with patch("agents.client") as mock_client:
            mock_client.messages.create.return_value = _mock_response("50")
            from agents import GuesserAgent
            g = GuesserAgent(1, 100).guess()
            assert g == 50

    def test_hint_is_included_in_followup_message(self):
        """The hint from check_guess must appear in the next user message to the GuesserAgent."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.side_effect = [
                _mock_response("50"),
                _mock_response("75"),
            ]
            from agents import GuesserAgent
            guesser = GuesserAgent(1, 100)
            guesser.guess()
            guesser.guess("📈 Go HIGHER!")

            second_call_messages = mock_client.messages.create.call_args_list[1]
            messages_arg = second_call_messages.kwargs["messages"]
            user_texts = [m["content"] for m in messages_arg if m["role"] == "user"]
            assert any("HIGHER" in t for t in user_texts)

    def test_conversation_history_grows_per_round(self):
        """Each guess/reply pair must be appended to the conversation history."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.side_effect = [
                _mock_response("50"),
                _mock_response("75"),
                _mock_response("87"),
            ]
            from agents import GuesserAgent
            guesser = GuesserAgent(1, 100)
            guesser.guess()
            guesser.guess("📈 Go HIGHER!")
            guesser.guess("📉 Go LOWER!")
            # 3 user messages + 3 assistant replies = 6 entries
            assert len(guesser._history) == 6

    def test_fallback_extracts_number_from_verbose_reply(self):
        """If Claude replies with words around the number, re.findall extracts it."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.return_value = _mock_response("My guess is 63.")
            from agents import GuesserAgent
            assert GuesserAgent(1, 100).guess() == 63


# ── run_agent_battle orchestrator ─────────────────────────────────────────────

class TestRunAgentBattle:
    def test_guesser_wins_on_first_try(self):
        """Battle should end immediately when guesser's first guess matches the secret."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.side_effect = [
                _mock_response("42"),  # Proposer picks 42
                _mock_response("42"),  # Guesser guesses 42 → Win
            ]
            from agents import run_agent_battle
            result = run_agent_battle("Normal")

        assert result["secret"] == 42
        assert result["winner"] == "Guesser"
        assert len(result["rounds"]) == 1
        assert result["rounds"][0]["outcome"] == "Win"

    def test_proposer_wins_when_attempts_exhausted(self):
        """Proposer wins when guesser never finds the number within the attempt limit."""
        # Easy: limit=10, secret=15; guesser always guesses 1 (wrong)
        responses = [_mock_response("15")]  # Proposer picks 15
        responses += [_mock_response("1")] * 10  # Guesser wrong every time
        with patch("agents.client") as mock_client:
            mock_client.messages.create.side_effect = responses
            from agents import run_agent_battle
            result = run_agent_battle("Easy")

        assert result["winner"] == "Proposer"
        assert len(result["rounds"]) == 10  # Easy attempt limit

    def test_result_structure(self):
        """Return value must contain all expected keys."""
        with patch("agents.client") as mock_client:
            mock_client.messages.create.side_effect = [
                _mock_response("10"),
                _mock_response("10"),
            ]
            from agents import run_agent_battle
            result = run_agent_battle("Easy")

        assert {"secret", "low", "high", "rounds", "winner"} <= result.keys()
        for r in result["rounds"]:
            assert {"attempt", "guess", "outcome", "message"} <= r.keys()
