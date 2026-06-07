
# Cosine Similarity

Cosine similarity measures the cosine of the angle between two non‑zero vectors in an inner product space. It is widely used to compare **dense embeddings** (e.g., sentence vectors, word vectors) because it captures orientation (direction) rather than magnitude (length).

## Formula

For vectors **A** and **B**:

cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
= Σ(Ai × Bi) / (√Σ(Ai²) × √Σ(Bi²))



- **Numerator** – Dot product (sum of element‑wise products).
- **Denominator** – Product of Euclidean (L2) norms.

The result is a scalar between **-1** and **1** (for non‑negative embeddings like TF‑IDF or ReLU‑based vectors, it’s between 0 and 1).

## Interpretation

| Cosine Similarity | Angle (degrees) | Meaning                             |
|-------------------|----------------|-------------------------------------|
| 1.0               | 0°             | Identical direction (perfectly similar) |
| 0.5               | 60°            | Somewhat similar                    |
| 0.0               | 90°            | Orthogonal (no relation)            |
| -0.5              | 120°           | Somewhat opposite (rare in embeddings) |
| -1.0              | 180°           | Opposite direction                  |

> **Note:** For most text embeddings (e.g., SBERT, OpenAI), vectors are L2‑normalised so that `||A|| = 1`. Then cosine similarity simplifies to the dot product: `similarity = A · B`.

## Why Not Euclidean Distance?

| Metric          | Sensitive to magnitude? | Best for                         |
|-----------------|-------------------------|----------------------------------|
| Cosine          | No (only direction)     | Comparing semantically similar texts of different lengths |
| Euclidean       | Yes                     | Clustering points with similar “strength” (e.g., image features) |

**Example:**  
`"cat"` and `"cats"` embeddings may have similar direction but different lengths (due to frequency). Cosine ignores length; Euclidean would see them as far apart.

## Code Example (NumPy)

```python
import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot / (norm_a * norm_b)

# Example with dense embeddings
emb1 = [0.2, 0.8, 0.5]
emb2 = [0.3, 0.7, 0.6]
sim = cosine_similarity(emb1, emb2)
print(f"Cosine similarity: {sim:.4f}")   # e.g., 0.9912
```
Using scikit‑learn

```python
from sklearn.metrics.pairwise import cosine_similarity

# Shape: (n_samples, n_features)
sim_matrix = cosine_similarity([emb1, emb2])   # returns 2x2 matrix
```
