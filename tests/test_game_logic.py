from logic_utils import check_guess, parse_guess, update_score


# --- existing tests (fixed to unpack the (outcome, message) tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- regression: even-attempt string-conversion bug ---
# Before the fix, secret was cast to str on even attempts, causing lexicographic
# comparison. E.g. str("9") vs int(50): "50" > "9" is False, so 50 was reported
# as "Too Low" when it should be "Too High".

def test_check_guess_always_numeric_high():
    # 50 is greater than 9 — must say Too High regardless of attempt parity
    outcome, _ = check_guess(50, 9)
    assert outcome == "Too High"

def test_check_guess_always_numeric_low():
    # 7 is less than 42 — must say Too Low
    outcome, _ = check_guess(7, 42)
    assert outcome == "Too Low"

def test_check_guess_secret_stays_int():
    # Passing an int secret should never raise TypeError
    outcome, message = check_guess(99, 100)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# --- regression: attempts off-by-one / score formula bug ---
# Before the fix, update_score used attempt_number + 1, and attempts started at 1,
# so a win on the first real guess was scored as if it were attempt 3.
# Now attempts start at 0, increment before scoring, so first win = attempt 1.

def test_score_win_on_first_attempt():
    # attempt_number=1 → points = 100 - 10*1 = 90
    new_score = update_score(0, "Win", 1)
    assert new_score == 90

def test_score_wrong_guess_never_rewards():
    # Too High and Too Low should always subtract, never add
    score_after_high = update_score(50, "Too High", 2)
    score_after_low = update_score(50, "Too Low", 2)
    assert score_after_high == 45
    assert score_after_low == 45
