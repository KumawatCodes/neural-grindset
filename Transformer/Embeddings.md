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
