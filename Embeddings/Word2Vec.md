
# Word2Vec

## Definition
Word2Vec is a neural network-based technique that converts words into dense numerical vectors (embeddings) while preserving semantic meaning. Similar words are represented by similar vectors.

### Example

```text
King - Man + Woman ≈ Queen
```

---

## Why Word2Vec?

Traditional methods like BoW and TF-IDF:
- Ignore word meaning
- Create sparse vectors

Word2Vec:
- Captures semantic relationships
- Produces dense embeddings
- Understands word similarity

---

## Types of Word2Vec

### 1. CBOW (Continuous Bag of Words)
Predicts the target word using surrounding context words.

**Example:**

```text
I love machine learning

Input: I, machine, learning
Output: love
```

### 2. Skip-Gram
Predicts surrounding context words using a target word.

**Example:**

```text
Input: love
Output: I, machine
```

---

## Architecture

```text
Input Word
     ↓
Embedding Layer
     ↓
Hidden Layer
     ↓
Output Layer
```

The hidden layer learns word embeddings.

---

## Python Implementation

### Installation

```bash
pip install gensim
```

### Code

```python
from gensim.models import Word2Vec

sentences = [
    ["i", "love", "machine", "learning"],
    ["machine", "learning", "is", "fun"]
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=2,
    min_count=1
)

print(model.wv["learning"])
```

---

## Finding Similar Words

```python
model.wv.most_similar("learning")
```

### Output

```text
[('machine', 0.91)]
```

---

## Advantages

- Captures semantic meaning
- Dense vector representation
- Memory efficient
- Useful for NLP tasks

---

## Limitations

- One vector per word
- Cannot distinguish multiple meanings

Example:

```text
bank (river)
bank (financial)
```

Both get the same embedding.

---
## Diagram

<img width="1536" height="1024" alt="ChatGPT Image May 31, 2026, 01_32_32 PM" src="https://github.com/user-attachments/assets/30a40777-6765-4b45-b151-7088af8bed13" />

## Applications

- Text Classification
- Sentiment Analysis
- Chatbots
- Semantic Search
- Recommendation Systems

---

## Key Takeaways

- Word2Vec converts words into meaningful vectors.
- Similar words have similar embeddings.
- Two architectures: **CBOW** and **Skip-Gram**.
- Widely used in NLP and Deep Learning.
