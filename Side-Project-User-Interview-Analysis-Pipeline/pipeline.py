"""
User Interview Analysis Pipeline
Three-stage multi-model automation:
  Stage 1: Haiku 4.5  — Extraction (structured, fast, cheap)
  Stage 2: Sonnet 4.6 — Inference  (nuanced, per-transcript reasoning)
  Stage 3: Opus 4.7   — Synthesis  (cross-transcript patterns and roadmap implications)
"""

import os
import anthropic
from pathlib import Path

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

TRANSCRIPTS_DIR = Path("sample-transcripts")
OUTPUT_DIR      = Path("sample-output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ── Prompts ───────────────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """
You are a user research assistant. Extract structured information from this interview transcript.
Be precise and literal. Do not interpret or infer — only extract what is explicitly stated.

Return in this exact format:

## Summary
One paragraph summary of the interview.

## Sentiment
One word only: frustrated / neutral / satisfied / conflicted

## Verbatim Quotes
The 3 most revealing quotes, copied exactly as spoken.
- "[quote 1]"
- "[quote 2]"
- "[quote 3]"

## Stated Pain Points
What the user explicitly said was difficult or broken.
- [pain point 1]
- [pain point 2]

## Observed Behaviors
What the user described actually doing — their current process or workarounds.
- [behavior 1]
- [behavior 2]

Transcript:
{transcript}
"""

INFERENCE_PROMPT = """
You are a senior user researcher. You have a structured extraction from a user interview.
Go beneath the surface — find what the user meant, not just what they said.

Return in this exact format:

## Said vs Meant
2-3 moments where the literal statement and underlying meaning diverge.
- Said: "[quote]" / Meant: [interpretation]

## Contradictions
Where the user contradicted themselves and what it reveals.
- [contradiction and insight]

## Unspoken Frustrations
Frustrations hinted at but never directly stated.
- [unspoken frustration and the signal]

## Behavior Gap
- Stated behavior: [what they claimed]
- Actual behavior: [what they described]
- Gap insight: [what this tells you]

## Workaround Detection
Workarounds built around the product rather than using it as intended.
- [workaround] — Type: bypass / supplement / substitute

Extraction:
{extraction}

Original transcript:
{transcript}
"""

SYNTHESIS_PROMPT = """
You are a principal product strategist with inference analyses from {n} user interviews.
Synthesize across all of them. Find patterns that only emerge when looking at everything together.
Do not summarize individual interviews. Be specific. Name numbers. Challenge obvious interpretations.

Return in this exact format:

## Cross-User Patterns
Themes appearing consistently across 8+ users.
- [Pattern]: seen in [X/{n}] users — [evidence]

## Loud Minority vs Quiet Majority
- Loud minority: [what they say, how many]
- Quiet majority: [what they actually show, how many]

## Workaround Taxonomy
How many users described workarounds vs direct pain points?
- Bypass workarounds: [count] — [what they bypass]
- Supplement workarounds: [count] — [what they add]
- Substitute workarounds: [count] — [what they replace]

## The Real Underlying Need
What is the user actually trying to accomplish beneath all stated pain points?
State as a single clear need, not a feature request.

## What We Were Solving For vs What We Should Be Solving For
Where does current product direction diverge from actual user need?

## Roadmap Implications
3 concrete implications with confidence levels.
- [Implication] — Confidence: high/medium/low — [why]

All inference analyses:
{all_inferences}
"""


# ── Stage 1: Extraction (Haiku) ───────────────────────────────────────────────

def extract(transcript: str, transcript_name: str) -> str:
    print(f"  [Haiku] Extracting: {transcript_name}")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": EXTRACTION_PROMPT.format(transcript=transcript)
        }]
    )
    return response.content[0].text


# ── Stage 2: Inference (Sonnet) ───────────────────────────────────────────────

def infer(transcript: str, extraction: str, transcript_name: str) -> str:
    print(f"  [Sonnet] Inferring: {transcript_name}")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": INFERENCE_PROMPT.format(
                extraction=extraction,
                transcript=transcript
            )
        }]
    )
    return response.content[0].text


# ── Stage 3: Synthesis (Opus) ─────────────────────────────────────────────────

def synthesize(all_inferences: list[str]) -> str:
    print(f"\n  [Opus] Synthesizing across {len(all_inferences)} transcripts...")
    combined = "\n\n---\n\n".join(
        [f"Interview {i+1}:\n{inf}" for i, inf in enumerate(all_inferences)]
    )
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": SYNTHESIS_PROMPT.format(
                n=len(all_inferences),
                all_inferences=combined
            )
        }]
    )
    return response.content[0].text


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline():
    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.md")) + \
                       sorted(TRANSCRIPTS_DIR.glob("*.txt"))

    if not transcript_files:
        print("No transcripts found in sample-transcripts/. Add .md or .txt files.")
        return

    print(f"\nRunning pipeline on {len(transcript_files)} transcripts...\n")

    all_inferences = []

    for tf in transcript_files:
        name      = tf.stem
        transcript = tf.read_text()

        print(f"\nProcessing: {name}")

        # Stage 1 — Extraction
        extraction = extract(transcript, name)
        (OUTPUT_DIR / f"{name}-1-extraction.md").write_text(extraction)

        # Stage 2 — Inference
        inference = infer(transcript, extraction, name)
        (OUTPUT_DIR / f"{name}-2-inference.md").write_text(inference)

        all_inferences.append(inference)

    # Stage 3 — Synthesis across all transcripts
    synthesis = synthesize(all_inferences)
    (OUTPUT_DIR / "synthesis.md").write_text(synthesis)

    print(f"\nDone. Outputs saved to {OUTPUT_DIR}/")
    print(f"  - {len(transcript_files)} extraction files")
    print(f"  - {len(transcript_files)} inference files")
    print(f"  - 1 synthesis file (synthesis.md)")


if __name__ == "__main__":
    run_pipeline()
