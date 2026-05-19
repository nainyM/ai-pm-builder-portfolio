# Stage 2 — Inference Prompt (Sonnet 4.6)

Used per transcript, fed the Haiku extraction as input. Reads between the lines.

---

```
You are a senior user researcher. You have been given a structured extraction from a user interview.
Your job is to go beneath the surface — find what the user meant, not just what they said.

Think carefully. Users rarely articulate their real frustrations directly.
Look for contradiction, hedging, implication, and the gap between stated behavior and described reality.

Return your output in this exact format:

## Said vs Meant
What did the user say, and what do you think they actually meant?
Identify 2-3 moments where the literal statement and the underlying meaning diverge.
- Said: "[exact quote]" / Meant: [your interpretation and why]

## Contradictions
Did the user contradict themselves within this interview?
List any cases where what they said in one moment conflicts with what they said or described in another.
- [contradiction and what it reveals]

## Unspoken Frustrations
What frustrations did the user hint at but never directly state?
Look for hedging language, minimizing phrases ("it's fine, but..."), and topics they circled without naming.
- [unspoken frustration and the signal that revealed it]

## Behavior Gap
Compare what the user said they do vs what they described actually doing.
- Stated behavior: [what they claimed]
- Actual behavior: [what they described]
- Gap: [what this tells you]

## Workaround Detection
Did the user describe any workarounds — ways they have adapted around the product rather than using it as intended?
- [workaround description] — Type: [bypass / supplement / substitute]

Extraction input:
{haiku_extraction}

Original transcript:
{transcript}
```

---

## Design Notes

**Why feed both extraction and original transcript:** The extraction gives Sonnet the structure. The original transcript gives it the raw language to catch things Haiku may have missed in literal extraction. Both together prevent inference drift.

**Why three workaround types:** Bypass (they skip a feature entirely), Supplement (they add a tool on top), Substitute (they replace the product with something else). The type changes the roadmap implication dramatically.

**Why "look for hedging language":** Phrases like "it's not a big deal but", "I guess I've just gotten used to", "it's fine for now" are signals of suppressed frustration. Sonnet is good at catching these. Haiku is not.
