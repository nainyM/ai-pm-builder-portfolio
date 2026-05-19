# Model Selection Rationale

Why three models instead of one, and why each model was matched to its stage.

---

## The Core Principle

Different cognitive tasks have different requirements. Using one model for everything is like using a sledgehammer for every job — it works, but it is expensive and often overkill. The right approach is to match model capability to task complexity.

---

## Stage 1 — Haiku 4.5 for Extraction

**Task type:** Structured information retrieval  
**Cognitive demand:** Low — find this, tag that, quote this  
**Why Haiku wins here:**

Extraction is a well-defined task. The instructions are explicit, the output format is fixed, and success is easy to verify. Haiku handles this with high accuracy at a fraction of the cost of larger models.

The moment extraction becomes interpretation — "what does this mean?" — Haiku starts to flatten. It will give you an answer, but it will miss nuance. So the extraction prompt is written to be strictly literal: only what the user explicitly said, no inference allowed.

**Cost comparison for 15 transcripts:**
- Haiku: ~$0.03
- Sonnet: ~$0.15
- Opus: ~$0.75

Saving ~$0.72 by using Haiku for extraction is meaningful at scale (thousands of transcripts).

---

## Stage 2 — Sonnet 4.6 for Inference

**Task type:** Nuanced language understanding within a single document  
**Cognitive demand:** Medium-high — reading between the lines  
**Why Sonnet wins here:**

Inference requires genuine language understanding. Finding the tension between what a user said and what they meant, spotting hedging language, identifying the gap between stated and actual behavior — these are tasks that need a model that holds the full texture of a conversation, not just its explicit content.

Haiku flattens at this level. It will tell you what was said but miss the subtext. Opus would do this well but is expensive per transcript and the task does not require cross-document reasoning yet.

Sonnet is the right fit: strong enough to hold nuance across a full transcript, cost-effective enough to run on each of 15 transcripts individually.

---

## Stage 3 — Opus 4.7 for Synthesis

**Task type:** Cross-document reasoning and strategic implication  
**Cognitive demand:** High — finding patterns across a complex multi-input dataset  
**Why Opus wins here:**

By the time you reach synthesis, you already know what the individual transcripts say. The question is what it all means together. This requires:

- Holding 15 documents in context simultaneously
- Distinguishing signal from noise at scale
- Challenging the dominant narrative in the data
- Reasoning about implications with appropriate confidence levels

Opus is the only model in the family that does this consistently well. The cost is justified because synthesis runs once per research round, not once per transcript. And the output directly informs roadmap decisions — the quality bar is highest here.

---

## What Happens If You Use One Model for Everything

**All Haiku:** Fast and cheap. Extraction is fine. Inference is shallow. Synthesis misses cross-document patterns entirely.

**All Sonnet:** Good inference. Synthesis is reasonable but misses non-obvious cross-user patterns. Costs more than the three-model approach for no gain on extraction.

**All Opus:** Best quality at every stage. Costs ~10x more than the tiered approach. At scale (hundreds of research rounds) this becomes prohibitive.

**Tiered approach:** Best quality where it matters most (synthesis), right-sized cost everywhere else. Total cost is ~$0.23 per research round of 15 transcripts.

---

## Decision Framework for Other Use Cases

Use this logic when selecting models for any multi-stage pipeline:

| If the task is... | Use... |
|---|---|
| Structured extraction, classification, tagging | Haiku |
| Single-document reasoning, nuance, inference | Sonnet |
| Cross-document synthesis, strategic reasoning | Opus |
| Real-time conversation, low latency required | Haiku |
| Complex code generation or debugging | Sonnet or Opus |
