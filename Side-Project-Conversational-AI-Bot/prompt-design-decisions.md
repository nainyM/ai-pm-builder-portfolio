# Prompt Design Decisions — 3P Framework Applied

This document explains the product thinking behind the system prompt structure.  
Framework used: **3P (Prioritization, Placement, Prominence)** + **4 AI Design Patterns**.

---

## The 3P Framework

### Prioritization — What should the bot handle first?

Support requests are not equal. Some are time-sensitive (a package that hasn't arrived), some are high-stakes (a refund dispute), and some are low-effort (a tracking number lookup). The bot needs to know the order of importance so it allocates effort correctly.

**Priority order built into the prompt:**

| Priority | Request Type | Why |
|----------|-------------|-----|
| 1 | Damaged / wrong item | Highest trust risk. Unhappy customer + incorrect item = churn |
| 2 | Delivery and tracking issues | Time-sensitive. Customer anxiety peaks here |
| 3 | Returns and refunds | High friction. Customers often expect the worst |
| 4 | Order status | High volume, low effort |
| 5 | Product questions | Lower urgency, good for bot deflection |

The bot does not rank these explicitly in its response — it internalizes the priority through how policies are ordered and weighted in the prompt. Damaged item policy is listed first and given the most permissive treatment (no return required). This signals to the model that this case is treated differently.

### Placement — Where in the conversation does critical information go?

Two placement decisions shaped the prompt:

**1. Acknowledgment before resolution.**  
For frustrated customers, the bot is instructed to lead with emotional acknowledgment before moving to the fix. Placing resolution first reads as dismissive — the customer feels unheard even if the problem gets solved. This is the same principle human support agents are trained on.

**2. Escalation path placed at the end of the constraints section.**  
Escalation is not buried or hidden — it is the last "always available" move. Placing it at the end means it functions as a catch-all: if everything else fails, the bot knows exactly what to do and where to send the customer.

### Prominence — What gets emphasis?

Three things are made visually and structurally prominent in the prompt:

**1. What the bot must never do** — formatted as a separate named section with a dedicated header. Not buried in a paragraph. This is the highest-risk zone: unauthorized discounts, hallucinated data, false promises. Prominence here is risk management.

**2. The structured context block** — placed at the end of the prompt as a clear template. By separating it structurally from the instructions, it trains the model to treat injected data differently from general knowledge.

**3. Tone instructions** — given their own sub-section, not a single sentence. Tone is the thing customers feel most directly. Under-specifying it leads to inconsistent bot personality across conversation types.

---

## 4 AI Design Patterns Applied

### 1. Inputs

**What the bot receives:**
- Structured context: customer name, order ID, status, tracking, return eligibility
- The customer's message in the conversation

**Design decision:** Context is injected as a structured template at conversation start, not embedded in a paragraph. This makes it easy to parse, extend, and debug. A new variable (e.g., loyalty tier) can be added in one place and immediately used anywhere in the conversation.

**What the bot does NOT receive:**
- Full order history beyond the current order
- Payment method details
- Past support ticket history

Limiting inputs is a product decision. More context can make the bot more helpful but also increases the risk of surfacing information incorrectly or confusing the model. Start minimal, expand deliberately.

### 2. Special Instructions

The "What you must never do" section is the Special Instructions layer. These are rules that override the model's general helpful behavior.

Key ones and why they matter:

| Instruction | Risk it prevents |
|-------------|-----------------|
| No unauthorized discounts | Customers learning to complain for discounts (support cost + margin loss) |
| No guessing order data | Hallucinated tracking info that customers act on |
| No claiming to be human | Ethical baseline; also a regulatory risk in some markets |
| No delivery date promises without data | Creates expectation the company cannot control |

The instructions are phrased as "do not" rather than "try not to" — LLMs respond better to clear negations than hedged suggestions.

### 3. Outputs

**Format:** Plain prose, no headers in responses, bullets only for lists of steps.  
**Length:** 1–3 short paragraphs.  
**Tone:** Warm and direct; adapts to customer emotional state.

**Why no filler phrases:**  
"Great question!" adds zero information and subtracts credibility. Customers in support contexts have a task. Every sentence that delays getting to resolution erodes the experience. This was validated by comparing responses with and without the instruction — the difference was immediately visible.

**Why adapt tone to emotional register:**  
A bot that responds to "I am absolutely furious about this" with a calm procedural explanation feels tone-deaf. Matching emotional register — leading with "I completely understand how frustrating this is" — is not just politeness. It reduces escalation rates.

### 4. Feedback Loops

The prompt is designed to support a feedback loop, even though this project does not implement one end-to-end.

**Designed feedback signals:**
- Escalation triggers → each escalation is a signal the bot encountered something outside its capability
- Explicit customer dissatisfaction → "I'm not happy with this answer" should be logged as a failure case
- Resolution confirmation → did the customer say "thanks, that helped" or did they go silent?

**What would improve the prompt over time:**
- Log cases where the bot had to say "I don't have that information" → these are missing input fields
- Log cases where customers asked for discounts the bot refused → validates or updates the discount policy
- Build a golden dataset from escalation transcripts → feed into an eval framework (see Project 04)

---

## What I Would Do Differently

**1. Add a confidence signal.**  
The bot should be able to say "I'm not certain about this — let me flag it" rather than either answering confidently or escalating. A confidence tier (confident / uncertain / escalate) would create a more nuanced support experience.

**2. Separate personas by channel.**  
A chat widget on the website and a support email thread need different response lengths, formality levels, and urgency signals. One system prompt trying to serve both will be slightly wrong for each. Channel-specific prompts with a shared policy core would be cleaner.

**3. Version the prompt explicitly.**  
Prompt changes are product changes. They should be tracked, dated, and documented the same way code changes are — not edited in place without a record of what changed and why.
