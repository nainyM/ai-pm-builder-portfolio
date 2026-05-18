# NAINY MEHRA — AI PM Builder Portfolio

> AI Product Manager | Maven AI PM Certification | Builder of conversational, search, and agentic AI systems

---

## About

I am an AI-native Product Manager with hands-on experience building and shipping AI products across conversational interfaces, personalization, and search. This portfolio documents real project work — from prompt design to multi-agent orchestration — built to demonstrate both product thinking and technical execution.

**Background:**
- COO & Co-founder, AgenticDating (AI-native dating agent, live at agenticdating.lovable.app)
- AI Product Management Certification — Maven (Instructors: Rohan Varma, OpenAI · Henry Shi, Anthropic)
- 8+ years building AI-powered consumer products

---

## Projects

| # | Project | Difficulty | Key Skill |
|---|---------|------------|-----------|
| 01 | [Conversational Support Bot](#01-conversational-support-bot) | Beginner | Prompt design, 3P Framework |
| 02 | [AI-Powered Product Search](#02-ai-powered-product-search) | Beginner–Medium | Embeddings, RAG, semantic search |
| 03 | [eCommerce Personalization Engine](#03-ecommerce-personalization-engine) | Medium | Context vs Behavior Matrix, LLM reasoning |
| 04 | [LLM Evaluation Framework](#04-llm-evaluation-framework) | Medium–Hard | LLMs-as-graders, golden datasets, evals |
| 05 | [Agentic Shopping Assistant](#05-agentic-shopping-assistant) | Hard | Multi-agent, Sense-Plan-Act, tool use |

---

## 01 — Conversational Support Bot

**Folder:** `01-conversational-bot/`

A customer support bot for an eCommerce store built with Claude API. The focus is on prompt architecture, not just making it work — documenting every design decision using the 3P Framework (Prioritization, Placement, Prominence) and the 4 AI Design Patterns: Inputs, Special Instructions, Outputs, and Feedback Loops.

**What's inside:**
- System prompt with inline annotations explaining each choice
- 5 real conversation examples covering edge cases
- Prompt design decisions doc
- Working Python implementation

**Resume bullet:** Designed AI-native user experiences using the 3P Framework and 4 AI Design Patterns across inputs, outputs, and feedback loops

---

## 02 — AI-Powered Product Search

**Folder:** `02-ai-powered-search/`

Semantic search over a product catalog using embeddings. Side-by-side comparison of keyword search vs semantic search on the same queries — showing concretely why semantic wins. Includes a RAG layer that generates natural language answers from retrieved products.

**What's inside:**
- Embedding-based search over a 20-product catalog
- Keyword vs semantic comparison on 5 real queries
- RAG layer design doc
- Working Python notebook

**Resume bullet:** Built AI-powered search using embeddings and RAG, demonstrating clear uplift over keyword-based retrieval

---

## 03 — eCommerce Personalization Engine

**Folder:** `03-ecommerce-personalization/`

Personalized product recommendations using user behavior context fed into an LLM. Shows that personalization is a reasoning problem — the model explains *why* it recommends each product, not just what to rank. Applies the Context vs. Behavior Matrix to decide when context alone is enough and when model behavior needs shaping.

**What's inside:**
- 3 user personas with distinct behavioral signals
- Personalization prompts with reasoning outputs
- Context vs Behavior Matrix applied to this use case
- Python implementation

**Resume bullet:** Applied the Context vs. Behavior Matrix to determine when to use prompt engineering vs RAG vs fine-tuning for personalization at scale

---

## 04 — LLM Evaluation Framework

**Folder:** `04-eval-framework/`

Automated eval suite that grades the Day 1 bot using an LLM as the grader. Builds a golden dataset of 20 question/answer pairs, runs responses through a structured rubric, and produces a scorecard with pass rates and failure analysis. No subjective review — everything is measurable and repeatable.

**What's inside:**
- 20-item golden dataset
- LLM-as-grader prompt with scoring rubric
- Eval runner script
- Sample scorecard with failure analysis
- Design decisions: what to measure and what to leave out

**Resume bullet:** Built automated LLM evaluation suites using LLMs-as-graders and curated golden datasets to replace subjective product assessments

---

## 05 — Agentic Shopping Assistant

**Folder:** `05-agentic-system/`

A multi-agent system with three specialized agents working in sequence: a search agent, a personalization agent, and a recommendation agent that drafts a personalized email. Built on the Agent Stack — Sense (multimodal input), Plan (LLM reasoning), Act (tool use). Demonstrates multi-agent orchestration, context passing, and deliberate tool access scoping.

**What's inside:**
- Full architecture doc with Mermaid diagram
- Orchestrator that coordinates all three agents
- Individual agent implementations
- Tool-use design doc: what each agent can and cannot do
- Multi-agent decision rationale

**Resume bullet:** Architected multi-agent systems using the Agent Stack — Sense, Plan, Act — with deliberate tool scoping and inter-agent context passing

---

## Skills Demonstrated

| Skill | Project |
|-------|---------|
| Prompt engineering and system design | 01, 03 |
| Embeddings and semantic search | 02 |
| RAG pipeline design | 02 |
| Context vs Behavior Matrix | 03 |
| LLM evaluation and golden datasets | 04 |
| LLMs-as-graders | 04 |
| Multi-agent orchestration | 05 |
| Tool use and agent scoping | 05 |
| Sense-Plan-Act architecture | 05 |

---

## Stack

- **LLMs:** Claude (Anthropic), OpenAI
- **Embeddings:** sentence-transformers, OpenAI embeddings
- **Frameworks:** Python, Anthropic SDK, OpenAI SDK
- **Tools:** Claude Code, Lovable, n8n

---

## Learning Log

Weekly notes on what I built, what surprised me, and what I'd do differently — see [LEARNING-LOG.md](./LEARNING-LOG.md)

---

*Built as part of the Maven AI Product Management Certification — May 2026*
