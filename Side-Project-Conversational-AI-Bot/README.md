# Conversational AI Support Bot — eCommerce

A customer support bot for a mid-size eCommerce store (ShopSmart) built with Claude API.  
The focus is on **prompt engineering and product design** — not code complexity.

---

## The Problem

Most eCommerce support bots fail in one of two ways:

1. **Too rigid** — scripted decision trees that break the moment a customer's situation doesn't fit the flowchart
2. **Too permissive** — LLM bots with no guardrails that hallucinate policies, give unauthorized discounts, or escalate every edge case to a human

The goal here was to design a bot that handles the messy middle: ambiguous requests, frustrated customers, and situations where the right answer is "I don't know, but here's what I can do."

---

## Approach

Built using the **3P Framework** (Prioritization, Placement, Prominence) and the **4 AI Design Patterns** (Inputs, Special Instructions, Outputs, Feedback Loops) from the Maven AI PM Certification.

The system prompt is the product. Every line is a deliberate design decision.

**What the bot handles:**
- Order status, tracking, and delivery issues
- Returns, refunds, and exchange requests
- Product questions and size/fit guidance
- Account and payment queries
- Escalation to a human agent when needed

**What the bot never does:**
- Offer discounts or adjustments not in the official policy
- Make up order or account details it hasn't been given
- Pretend to be a human when sincerely asked

---

## Files

| File | Description |
|------|-------------|
| `system-prompt.md` | The full system prompt with inline annotations |
| `prompt-design-decisions.md` | Product thinking behind the prompt structure |
| `bot.py` | Python implementation using Anthropic SDK |
| `conversation-examples/` | 5 real edge-case conversations |

---

## What I Learned

**1. The system prompt is a product spec, not a chatbot script.**  
Every constraint in the prompt reflects a real product decision — what the company is liable for, what creates trust, what burns support team time. Writing it forced clarity on things a PRD often leaves vague.

**2. Tone is a design lever, not a style preference.**  
A bot that sounds too corporate loses frustrated customers faster. A bot that sounds too casual loses credibility on policy issues. Calibrating tone by *topic type* (empathetic for complaints, precise for policies) made a measurable difference in conversation quality.

**3. The hardest cases are not the angry ones — they are the ambiguous ones.**  
A customer asking "can you help me?" with no context is harder to handle well than a customer who is furious about a late order. Designing good fallback behavior took more iteration than any other part.

**4. Knowing when NOT to answer is a feature.**  
The bot's explicit refusal to fabricate order details or invent policies is not a limitation — it is the thing that makes it trustworthy enough to deploy.

---

## Stack

- Claude 3.5 Sonnet via Anthropic SDK
- Python 3.11
- No vector database or RAG — pure prompt engineering
