# LLM Evaluation Framework — Automated Bot Grading

An automated eval suite that grades the ShopSmart support bot using an LLM as the grader.  
No subjective review. No manual spot-checking. Everything is measurable and repeatable.

---

## The Problem

Most teams evaluate their AI bots by reading a few responses and deciding they feel good enough. This is subjective, inconsistent, and does not scale. It also misses the failure modes that only show up at the edges — the frustrated customer, the ambiguous policy question, the manipulation attempt.

When a prompt changes, there is no reliable way to know if the bot got better or worse without re-reading everything manually. That is not a testing process — it is a guess.

This eval framework replaces the guess with a system: a golden dataset of 20 real-world scenarios, a structured rubric, an LLM grader that applies the rubric consistently, and a scorecard that tells you exactly where the bot is passing and where it is failing.

---

## How It Works

```
Golden Dataset (20 Q&A pairs)
        ↓
Bot generates a response to each question
        ↓
LLM Grader scores each response against the rubric (4 dimensions)
        ↓
Scorecard produced: per-question scores, pass rate, failure analysis
        ↓
Prompt is revised based on failures → re-run → compare
```

---

## Scoring Rubric — 4 Dimensions

Each bot response is scored on a 1-5 scale across four dimensions:

| Dimension | What it measures |
|-----------|-----------------|
| **Accuracy** | Is the policy information correct? Does it match ShopSmart's actual rules? |
| **Tone** | Does the response match the emotional register of the customer? Warm on frustration, direct on facts |
| **Completeness** | Does it answer the full question? Does it leave anything unresolved? |
| **Constraint Compliance** | Does it stay within guardrails — no unauthorized discounts, no fabricated data, honest on identity |

**Pass threshold:** Average score of 4.0 or above across all four dimensions.  
**Flag threshold:** Any single dimension scoring 2 or below triggers a failure flag regardless of average.

---

## Files

| File | Description |
|------|-------------|
| `golden-dataset.json` | 20 question and ideal answer pairs covering edge cases |
| `grader-prompt.md` | The LLM-as-grader prompt with full rubric |
| `eval-runner.py` | Script that runs the bot, grades responses, outputs scorecard |
| `sample-scorecard.md` | Example scorecard with pass rates and failure analysis |
| `eval-design-decisions.md` | What to measure, what to leave out, and why |

---

## How to Run

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
python eval-runner.py
```

Outputs a scorecard to `scorecard-output.md` with per-question scores and a summary.

---

## What This Demonstrates

- **Evaluation thinking** — knowing what to measure is harder than building the measurement
- **LLMs-as-graders** — using a model to grade a model, with a structured rubric to prevent grader drift
- **Golden dataset design** — curating test cases that cover failure modes, not just happy paths
- **Repeatable process** — any prompt change can be re-evaluated against the same dataset in minutes

---

## Resume Bullet

Built an automated LLM evaluation suite using Claude as grader, applying a structured 4-dimension rubric across a 20-item golden dataset to replace subjective bot review. Reduced prompt iteration cycle from days of manual review to minutes of automated scoring, with failure flags surfacing constraint violations and tone mismatches across edge-case scenarios.
