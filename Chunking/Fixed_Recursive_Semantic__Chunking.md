
# neural-grindset / LLM Concepts / ChunkingStrategies.md

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



### Implementation

```python
def fixed_size_chunk(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    """Simple fixed-size chunking with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        # Try to break at word boundary
        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space > chunk_size * 0.8:
                chunk = chunk[:last_space]
                end = start + last_space
        chunks.append(chunk.strip())
        start = end - overlap
    return chunks[reference:17]
```

## 2. Recursive Character Chunking
The default in most RAG stacks (LangChain, LlamaIndex). It uses a hierarchy of separators, trying larger structural units first and falling back to smaller ones until each chunk fits the size limit.

How It Works
The splitter tries separators in order: paragraph break → newline → sentence boundary → space → character.

Default separators: ["\n\n", "\n", ". ", " ", ""]

Document: "Paragraph 1.\n\nParagraph 2. Sentence A. Sentence B."
Step 1: Try "\n\n" → splits into paragraphs ✓ (fits size limit)
Step 2: If paragraph too large, try "\n"
Step 3: If still too large, try ". " (sentences)
Step 4: If still too large, try " " (words)
Step 5: Fallback to "" (characters)
