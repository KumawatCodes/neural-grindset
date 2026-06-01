
### Embeddings

## What are Embeddings?

Embeddings are dense numerical vector representations of words, sentences, or documents that capture their semantic meaning.

Unlike Bag of Words or TF-IDF, embeddings can understand relationships between words.

### Example

```text
King  → [0.25, -0.12, 0.87, ...]
Queen → [0.23, -0.10, 0.85, ...]
```

Similar words have similar vectors.

---

# 1. Word2Vec

## Definition
Word2Vec is a neural network-based embedding technique that learns word representations from surrounding context.

### Types
- CBOW (Predict target word from context)
- Skip-Gram (Predict context from target word)

### Example

```text
King - Man + Woman ≈ Queen
```

### Advantages
- Captures semantic meaning
- Fast and efficient
- Dense vector representation

### Limitation
Produces only one embedding per word.

Example:

```text
bank (river)
bank (financial)
```

Both receive the same vector.

---

# 2. GloVe

## Full Form
Global Vectors for Word Representation

## Definition
GloVe is a word embedding technique developed by Stanford that combines global word co-occurrence statistics with vector learning.

### Key Idea

Words that appear in similar contexts should have similar embeddings.

### Example

```text
ice ↔ cold
steam ↔ hot
```

The model learns these relationships from word co-occurrence frequencies.

### Advantages
- Captures global context
- Better semantic relationships
- Pretrained embeddings widely available

### Limitation
Cannot handle unseen words.

---

# 3. FastText

## Definition
FastText is an extension of Word2Vec developed by Facebook that represents words using character n-grams.

### Example

Word:

```text
learning
```

Character n-grams:

```text
lea
ear
arn
rni
nin
ing
```

The final embedding is built using these subwords.

### Advantages
- Handles rare words
- Handles unseen words (OOV)
- Works well for morphologically rich languages

### Example

Even if the model has never seen:

```text
learnable
```

it can still generate an embedding using character n-grams.

### Limitation
Slightly larger model size compared to Word2Vec.

---

# Comparison

| Feature | Word2Vec | GloVe | FastText |
|----------|----------|--------|----------|
| Uses Context | ✅ | ✅ | ✅ |
| Uses Global Statistics | ❌ | ✅ | ❌ |
| Handles Rare Words | ❌ | ❌ | ✅ |
| Handles Unseen Words | ❌ | ❌ | ✅ |
| Uses Character Information | ❌ | ❌ | ✅ |
| Training Speed | Fast | Medium | Fast |

---

# Key Takeaways

- **Word2Vec** learns embeddings using surrounding words.
- **GloVe** learns embeddings using global word co-occurrence statistics.
- **FastText** learns embeddings using character n-grams and can handle unseen words.
- FastText is generally preferred when dealing with rare or out-of-vocabulary words.
