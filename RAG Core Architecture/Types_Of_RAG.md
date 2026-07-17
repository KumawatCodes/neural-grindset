
# neural-grindset / LLM Concepts / RAGTypes.md

## Edit

# Types of RAG

RAG (Retrieval-Augmented Generation) has evolved far beyond the simple "retrieve‑then‑generate" pipeline. Today, there are dozens of RAG variants, each optimized for specific challenges: latency, reliability, multi‑step reasoning, structured data, and long documents.

This guide breaks down the major RAG types – from foundational to agentic and graph‑based – with clear explanations and selection criteria.

---

## RAG Type Comparison Table

| RAG Type | Core Concept | Best For |
|----------|--------------|----------|
| **Naive RAG** | Basic pipeline: retrieve top‑k chunks → LLM generates answer | Prototypes, small/clean datasets |
| **Advanced RAG** | Adds pre‑retrieval & post‑retrieval optimizations | Production systems with moderate complexity |
| **Hybrid RAG** | Combines vector (semantic) + lexical (BM25) search | Enterprise RAG where exact terms & synonyms both matter |
| **Modular RAG** | Pluggable, swappable components (retrievers, rerankers, fusion strategies) | Teams that iterate fast & need flexibility |
| **Agentic RAG** | Autonomous LLM agent decomposes queries, iterates, self‑corrects | Complex multi‑step questions requiring reasoning |
| **Graph RAG** | Uses knowledge graphs for structured, relationship‑aware retrieval | Queries about entity relationships & multi‑hop facts |
| **Multi‑hop RAG** | Chains multiple retrievals to answer questions requiring synthesizing facts from different sources | "Who is the CEO of the company that acquired X?" |
| **Self‑RAG** | Model emits reflection tokens to evaluate relevance & support; retries if needed | High‑reliability Q&A where hallucinations must be minimized |
| **Corrective RAG (CRAG)** | Adds reliability layer: if retrieval is ambiguous → web search; incorrect → discard & retry | Systems that need graceful failure handling |
| **Adaptive RAG** | Classifier predicts query complexity → routes to simple or complex pipeline | UX that needs sub‑3s responses for easy queries |
| **Fusion RAG** | Merges results from multiple retrievers or query variations before generation | Maximizing recall across diverse data sources |
| **Hierarchical RAG** | Multi‑level chunking (document → sections → paragraphs) preserves structure | Long industrial/legal documents with complex layouts |
| **Long‑context RAG** | Handles near‑infinite context via efficient indexing & retrieval | Scenarios where entire documents must be considered |

---

## 1. Foundational RAG Types

### Naive RAG

The simplest form: index documents → embed them → store vectors → retrieve top‑k → feed into LLM.

**Pipeline:**
