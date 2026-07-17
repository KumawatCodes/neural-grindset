
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

Documents → Chunk → Embed → Vector DB → Retrieve Top‑k → LLM → Answer

**Pipeline:**


| Pros ✅ | Cons ❌ |
|---------|---------|
| Easy to implement | Poor retrieval quality on noisy data |
| Great for prototypes | No query rewriting → mismatched semantics |
| Low latency | Fixed chunk size ignores structure |

> **When to use:** Quick prototypes, small/clean datasets, or educational demos.

---

### Advanced RAG

Adds optimizations **before** retrieval (query rewriting, HyDE) and **after** (reranking, contextual compression). Considered the new production baseline.

**Optimizations:**

| Stage | Techniques |
|-------|------------|
| **Pre‑retrieval** | Query rewriting, HyDE (Hypothetical Document Embeddings), query expansion |
| **Retrieval** | Hybrid search, multi‑query retrieval |
| **Post‑retrieval** | Reranking (cross‑encoders), contextual compression, LLM‑based filtering |

> **When to use:** Production systems with moderate complexity and quality requirements.

---

### Modular RAG

Separates retrieval and generation into **pluggable modules**. Swap retrievers, test rerankers, iterate fast – represents the third evolutionary stage after Naive and Advanced RAG.

┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Retriever │ ──→ │ Reranker │ ──→ │ Generator │
│ (pluggable)│ │ (pluggable)│ │ (pluggable)│
└─────────────┘ └─────────────┘ └─────────────┘

text

> **When to use:** Teams that iterate fast, A/B test different components, or need flexibility across multiple domains.

---

## 2. Retrieval‑Enhanced RAG Types

### Hybrid RAG

Combines **semantic (vector)** search with **lexical (BM25)** search. Vector covers meaning/synonyms; BM25 catches exact terms, IDs, and acronyms. Results are fused (e.g., Reciprocal Rank Fusion – RRF).

Query ──┬──────────────────┬─────────────────┐
│ │ │
▼ ▼ ▼
Vector Search BM25 Search Fuse (RRF)
(semantic) (exact match) │
│ │ │
└──────────────────┴─────────────────┘
│
▼
Top‑k Retrieved


> **When to use:** Enterprise RAG where both synonyms AND exact terms (e.g., product codes, legal citations) matter.

---

### Multi‑Query RAG

LLM generates multiple paraphrased versions of the original query; searches all; merges results → increases recall.

```python
queries = ["What is LoRA?", "Explain LoRA fine‑tuning", "LoRA adaptation method"]
results = [retriever.search(q) for q in queries]
merged = merge_results(results)
```
HyDE (Hypothetical Document Embeddings)
LLM first generates a "hypothetical" ideal answer document; its embedding is used for search – bridges the gap between short queries and long documents.

Query: "What is LoRA?"
   │
   ▼
LLM generates hypothetical answer:
"LoRA (Low‑Rank Adaptation) is a PEFT method..."
   │
   ▼
Embed the hypothetical answer → search vector DB

3. Reasoning & Agentic RAG Types
Agentic RAG
Moves from a linear pipeline to a reasoning loop. An autonomous agent:

Plans – breaks complex queries into subtasks.

Uses tools – vector search, web search, SQL, APIs.

Iterates – evaluates results, retries, resolves conflicts.

┌─────────────────────────────────────────────────────┐
│                   Agent Loop                         │
│                                                      │
│  ┌──────────┐   ┌──────────┐   ┌───────────────┐   │
│  │  Plan    │ ─→│ Execute  │ ─→│ Reflect/Decide│ ──┐│
│  │(decompose)│   │ (search) │   │  (evaluate)   │  ││
│  └──────────┘   └──────────┘   └───────────────┘  ││
│          ▲                                      │  ││
│          └──────────────────────────────────────┘  ││
└─────────────────────────────────────────────────────┘
