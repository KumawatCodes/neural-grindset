# RAG (Retrieval-Augmented Generation)

RAG (Retrieval-Augmented Generation) is an architecture that enhances large language models by **retrieving relevant information from an external knowledge base** and incorporating it into the prompt before generation. Instead of relying solely on the model's internal (and often outdated) parameters, RAG grounds the response in real, factual, and up-to-date data.

## Core Idea

Retrieve → Augment → Generate
↓ ↓ ↓
Search Inject LLM produces
external retrieved answer with
data context citations


Instead of asking the model: *"What is the answer?"*  
RAG asks: *"What is the answer, based on these specific documents I just found?"*

## Why RAG? (The Three Core Problems It Solves)

LLMs, despite their power, have fundamental limitations that RAG directly addresses:

### 1. Knowledge Cutoff (Stale Information)

LLMs are frozen at their training date. A model trained in 2023 has **zero knowledge** of:

- Recent news, events, or discoveries (e.g., "Who won the 2026 World Cup?")
- New product releases or API updates
- Latest research papers or regulations

**RAG fix:** Point the retriever to a freshly updated database (news feeds, company wikis, live APIs) – the model instantly becomes "current" without retraining.

### 2. Hallucinations (Confident Falsehoods)

LLMs are next-token predictors, not fact-checkers. When unsure, they **generate plausible-sounding but incorrect information** – complete with convincing citations that don't exist.

**Example:**
