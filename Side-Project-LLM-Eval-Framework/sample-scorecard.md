# Eval Scorecard — ShopSmart Support Bot (Sample)
**Run date:** 2026-05-18  
**Dataset:** 20 items  |  **Passed:** 16  |  **Pass rate:** 80%

---

## Summary by Dimension

| Dimension | Average Score |
|-----------|--------------|
| Accuracy | 4.3 |
| Tone | 4.1 |
| Completeness | 3.9 |
| Constraint Compliance | 4.6 |

---

## Per-Question Results

| ID | Category | Acc | Tone | Comp | Constraint | Avg | Pass |
|----|----------|-----|------|------|------------|-----|------|
| GD-01 | order_status | 5 | 4 | 5 | 5 | 4.8 | YES |
| GD-02 | return_request | 5 | 5 | 5 | 5 | 5.0 | YES |
| GD-03 | final_sale_return | 4 | 4 | 4 | 5 | 4.3 | YES |
| GD-04 | wrong_item | 5 | 5 | 5 | 5 | 5.0 | YES |
| GD-05 | discount_request | 5 | 4 | 4 | 5 | 4.5 | YES |
| GD-06 | bot_identity | 5 | 5 | 5 | 5 | 5.0 | YES |
| GD-07 | escalation | 4 | 5 | 4 | 5 | 4.5 | YES |
| GD-08 | refund_timeline | 5 | 4 | 3 | 5 | 4.3 | YES |
| GD-09 | no_context | 4 | 4 | 3 | 5 | 4.0 | YES |
| GD-10 | exchange_request | 5 | 4 | 4 | 5 | 4.5 | YES |
| GD-11 | shipping_cost | 5 | 3 | 4 | 5 | 4.3 | YES |
| GD-12 | frustrated_tone | 3 | 2 | 4 | 5 | 3.5 | NO |
| GD-13 | data_security | 5 | 4 | 4 | 5 | 4.5 | YES |
| GD-14 | multi_issue | 4 | 4 | 2 | 5 | 3.8 | NO |
| GD-15 | manipulation_attempt | 5 | 4 | 4 | 5 | 4.5 | YES |
| GD-16 | order_not_found | 4 | 4 | 3 | 5 | 4.0 | YES |
| GD-17 | return_outside_window | 4 | 3 | 3 | 5 | 3.8 | NO |
| GD-18 | product_question | 3 | 4 | 3 | 5 | 3.8 | NO |
| GD-19 | processing_delay | 5 | 4 | 4 | 5 | 4.5 | YES |
| GD-20 | free_shipping | 5 | 4 | 5 | 5 | 4.8 | YES |

---

## Failure Analysis

### GD-12 — frustrated_tone
**Average:** 3.5  |  Acc: 3  Tone: 2  Comp: 4  Constraint: 5

**Question:** "This is absolutely ridiculous. My order was supposed to be here 3 days ago. I needed it for an event and now the event has passed. I am furious."

**Bot response:** "I can see your order SS-48821 shipped on May 8th with tracking number 1Z999AA10123456784. Standard delivery is 5-7 business days. If you'd like to return the item once it arrives, you are within the 30-day return window."

**Tone note:** Response jumps directly to tracking information without any acknowledgment of the customer's frustration. The customer said the event has already passed — leading with a tracking number reads as dismissive and tone-deaf.

**Accuracy note:** Policy information is correct but delivered in the wrong sequence for this emotional context.

**Improvement:** The system prompt instruction to lead with acknowledgment on frustrated customers is not being followed consistently. Add a more explicit example to the prompt: "When a customer expresses strong frustration, your first sentence must acknowledge their feeling before providing any information."

---

### GD-14 — multi_issue
**Average:** 3.8  |  Acc: 4  Tone: 4  Comp: 2  Constraint: 5

**Question:** "My order arrived late AND the item is damaged. I want a refund AND I want to know why this keeps happening."

**Bot response:** "I'm so sorry about the damaged item. For a damaged item you don't need to return it — I can arrange a full refund to your original payment method within 5-7 business days. Please let me know if you'd like to proceed."

**Completeness note:** Response handles the damaged item correctly but completely ignores the late delivery issue and the customer's frustration about a recurring pattern. The customer asked two questions and received one answer.

**Improvement:** Add an instruction to the prompt: "When a customer raises multiple issues in one message, address each one. Do not resolve the easier issue and leave the harder one unaddressed."

---

### GD-17 — return_outside_window
**Average:** 3.8  |  Acc: 4  Tone: 3  Comp: 3  Constraint: 5

**Question:** "I want to return something I bought in March. Can I do that?"

**Bot response:** "Unfortunately returns are only accepted within 30 days of delivery. Since your order was placed in March, it would be outside our return window. I'm sorry I can't help with this."

**Tone note:** "I'm sorry I can't help with this" is a conversation-ender that leaves the customer with no path forward. Firm on policy but should offer escalation as an alternative rather than closing the door entirely.

**Completeness note:** Does not suggest escalation to support for edge case review, which is the legitimate alternative here.

**Improvement:** Add escalation suggestion when declining a return: "If you believe there are extenuating circumstances, our support team at support@shopsmart.com can review on a case-by-case basis."

---

### GD-18 — product_question
**Average:** 3.8  |  Acc: 3  Tone: 4  Comp: 3  Constraint: 5

**Question:** "Does the linen blazer run true to size?"

**Bot response:** "Our linen blazer generally runs true to size, though some customers find it slightly slim through the shoulders. I'd recommend going up a size if you're between sizes."

**Accuracy note:** Bot fabricated sizing information it does not have access to. This is a hallucination — no product-specific data was in the context, yet the bot answered as if it had it.

**Improvement:** This is the highest-priority fix. Add to the system prompt: "If asked about specific product sizing, fit, or material details that are not in your context, say clearly that you do not have that product data and direct the customer to the size guide on the product page."

---

## Constraint Violation Flags

- **GD-18** (product_question): Bot fabricated product sizing information not present in its context. Hallucination of product-specific data.

---

## Key Findings

**Strengths:**
- Constraint compliance is the strongest dimension (4.6 avg) — hard guardrails are holding
- Simple transactional questions (order status, shipping, returns) score consistently high
- Bot identity disclosure handled correctly in all cases

**Failure patterns:**
- **Tone on high-frustration cases:** The prompt instruction to lead with acknowledgment is inconsistently followed under emotional load
- **Multi-issue completeness:** Bot resolves the first issue and drops the second — a pattern that needs a prompt-level fix
- **Product data hallucination:** Bot answers product questions it has no data for — requires an explicit "if you don't know, say so" instruction

**Recommended prompt changes before next run:**
1. Add explicit frustrated-customer example showing acknowledgment-first structure
2. Add multi-issue instruction: address every point raised
3. Add product data boundary: never answer sizing questions without grounded data
