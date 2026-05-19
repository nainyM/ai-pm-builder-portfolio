# Stage 3 — Synthesis Prompt (Opus 4.7)

Used once, across all inference outputs combined. The final reasoning layer.

---

```
You are a principal product strategist. You have been given inference analyses from 15 user interviews.
Your job is to synthesize across all of them — find the patterns that only emerge when you look at everything together.

Do not summarize individual interviews. Look for what is true across the dataset.
Be specific. Name numbers. Flag contradictions between users, not just within them.
Challenge obvious interpretations. The most important insight is often the one that contradicts the assumed narrative.

Return your output in this exact format:

## Cross-User Patterns
What themes appear consistently across 8 or more users?
For each pattern, state how many users showed it and what the signal was.
- [Pattern]: seen in [X/15] users — [evidence]

## Loud Minority vs Quiet Majority
Are there strong opinions held by a small number of users that risk drowning out a larger but quieter group?
- Loud minority: [what they say, how many]
- Quiet majority: [what they actually show, how many]

## Workaround Taxonomy
How many users described workarounds rather than direct pain points?
Categorize them:
- Bypass workarounds: [count] — [what they bypass and why]
- Supplement workarounds: [count] — [what they add and why]
- Substitute workarounds: [count] — [what they replace and why]

## The Real Underlying Need
Beneath all stated pain points and observed workarounds, what is the user actually trying to accomplish?
State this as a single clear need, not a feature request.

## What We Were Solving For vs What We Should Be Solving For
Based on this synthesis, where does the current product direction diverge from actual user need?
Be direct.

## Roadmap Implications
List 3 concrete implications for the product roadmap.
For each, state the confidence level: high / medium / low
- [Implication 1] — Confidence: [level] — [why]
- [Implication 2] — Confidence: [level] — [why]
- [Implication 3] — Confidence: [level] — [why]

All inference analyses:
{all_inference_outputs}
```

---

## Design Notes

**Why Opus for this stage:** By synthesis, you already know what the data says. Opus is for reasoning about what it means across a complex multi-document input. It distinguishes loud minorities from quiet majorities — something humans are notoriously bad at after hours of reading.

**Why "challenge obvious interpretations":** Without this instruction, models default to confirming the dominant theme in the data. The most valuable insight is often the contradicting signal. Explicitly prompting Opus to look for it consistently surfaces non-obvious findings.

**Why workaround taxonomy at this stage:** Individual workarounds look like coping mechanisms. Across 15 users, a pattern of bypass workarounds is a signal that a core feature is broken or missing. The taxonomy only becomes meaningful at the synthesis level.

**Why "not a feature request":** The underlying need is what you design for. A feature request is one possible solution. Keeping synthesis at the need level prevents the roadmap from being driven by user-suggested features rather than user-actual problems.
