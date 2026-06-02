# Embeddings

## What are Embeddings?

Embeddings are dense vector representations of words that capture semantic meaning and relationships between words.

Example:

```text
King - Man + Woman ≈ Queen
```

---

# 1. Word2Vec

## Definition
Word2Vec is a neural network-based technique that learns word embeddings from surrounding context words.

### Types
- CBOW
- Skip-Gram

### Small Code

```python
from gensim.models import Word2Vec

sentences = [["i","love","nlp"]]

model = Word2Vec(
    sentences,
    vector_size=50,
    min_count=1
)

print(model.wv["nlp"])
```

### Advantages
- Fast
- Captures semantic meaning

### Limitation
One embedding per word.

---

# 2. GloVe

## Full Form
Global Vectors for Word Representation

## Definition
GloVe learns embeddings using word co-occurrence statistics from the entire corpus.

### Small Code

```python
import gensim.downloader as api

glove = api.load("glove-wiki-gigaword-50")

print(glove["king"])
```

### Advantages
- Captures global context
- Good semantic relationships

### Limitation
Cannot handle unseen words.

---

# 3. FastText

## Definition
FastText extends Word2Vec by using character n-grams to create embeddings.

### Small Code

```python
from gensim.models import FastText

sentences = [["i","love","nlp"]]

model = FastText(
    sentences,
    vector_size=50,
    min_count=1
)

print(model.wv["nlp"])
```

### Advantages
- Handles rare words
- Handles unseen words (OOV)

### Example

```text
learning
learned
learner
```

FastText understands similarities because it uses character information.

### Limitation
Larger model size than Word2Vec.

---

# Comparison

| Feature | Word2Vec | GloVe | FastText |
|----------|----------|--------|----------|
| Context Based | ✅ | ✅ | ✅ |
| Global Statistics | ❌ | ✅ | ❌ |
| Handles Rare Words | ❌ | ❌ | ✅ |
| Handles Unseen Words | ❌ | ❌ | ✅ |
| Character N-grams | ❌ | ❌ | ✅ |

---

## Key Takeaways

- **Word2Vec** → Learns from context words.
- **GloVe** → Learns from word co-occurrence statistics.
- **FastText** → Learns from character n-grams and handles unseen words.

# Sentence Transformers & Dense Embeddings

## 1. Dense Embeddings

### Definition
Dense embeddings are low-dimensional numerical vectors that capture the semantic meaning of text.

Unlike TF-IDF or Bag of Words, dense embeddings understand context and meaning.

### Example

```text
"I love AI"
      ↓
[0.23, -0.45, 0.81, ...]
```

### Advantages
- Captures semantic meaning
- Compact representation
- Useful for similarity search
- Works well in RAG systems

### Similarity Example

```python
from sentence_transformers import util

score = util.cos_sim(vec1, vec2)
print(score)
```

---

## 2. Sentence Transformers

### Definition
Sentence Transformers (SBERT) are models that convert entire sentences, paragraphs, or documents into dense embeddings.

Built on top of BERT, they are optimized for semantic similarity tasks.

### Example

```text
Sentence:
"I love machine learning"

Embedding:
[0.34, -0.21, 0.67, ...]
```

---

## Why Sentence Transformers?

Traditional BERT:

```text
Sentence A + Sentence B
       ↓
      BERT
```

Requires comparing sentences one pair at a time.

Sentence Transformers:

```text
Sentence A → Embedding A
Sentence B → Embedding B

Cosine Similarity(A,B)
```

Much faster for retrieval and search.

---

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

## Semantic Similarity Example

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

emb1 = model.encode(
    "I love AI"
)

emb2 = model.encode(
    "I enjoy artificial intelligence"
)

print(
    util.cos_sim(emb1, emb2)
)
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

## Dense vs Sparse Embeddings

| Feature | Sparse (TF-IDF) | Dense Embeddings |
|----------|----------|----------|
| Captures Meaning | ❌ | ✅ |
| Vector Size | Large | Small |
| Semantic Search | ❌ | ✅ |
| Used in RAG | Limited | ✅ |

---

## Key Takeaways

- **Dense Embeddings** are compact vectors that capture semantic meaning.
- **Sentence Transformers (SBERT)** generate embeddings for entire sentences and documents.
- Similar texts have similar embeddings.
- Widely used in **Semantic Search**, **Vector Databases**, and **RAG pipelines**.
