# AI Interactions Log

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked the agent to complete the model card and all optional recommender
extensions while preserving the working CLI and tests.

**Prompts used:**

- "Add five advanced song attributes and make the scoring logic use them."
- "Create multiple scoring modes that can be selected from the CLI."
- "Add a diversity penalty for repeated artists or genres."
- "Display scores and reasons in a readable terminal table."

**What did the agent generate or change?**

The agent expanded `songs.csv`, added three scoring modes, implemented greedy
diversity reranking, built an ASCII table, completed the model card, and added
tests. It also ran the CLI in each mode and validated all CSV value ranges.

**What did you verify or fix manually?**

I verified that all 18 songs load, numerical columns have correct types, scores
remain deterministic, and all tests pass. I checked that diversity changes the
lofi ordering without removing relevant songs. I also reviewed the model card
to ensure its claims match observed output.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

A simple **Strategy pattern**.

**How did AI help you brainstorm or implement it?**

AI suggested keeping named weight dictionaries instead of copying the scoring
function three times. This makes each mode a replaceable scoring strategy.

**How does the pattern appear in your final code?**

`SCORING_MODES` in `src/recommender.py` stores the balanced, genre-first, and
energy-focused strategies. `get_scoring_weights()` selects one, and
`recommend_songs()` applies it. `python -m src.main --mode ...` lets the user
switch modes.
