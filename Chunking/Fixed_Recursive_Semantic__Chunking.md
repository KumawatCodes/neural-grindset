
# neural-grindset / LLM Concepts / ChunkingStrategies.md

## Edit

# Chunking Strategies: Fixed, Recursive & Semantic

Chunking is the process of breaking down large documents into smaller, manageable pieces before they are embedded and indexed in a vector database[reference:0]. The way you split documents has a **larger impact on retrieval quality than almost any other decision** in the RAG pipeline[reference:1].

The core tension is straightforward[reference:2]:

- **Chunks too small** → each vector represents only a fragment. Retrieval returns pieces that lack context.
- **Chunks too large** → each vector averages across many topics. Irrelevant content fills the context window.

> **The Goldilocks Problem:** There is no universally correct chunk size. The right size depends on your document type, query patterns, and embedding model[reference:3].

---

## Strategy Comparison

| Strategy | Best For | Chunk Quality | Implementation Complexity | Ingest Cost |
|----------|----------|---------------|---------------------------|-------------|
| **Fixed-Size** | Log files, structured data, quick prototyping[reference:4] | Low-Medium[reference:5] | Simple[reference:6] | Lowest[reference:7] |
| **Recursive** | General articles, mixed content, default starting point[reference:8] | Medium[reference:9] | Simple【6L10】 | Low[reference:10] |
| **Semantic** | Technical docs, research papers, content with natural topic boundaries[reference:11] | High[reference:12] | Medium[reference:13] | 5-15× fixed[reference:14] |

---

## 1. Fixed-Size Chunking

The simplest and most common approach: split text into chunks of a fixed number of tokens or characters, with optional overlap between adjacent chunks[reference:15].

### How It Works

A sliding window moves through the document producing chunks of equal size. A 10-20% overlap means the last part of one chunk repeats as the first part of the next, reducing the chance of splitting a key sentence across chunk boundaries[reference:16].

Document: [The quick brown fox jumps over the lazy dog. The dog slept.]
Chunk 1 (size=20): "The quick brown fox jum"
Chunk 2 (size=20): "umps over the lazy dog."
↑ Splits mid-word (bad!)
