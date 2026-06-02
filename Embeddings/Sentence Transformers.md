
# Sentence Transformers (SBERT)

## Definition
Sentence Transformers (SBERT) are models that convert sentences, paragraphs, or documents into dense vector embeddings that capture semantic meaning.

They are built on top of BERT and are optimized for tasks like semantic similarity, search, and retrieval.

---

## Why Sentence Transformers?

Traditional BERT compares sentences pairwise, making similarity search slow.

Sentence Transformers generate embeddings once and then compare them using cosine similarity.

```text
Sentence
    ↓
SBERT
    ↓
Dense Embedding
```

---

## Example

```text
Sentence:
"I love machine learning"

Embedding:
[0.34, -0.21, 0.67, ...]
```

Similar sentences produce similar embeddings.

```text
"I love AI"
"I enjoy artificial intelligence"
```

→ High similarity score

---
## diagram
<img width="2000" height="697" alt="image" src="https://github.com/user-attachments/assets/920c6718-2dc2-4008-b830-4782e1b4962d" />

## Small Code Example

### Installation

```bash
pip install sentence-transformers
```

### Generate Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embedding = model.encode(
    "I love NLP"
)

print(embedding.shape)
```

---

## Semantic Similarity

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

emb1 = model.encode("I love AI")
emb2 = model.encode(
    "I enjoy artificial intelligence"
)

print(util.cos_sim(emb1, emb2))
```

### Output

```text
0.91
```

Higher score = more similar meaning.

---

## Applications

- Semantic Search
- RAG Systems
- Question Answering
- Recommendation Systems
- Duplicate Detection
- Document Retrieval

---

## Advantages

- Captures sentence meaning
- Fast similarity search
- Better than TF-IDF for semantic tasks
- Widely used in modern RAG pipelines

---

## Key Takeaways

- SBERT converts sentences into dense embeddings.
- Similar sentences have similar vectors.
- Commonly used for semantic search and retrieval.
- A core component of modern Vector Databases and RAG systems.
