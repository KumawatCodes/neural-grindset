
# neural-grindset / LLM Concepts / ChunkingStrategies.md

# Chunking Strategies: Hierarchical, Token-Aware & Adaptive

Following the foundational and intermediate strategies (Fixed, Recursive, Semantic, Sentence, Paragraph, Sliding Window), this guide covers three advanced approaches that address **structural integrity**, **token budget precision**, and **dynamic strategy selection**. These strategies are essential for production-grade RAG systems dealing with complex, heterogeneous document corpora.

---

## Chunking Strategy Comparison (Complete Reference)

| Strategy | Best For | Granularity | Context Preservation | Overhead | Implementation Complexity |
|----------|----------|-------------|----------------------|----------|---------------------------|
| **Fixed-Size** | Log files, prototyping | Token/Character | Low | None | Very Low |
| **Recursive** | General articles, default | Hierarchical | Medium | None | Low |
| **Semantic** | Research papers, tech docs | Topic-bound | Very High | High (embeddings) | High |
| **Sentence** | NER, sentiment, short QA | Grammatical | Very Low | None | Low |
| **Paragraph** | Topic-based retrieval | Topical | High | None | Very Low |
| **Sliding Window** | Context-heavy QA | Rolling context | Very High | High (duplicates) | Medium |
| **Hierarchical** | Structured docs, legal/medical | Parent-Child | High (with full context) | Medium (dual storage) | Medium |
| **Token-Aware** | Token-budget constrained | Token-precise | Medium-High | Low | Medium |
| **Adaptive** | Heterogeneous corpora | Per-document optimal | Strategy-dependent | High (evaluation) | High |

---

## 7. Hierarchical Chunking

Hierarchical (Parent-Child) chunking creates a **two-level (or multi-level) structure**: fine-grained **child** chunks for precise retrieval, and larger **parent** chunks that provide broader context during generation[reference:0].

### How It Works

1. **Document is split** into small, semantically coherent **child chunks** (e.g., 200–400 tokens).
2. **Child chunks are indexed** and embedded for retrieval.
3. **Larger parent chunks** (e.g., 1500–3000 tokens) are stored with references to their children[reference:1].
4. **At query time**: retrieve relevant child chunks, then fetch their parent chunks to provide full context for generation[reference:2].

Document
│
▼
┌─────────────────────────────────────────────────────┐
│ Parent Chunk (1500-3000 tokens) │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Child 1 │ │ Child 2 │ │ Child 3 │ │ Child 4 │ │
│ │(200-400)│ │(200-400)│ │(200-400)│ │(200-400)│ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────┘

Retrieval: Query → finds Child 2 → returns Parent chunk (full context)
