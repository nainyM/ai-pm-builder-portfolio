# User Interview Analysis Pipeline — Multi-Model AI Automation

Automated user research synthesis using a three-stage Claude pipeline:  
**Haiku 4.5 → Sonnet 4.6 → Opus 4.7**

Same transcripts. Same prompts. Each model doing what it does best.

---

## The Problem

User interviews generate a lot of raw material — 15 transcripts, hours of notes, scattered quotes. The traditional PM approach is to manually read everything, tag themes in a spreadsheet, and synthesize by intuition. It is slow, subjective, and the insight quality depends entirely on how much cognitive energy you have left at the end.

The deeper problem: when you do it manually, you tend to find what you are already looking for. Confirmation bias at the research stage kills roadmaps.

This pipeline replaces manual synthesis with a structured three-stage AI workflow — each stage using a different Claude model, matched to the cognitive demand of the task.

---

## The Insight That Changed Everything

After running 15 transcripts through this pipeline, Opus flagged something the manual process had missed entirely:

> **11 of 15 users described workarounds, not pain points.**

They were not complaining about the product. They had quietly adapted around it. That distinction — workaround vs pain point — completely changed what we needed to build. We had been solving for the wrong thing.

That single insight came from synthesis across all 15 transcripts at once — something that is cognitively hard for a human to do after hours of reading, and trivial for a model that holds all the context simultaneously.

---

## Three-Stage Pipeline

### Stage 1 — Haiku 4.5 — Extraction

**Task:** Process each transcript individually. Pull out structured data fast and cheap.

**Haiku extracts:**
- One-paragraph summary of the interview
- Sentiment tag (frustrated / neutral / satisfied / conflicted)
- Top 3 verbatim quotes
- Stated pain points (what the user explicitly complained about)
- Observed behaviors (what they said they actually do)

**Why Haiku:** It is 5x cheaper than Opus and handles structured extraction with high accuracy. The task is well-defined — find this, tag that, quote this. Haiku is fast and reliable here. The moment you ask it to reason across transcripts or find tensions, it flattens. So we don't ask it to.

**Cost:** ~$0.002 per transcript

---

### Stage 2 — Sonnet 4.6 — Inference

**Task:** Take Haiku's structured extractions and go deeper on each transcript. Find what is underneath the surface.

**Sonnet infers:**
- What users said vs what they actually meant
- Contradictions within the same interview (said X, described doing Y)
- Unspoken frustrations (things they hinted at but did not say directly)
- Behavior gaps (the difference between what they said they do and what they described doing)
- Workarounds they have built around the product

**Why Sonnet:** Sonnet holds nuance across a full transcript in a way Haiku cannot. It picks up on hedging language, contradiction, and implication. This is inference work — reading between the lines — which requires genuine language understanding, not just pattern matching.

**Cost:** ~$0.01 per transcript

---

### Stage 3 — Opus 4.7 — Synthesis

**Task:** Take all inference outputs from all 15 transcripts and synthesize across them. Find the patterns that only emerge when you look at everything together.

**Opus synthesizes:**
- Cross-user patterns (what is consistent across 10+ users)
- Contradictions across users (where users disagree and why)
- Workaround taxonomy (how many users built workarounds and what kind)
- The real underlying need beneath all stated pain points
- Roadmap implications with confidence levels

**Why Opus:** By the time you reach synthesis, you already know what the data says. Opus is for reasoning about what it means. It flags things that are statistically significant across the dataset and distinguishes between loud minorities and quiet majorities — something humans are notoriously bad at.

**Cost:** ~$0.05 for all 15 transcripts synthesized together

---

## Total Cost per Research Round

| Stage | Model | Cost for 15 Transcripts |
|-------|-------|------------------------|
| Extraction | Haiku 4.5 | ~$0.03 |
| Inference | Sonnet 4.6 | ~$0.15 |
| Synthesis | Opus 4.7 | ~$0.05 |
| **Total** | | **~$0.23** |

A full user research synthesis for under 25 cents.

---

## Files

| File | Description |
|------|-------------|
| `pipeline.py` | Full three-stage automation script |
| `prompts/extraction.md` | Haiku extraction prompt |
| `prompts/inference.md` | Sonnet inference prompt |
| `prompts/synthesis.md` | Opus synthesis prompt |
| `model-selection-rationale.md` | Why each model was matched to each stage |
| `sample-transcripts/` | 3 realistic sample interview transcripts |
| `sample-output/` | Example outputs from each pipeline stage |

---

## How to Run

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key-here
python pipeline.py
```

Drop your transcript `.txt` or `.md` files into `sample-transcripts/` and run. Outputs land in `sample-output/`.

---

## Resume Bullet

> Designed and built a three-stage multi-model user research pipeline using Claude Haiku, Sonnet, and Opus — automating extraction, inference, and synthesis across 15 interview transcripts. Identified that 11 of 15 users described workarounds rather than pain points, a cross-transcript pattern that changed the product roadmap direction.

---

## What This Demonstrates

- **Model selection judgment** — not using one model for everything, matching capability to task
- **Cost vs quality tradeoffs** — Haiku where speed and price matter, Opus where reasoning depth matters
- **Multi-model orchestration** — outputs of one model feed the next stage
- **Real PM outcome** — the pipeline produced a roadmap-changing insight, not just a summary
