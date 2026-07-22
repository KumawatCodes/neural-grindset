
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

## Parent–Child Chunking

```text
Document
   │
   ▼
┌──────────────────────────────────────────────────────────────┐
│ Parent Chunk (1500–3000 tokens)                              │
│                                                              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │ Child 1  │ │ Child 2  │ │ Child 3  │ │ Child 4  │          │
│ │200–400   │ │200–400   │ │200–400   │ │200–400   │          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└──────────────────────────────────────────────────────────────┘

Retrieval:
Query → finds Child 2 → returns Parent Chunk (full context)
```
Retrieval: Query → finds Child 2 → returns Parent chunk (full context)


### Implementation (Conceptual)

```python
from typing import List, Tuple

class HierarchicalChunker:
    def __init__(
        self,
        child_size: int = 300,
        parent_size: int = 2000,
        overlap: int = 50
    ):
        self.child_size = child_size
        self.parent_size = parent_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> List[Tuple[str, str]]:
        """
        Returns list of (child_chunk, parent_chunk) pairs.
        Multiple children share the same parent.
        """
        # 1. Split into parent chunks (large, e.g., 2000 tokens)
        parent_chunks = self._split_by_size(text, self.parent_size, self.overlap)
        
        result = []
        for parent in parent_chunks:
            # 2. Split each parent into child chunks (small, e.g., 300 tokens)
            children = self._split_by_size(parent, self.child_size, self.overlap)
            for child in children:
                result.append((child, parent))
        
        return result
    
    def _split_by_size(self, text: str, size: int, overlap: int) -> List[str]:
        # Simplified: recursive splitter logic
        pass

# Usage
chunker = HierarchicalChunker(child_size=300, parent_size=2000)
chunks = chunker.chunk(long_document)
# Each chunk: (child_text, parent_context)
```

How It Works
Split into paragraphs on \n{2,}

Split into sentences on [.!?]\s+ (with abbreviation handling)

Greedy-pack sentences into a chunk while token count ≤ max_tokens

If a single sentence exceeds max_tokens: slice it at token boundaries (BPE)

Apply overlap by re-prepending the last N tokens of each chunk to the next
```
Sentence Sequence: [S1(100t)] [S2(150t)] [S3(200t)] [S4(80t)] [S5(250t)]
max_tokens = 400

Chunk 1: [S1(100)] + [S2(150)] + [S3(200)] = 450t (too big!)
          → [S1(100)] + [S2(150)] = 250t ✅
Chunk 2: [S3(200)] + [S4(80)] = 280t ✅
Chunk 3: [S5(250)] = 250t ✅ (single sentence, within limit)
```
Implementation (snipsplit)
The snipsplit library implements token-aware chunking efficiently in Rust with a Python frontend:

```python
from snipsplit import Chunker

# Initialize with token budget and overlap
chunker = Chunker(
    max_tokens=512,           # Max tokens per chunk
    overlap_tokens=64,        # Overlap between chunks
    encoding="cl100k_base"    # OpenAI's tokenizer (or "o200k_base")
)

text = open("long_document.txt").read()

# Split into token-aware chunks
for chunk in chunker.split(text):
    print(f"Tokens: {chunk.token_count}, Start: {chunk.start}, End: {chunk.end}")
    print(chunk.text[:60])
```
## Algorithm Steps
```
1. Split text into paragraphs (\n{2,})
2. Split paragraphs into sentences ([.!?]\s+ with abbreviation handling)
3. Greedy-pack sentences while running token count <= max_tokens
4. If single sentence > max_tokens, slice at token boundaries (BPE)
5. Apply overlap_tokens by re-prepending last N tokens to next chunk
6. Drop chunks shorter than min_tokens
```
