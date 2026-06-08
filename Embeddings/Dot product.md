
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
