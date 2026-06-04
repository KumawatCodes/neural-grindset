
# Dense Embeddings

Dense embeddings are vector representations where most (or all) dimensions contain **non‑zero** values. They map discrete objects (words, sentences, items) into a continuous, low‑dimensional space using learned neural networks.

## Key Characteristics

- **Dense** – Almost every dimension carries signal; very few or no zeros.
- **Low‑dimensional** – Typically 50–1024 dimensions (vs. vocabulary size of 50k+).
- **Learned** – Trained from data to capture semantic / functional relationships.
- **Continuous** – Real‑valued entries, e.g., `[0.23, -0.45, 0.67, …]`.

## Dense vs. Sparse Embeddings

| Feature                | Dense Embeddings                  | Sparse Embeddings                  |
|------------------------|-----------------------------------|-------------------------------------|
| Example                | Word2Vec, BERT                    | One‑hot, Bag‑of‑words, TF‑IDF       |
| Dimension              | Small (e.g., 300)                 | Large (e.g., 50k vocabulary)        |
| Zero entries           | Few / none                        | Mostly zeros                        |
| Storage                | Efficient                         | Inefficient (unless sparse format)  |
| Semantic similarity    | Cosine / dot product              | Limited (often overlap‑based)       |
| Training               | Neural network                    | Counting‑based (no training)        |

## How They Are Created

- **Word2Vec / GloVe** – From word co‑occurrence statistics.
- **BERT / Sentence‑Transformers** – Contextual embeddings from transformers.
- **Neural collaborative filtering** – Embed user & item IDs for recommendations.

## Why Use Dense Embeddings?

- **Semantic meaning** – Similar objects are close in vector space.  
  Example: `king - man + woman ≈ queen`
- **Downstream efficiency** – Work well with linear models, nearest‑neighbour indices (FAISS, HNSW), and neural networks.
- **Generalisation** – Models can infer relationships for unseen inputs.

## Common Applications

- **Semantic search** – Retrieve documents by meaning, not just keywords.
- **Recommendation systems** – Find items similar to a user’s preferences.
- **Clustering & anomaly detection** – Group or identify outliers in embedding space.
- **Transfer learning** – Pre‑trained embeddings boost small‑data tasks.

## Example (Word2Vec – 3D for illustration)

```python
# Dense vectors
king  = [0.25, 0.80, 0.12]
queen = [0.22, 0.78, 0.15]   # close to king
apple = [0.95, 0.10, 0.88]   # far from king
