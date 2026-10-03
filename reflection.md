# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it loaded but had problems right away. The attempts counter was already at 1 before I made a single guess, so "Attempts left" was always one short. On my second guess — and every even-numbered attempt after — the hint direction was wrong: I could guess too low and be told to go lower, or even guess the exact number and not win. Hard difficulty also used a range of 1–50, which is actually a smaller target space than Normal's 1–100, making it easier to guess despite having fewer attempts.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Start a fresh game (no guesses yet) | Attempts counter starts at 0; first guess counts as attempt #1 | Counter initializes to 1, so the first guess immediately registers as attempt #2 and "Attempts left" is off by one the entire game | None — silent off-by-one | `app.py:96`, `st.session_state.attempts = 1` |
| Guess 7 when secret is 42, on attempt #2 (even) | Hint says "Go Higher" (7 < 42) | Hint says "Go Higher" but for the wrong reason — `secret` is cast to the string `"42"`, so the code compares `int(7) > str("42")`, hits a `TypeError`, then falls back to `"7" > "42"` which is `True` lexicographically, accidentally giving the right answer by coincidence; guessing e.g. 50 when secret is 9 on an even attempt shows "Go Lower" incorrectly | None — `except TypeError` silently swallows the error | `app.py:158–161`, `check_guess` function (`app.py:32–47`) |
| Select "Hard" difficulty, then play | Harder range than Normal (more numbers = harder to guess) | Range is 1–50, which is a *smaller* space than Normal's 1–100; the info banner also always reads "1 to 100" regardless of difficulty | None | `app.py:9–10`, `get_range_for_difficulty`; info string hardcoded at `app.py:110` |
| Guess too high on an even-numbered attempt | Score goes down (wrong guess = penalty) | Score goes *up* by 5 — `update_score` rewards "Too High" outcomes on even attempts | None — score silently increases for a wrong guess | `app.py:57–60`, `update_score` function |

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) as my AI coding assistant throughout this project, working in its chat and agent modes directly inside VS Code.

**Suggestion I accepted — refactoring `check_guess` into `logic_utils.py` with a pure int comparison:**
The AI suggested moving all game logic functions out of `app.py` into `logic_utils.py` and rewriting `check_guess` to accept only `int` arguments, removing the `except TypeError` fallback entirely. This was correct: the root cause of the flipped hints was that `app.py` deliberately cast `secret` to a string on even attempts, which forced `check_guess` into a broken fallback path. By making `check_guess` type-safe and never passing a string, the bug cannot happen at all — not just worked around. I verified it by running `python3 -c "from logic_utils import check_guess; print(check_guess(50, 9))"` and confirming the output was `('Too High', ...)`, then confirmed the same case (`guess=50, secret=9`) in the live game showed the correct hint.

**Suggestion I did not accept as written — adding a +5 "close guess" bonus in `update_score`:**
When I asked the AI to fix the even-attempt score bug (wrong guesses were rewarding +5 points), it proposed replacing the reward with a tiered system: guesses within 10 of the secret would lose only 2 points instead of 5, and guesses far away would lose 10. The idea was to make scoring feel more encouraging. I rejected it because it was out of scope — the task was to fix a bug, not redesign the scoring system — and it added complexity that wasn't in the original spec. I kept the simpler fix: any wrong guess (Too High or Too Low) always subtracts 5 points. I verified by running `pytest` and checking that `test_score_wrong_guess_never_rewards` passed, confirming both outcomes always decrease the score.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when two conditions were both true: a pytest test specifically targeting that bug passed, and I could reproduce the formerly broken scenario in the live Streamlit app and see correct behavior.

For the hint-direction bug, I wrote `test_check_guess_always_numeric_high` which calls `check_guess(50, 9)` — the exact case that previously returned "Too Low" due to lexicographic comparison of `"50" < "9"`. After the fix the test passes, confirming the function now always does numeric comparison. I also ran the app, opened the Developer Debug Info expander to see the secret, then guessed a number with a smaller leading digit than the secret on an even attempt (the formerly broken case) and confirmed the hint was correct.

For the attempts off-by-one bug, `test_score_win_on_first_attempt` asserts that `update_score(0, "Win", 1)` returns `90` (100 − 10×1). Before the fix, the first guess was counted as attempt 2, so the same win would have scored 80. The test pinning attempt 1 → 90 points locks in the corrected behavior.

The AI helped me design the regression tests by suggesting I write cases that directly replicate the broken input — not just generic "too high / too low" cases, but the specific numeric combinations that exposed the lexicographic flaw (e.g., a guess whose leading digit is smaller than the secret's leading digit). That made the tests actually catch the bug rather than pass by coincidence.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
