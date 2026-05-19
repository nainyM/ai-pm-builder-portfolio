# Eval Design Decisions

What to measure, what to leave out, and why every choice was made deliberately.

---

## What to Measure

### Why four dimensions and not one overall score

A single score hides the failure mode. A bot can score 4.2 overall while having a constraint violation that would cause a real customer incident — unauthorized discount offered, order data fabricated, human identity claimed falsely. That response should never pass regardless of how warm its tone was.

Four dimensions make failures visible and actionable:
- **Accuracy** catches wrong policy information and hallucinated data
- **Tone** catches emotional mismatch — the most common reason customers escalate
- **Completeness** catches partial answers that leave issues unresolved
- **Constraint Compliance** catches hard guardrail violations — binary, no curve

### Why the hard floor on constraint compliance

Any response that violates a hard constraint scores 1 on Constraint Compliance automatically, regardless of how well it scored on other dimensions. And any dimension scoring 2 or below fails the item regardless of the average.

This is intentional. In a support context, a response that offers an unauthorized discount while being warm and accurate is still a business liability. The rubric reflects the real stakes.

### Why pass threshold is 4.0 average

A threshold of 4.0 means the bot needs to be solidly good, not just acceptable. A 3.5 average would let too many mediocre responses through. A 4.5 threshold would be unrealistically strict for early-stage evaluation. 4.0 is the right bar for a bot that is ready for limited production use.

---

## What to Leave Out

### Why not measure response length

Length is a proxy metric, not a quality metric. A 2-sentence response to a frustrated customer can be better than a 6-sentence one. A 1-sentence answer to a complex multi-issue complaint is almost always incomplete. Scoring length directly would penalize the right behavior in both cases.

Completeness already captures "did the response cover what it needed to" without enforcing an arbitrary word count.

### Why not measure grammar or spelling

The bot uses an LLM — grammar is not the failure mode. Spending evaluation capacity on grammar distracts from the dimensions that actually matter: policy accuracy, tone calibration, and constraint adherence.

### Why not measure customer satisfaction

Customer satisfaction requires a real customer. In an automated eval, satisfaction scoring would be simulated — the grader estimating how a customer might feel. That is a second layer of inference on top of an already-inferred grade, which reduces reliability. The four dimensions are proxies for satisfaction that can be measured directly against objective criteria.

### Why not use human graders

Human graders are slow, expensive, and inconsistent between reviewers. Two humans grading the same response to a frustrated customer will often disagree on whether the tone was appropriate. An LLM grader with a precise rubric applies the same standard every time.

This does not mean human review is useless — spot-checking grader outputs against human judgment is good practice. But as the primary eval mechanism, LLM-as-grader is faster, cheaper, and more consistent.

---

## Golden Dataset Design Decisions

### Why 20 items and not more

20 items is enough to cover the meaningful failure modes without making the eval expensive or slow to run on every prompt iteration. The goal of a golden dataset is to catch regressions — not to exhaustively test every possible scenario.

The 20 items were chosen to cover:
- High-frequency question types (order status, returns, shipping)
- Hard constraint scenarios (discount requests, bot identity, data security)
- Edge cases that break naive prompts (frustrated tone, multi-issue, missing context)
- Policy boundary cases (final sale, return outside window, product question without data)

### Why include the no-context scenarios

GD-09 and GD-16 test the bot with no customer data injected. This is one of the most important failure modes: a bot that fabricates order information when it has none is more dangerous than one that simply says it needs more details. Including these in the golden dataset ensures every prompt change is tested against the hallucination risk.

### Why include the manipulation scenario (GD-15)

Customers who have learned that complaining yields discounts will test the bot's boundaries. GD-15 — "just give me a discount and I'll go away" — tests whether the constraint holds under explicit social pressure. A bot that passes GD-05 (polite discount request) might still fail GD-15 (pushy discount request). Both need to be in the dataset.

---

## Grader Design Decisions

### Why Sonnet as the grader and not Haiku or Opus

- **Haiku** lacks the nuance to reliably catch tone mismatches and subtle policy inaccuracies. It grades accurately on simple right/wrong questions but misses the qualitative dimensions.
- **Opus** is consistent and excellent but overkill for per-response grading. At 20 items per eval run, Sonnet provides the right balance of quality and cost.
- **Sonnet** holds the rubric reliably, catches nuanced failures, and costs approximately $0.008 per response graded — making a full 20-item eval run cost under $0.20.

### Why request JSON output from the grader

Structured JSON output makes the scorecard generation deterministic. Free-text grader output requires parsing logic that can break unpredictably. JSON forces the grader to score in the exact format the runner expects and makes it easy to add new dimensions later without changing the parsing code.

### Why include an improvement suggestion in the grader output

Each eval run should produce actionable prompt changes, not just a score. The improvement suggestion forces the grader to identify the specific, fixable thing that would raise the lowest dimension. This makes the eval-to-prompt-iteration loop tight and intentional.

---

## What Would Make This Better

**1. Version tracking**
Each eval run should be tagged with the prompt version it tested. Without versioning, you lose the ability to compare results across iterations and attribute improvements or regressions to specific prompt changes.

**2. Regression detection**
An automated comparison between the current run and the previous run would flag new failures — items that passed before and now fail. This is the most important signal during active prompt development.

**3. Expanding the dataset over time**
Every real support escalation is a potential golden dataset item. A pipeline that flags escalations as candidate test cases and routes them for review would keep the dataset growing with real-world failures rather than hypothetical ones.

**4. Calibration check**
Periodically have a human grade a sample of the same responses the LLM grader evaluated and compare scores. If the grader and the human consistently disagree on tone, the rubric needs refinement.
