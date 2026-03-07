from logic_utils import check_guess

def test_winning_guess():
    # Fix 8: check_guess returns a tuple (outcome, message); original tests compared the whole tuple to a string
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Fix 8: unpacked tuple before asserting
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # Fix 8: unpacked tuple before asserting
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_direction_too_high():
    # Bug: hint used to say "Go HIGHER!" when guess was too high.
    # When guess > secret, the message must tell the player to go LOWER.
    outcome, message = check_guess(80, 42)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_hint_direction_too_low():
    # Bug: hint used to say "Go LOWER!" when guess was too low.
    # When guess < secret, the message must tell the player to go HIGHER.
    outcome, message = check_guess(10, 42)
    assert outcome == "Too Low"
    assert "HIGHER" in message
