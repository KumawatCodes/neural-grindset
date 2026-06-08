
# Dot Product

The dot product (also called scalar product or inner product) is an algebraic operation that takes two equal‑length vectors and returns a single scalar. It is fundamental to dense embeddings – used in similarity scoring, attention mechanisms, and linear transformations.

## Definition

For vectors **a** and **b** of length `n`:

a · b = Σᵢ (aᵢ × bᵢ) = a₁b₁ + a₂b₂ + ... + aₙbₙ

text

Geometrically, the dot product equals the product of the vectors’ magnitudes (lengths) and the cosine of the angle θ between them:
a · b = ||a|| × ||b|| × cos(θ)

text

## Relationship to Cosine Similarity

Cosine similarity is the **normalised dot product**:

cosine_similarity(a, b) = (a · b) / (||a|| × ||b||)

text

| If vectors are…                     | Then dot product equals…                          |
|-------------------------------------|----------------------------------------------------|
| Raw (any length)                    | `||a|| × ||b|| × cos(θ)` (not normalised)         |
| L2‑normalised (||a|| = ||b|| = 1)   | **Cosine similarity** (directly)                  |
| Unit length and identical direction | `1.0` (maximum)                                   |
| Orthogonal (θ = 90°)                | `0`                                               |
| Opposite direction (θ = 180°)       | `-||a|| × ||b||` (minimum)                        |

## Code Examples

### Pure Python

```python
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

a = [0.2, 0.8, 0.5]
b = [0.3, 0.7, 0.6]
print(dot_product(a, b))   # 0.2*0.3 + 0.8*0.7 + 0.5*0.6 = 0.92
NumPy (fast)
python
import numpy as np

a = np.array([0.2, 0.8, 0.5])
b = np.array([0.3, 0.7, 0.6])

# Method 1
dot = np.dot(a, b)          # 0.92

# Method 2
dot = a @ b                 # Python 3.5+ (matrix multiplication operator)

# Method 3
dot = np.sum(a * b)         # element‑wise multiply then sum
