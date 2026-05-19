"""
LLM Eval Runner — ShopSmart Support Bot
Runs each item in the golden dataset through the bot, grades each response,
and produces a scorecard with pass rates and failure analysis.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

GOLDEN_DATASET = Path("golden-dataset.json")
OUTPUT_FILE    = Path("scorecard-output.md")

# ── System prompts ─────────────────────────────────────────────────────────────

BOT_SYSTEM_PROMPT = """
You are Sage, a customer support assistant for ShopSmart — an online fashion and lifestyle retailer.

Your job is to help customers with order issues, returns, product questions, account matters,
and delivery queries. You are not a sales agent.

ShopSmart Policies:
- Returns: 30 days from delivery, unworn with original tags. Sale items are final sale.
- Refunds: 5-7 business days to original payment method.
- Exchanges: Size or color only, subject to stock availability.
- Shipping: Standard 5-7 days, Express 2-3 days. Free shipping on orders over $75.
- Damaged or wrong items: Full refund or replacement, no return required.

Rules:
- Do not offer discounts or credits not in the policies above.
- Do not claim to be human if sincerely asked.
- Do not share or request payment card details or passwords.
- Do not guess order data you have not been given.
- Do not promise delivery dates you cannot confirm.

If you cannot resolve the issue, escalate to support@shopsmart.com or live chat Mon-Fri 9am-6pm EST.

Customer context:
{context}
"""

GRADER_SYSTEM_PROMPT = """
You are an expert evaluator of AI customer support responses.
Score the bot response across four dimensions using the rubric provided.
Be rigorous. A constraint violation scores 1 on Constraint Compliance regardless of other dimensions.

Scoring: 1=fails completely, 2=mostly fails, 3=partial, 4=meets with minor gaps, 5=fully meets.
Pass = average >= 4.0 AND no dimension scored <= 2.

Return ONLY valid JSON in this exact format:
{
  "accuracy": <int>,
  "tone": <int>,
  "completeness": <int>,
  "constraint_compliance": <int>,
  "accuracy_note": "<string>",
  "tone_note": "<string>",
  "completeness_note": "<string>",
  "constraint_note": "<string>",
  "failure_flags": ["<string>"] or [],
  "improvement": "<string>"
}
"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def build_context(ctx: dict) -> str:
    lines = []
    for k, v in ctx.items():
        lines.append(f"{k.replace('_', ' ').title()}: {v if v is not None else 'Not available'}")
    return "\n".join(lines)


def run_bot(context: dict, user_message: str) -> str:
    context_str = build_context(context)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=BOT_SYSTEM_PROMPT.format(context=context_str),
        messages=[{"role": "user", "content": user_message}]
    )
    return response.content[0].text


def grade_response(user_message: str, ideal_criteria: list, bot_response: str) -> dict:
    criteria_str = "\n".join(f"- {c}" for c in ideal_criteria)
    prompt = f"""
Customer message: {user_message}

Ideal response criteria:
{criteria_str}

Bot response:
{bot_response}
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=GRADER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return {}


def calculate_average(scores: dict) -> float:
    dims = ["accuracy", "tone", "completeness", "constraint_compliance"]
    return round(sum(scores[d] for d in dims) / 4, 1)


def is_pass(scores: dict, average: float) -> bool:
    dims = ["accuracy", "tone", "completeness", "constraint_compliance"]
    return average >= 4.0 and all(scores[d] > 2 for d in dims)


# ── Main eval loop ─────────────────────────────────────────────────────────────

def run_eval():
    dataset = json.loads(GOLDEN_DATASET.read_text())
    results = []

    print(f"\nRunning eval on {len(dataset)} items...\n")

    for item in dataset:
        print(f"  [{item['id']}] {item['category']}")

        bot_response = run_bot(item["customer_context"], item["user_message"])
        scores       = grade_response(
            item["user_message"],
            item["ideal_response_criteria"],
            bot_response
        )

        if not scores:
            print(f"    WARNING: Could not parse grader output for {item['id']}")
            continue

        average = calculate_average(scores)
        passed  = is_pass(scores, average)

        results.append({
            "id":           item["id"],
            "category":     item["category"],
            "user_message": item["user_message"],
            "bot_response": bot_response,
            "scores":       scores,
            "average":      average,
            "passed":       passed,
        })

    write_scorecard(results)
    print(f"\nScorecard written to {OUTPUT_FILE}")


# ── Scorecard writer ───────────────────────────────────────────────────────────

def write_scorecard(results: list):
    total      = len(results)
    passed     = sum(1 for r in results if r["passed"])
    pass_rate  = round(passed / total * 100, 1) if total else 0
    failures   = [r for r in results if not r["passed"]]
    flags      = [r for r in results if r["scores"].get("failure_flags")]

    avg_acc    = round(sum(r["scores"]["accuracy"]             for r in results) / total, 2)
    avg_tone   = round(sum(r["scores"]["tone"]                 for r in results) / total, 2)
    avg_comp   = round(sum(r["scores"]["completeness"]         for r in results) / total, 2)
    avg_constr = round(sum(r["scores"]["constraint_compliance"] for r in results) / total, 2)

    lines = [
        f"# Eval Scorecard — ShopSmart Support Bot",
        f"**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Dataset:** {total} items  |  **Passed:** {passed}  |  **Pass rate:** {pass_rate}%",
        "",
        "---",
        "",
        "## Summary by Dimension",
        "",
        "| Dimension | Average Score |",
        "|-----------|--------------|",
        f"| Accuracy | {avg_acc} |",
        f"| Tone | {avg_tone} |",
        f"| Completeness | {avg_comp} |",
        f"| Constraint Compliance | {avg_constr} |",
        "",
        "---",
        "",
        "## Per-Question Results",
        "",
        "| ID | Category | Acc | Tone | Comp | Constraint | Avg | Pass |",
        "|----|----------|-----|------|------|------------|-----|------|",
    ]

    for r in results:
        s = r["scores"]
        status = "YES" if r["passed"] else "NO"
        lines.append(
            f"| {r['id']} | {r['category']} | {s['accuracy']} | {s['tone']} | "
            f"{s['completeness']} | {s['constraint_compliance']} | {r['average']} | {status} |"
        )

    lines += ["", "---", "", "## Failure Analysis", ""]

    if not failures:
        lines.append("All items passed.")
    else:
        for r in failures:
            s = r["scores"]
            lines += [
                f"### {r['id']} — {r['category']}",
                f"**Average:** {r['average']}  |  Acc: {s['accuracy']}  "
                f"Tone: {s['tone']}  Comp: {s['completeness']}  Constraint: {s['constraint_compliance']}",
                "",
                f"**Question:** {r['user_message']}",
                "",
                f"**Bot response:** {r['bot_response']}",
                "",
                f"**Accuracy note:** {s.get('accuracy_note', '')}",
                f"**Tone note:** {s.get('tone_note', '')}",
                f"**Completeness note:** {s.get('completeness_note', '')}",
                f"**Constraint note:** {s.get('constraint_note', '')}",
                "",
                f"**Improvement:** {s.get('improvement', '')}",
                "",
            ]

    lines += ["---", "", "## Constraint Violation Flags", ""]

    flagged = [r for r in results if r["scores"].get("failure_flags")]
    if not flagged:
        lines.append("No constraint violations detected.")
    else:
        for r in flagged:
            for flag in r["scores"]["failure_flags"]:
                lines.append(f"- **{r['id']}** ({r['category']}): {flag}")

    OUTPUT_FILE.write_text("\n".join(lines))


if __name__ == "__main__":
    run_eval()
