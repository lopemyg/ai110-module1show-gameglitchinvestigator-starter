# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

"Plan and implement a High Score tracker that saves the player's best score to a file so it persists across sessions. Show it in the sidebar and display a 'New high score!' message on a win."

**What did the agent do?**

1. Added `load_high_score()` and `save_high_score(score)` to `logic_utils.py` — reads/writes `highscore.json` using the `json` and `os` standard library modules. `save_high_score` only overwrites the file if the new score beats the current best.
2. Updated the import line in `app.py` to include the two new functions.
3. Added `st.sidebar.metric("🏆 High Score", load_high_score())` to the sidebar so the best score is visible before every game.
4. Called `save_high_score()` inside the win branch in `app.py`, then read the persisted value back to decide whether to show "New high score!" or display the previous best.
5. Ran a smoke test in the terminal to confirm that repeated saves only update the file when the new score is strictly higher.

**What did you have to verify or fix manually?**

The agent's first draft of the win message read back the high score *before* calling `save_high_score`, so a new record would always show the old best rather than "New high score!". The order needed to be: save first, then read back to compare — which I caught by reading the diff carefully and correcting the call order before committing.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
