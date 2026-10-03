import json
import os

HIGHSCORE_FILE = "highscore.json"


def load_high_score() -> int:
    """Return the saved high score, or 0 if none exists yet."""
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    try:
        with open(HIGHSCORE_FILE) as f:
            data = json.load(f)
        return int(data.get("high_score", 0))
    except Exception:
        return 0


def save_high_score(score: int) -> None:
    """Persist score to disk if it beats the current high score."""
    current = load_high_score()
    if score > current:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 1000
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Refactored into logic_utils.py using agent mode. AI correctly identified
    # that passing secret as a plain int (never str) eliminates the TypeError fallback
    # that caused lexicographic comparison and flipped hints on even attempts.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📈 Go LOWER!"
    return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Removed the even-attempt +5 reward for wrong guesses. AI suggested keeping
    # a small bonus for "close" guesses, but that was out of scope — wrong guesses
    # should always cost points, so both Too High and Too Low now subtract 5.
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
