
# Sparse Embeddings

Sparse embeddings are vector representations where the vast majority of the dimensions contain **zero** values. Instead of mapping text into a dense, low-dimensional continuous space, sparse embeddings map objects (words, phrases, or documents) into a massive, high-dimensional space where each dimension typically corresponds to a specific word or token in a dictionary.

## ## Key Characteristics

* **Sparse:** Only a fraction of the total dimensions carry a signal (non-zero weights); the rest are completely empty (zeros).
* **High-dimensional:** Typically spans 30,000 to 100,000+ dimensions (matching the size of a model's vocabulary or corpus dictionary).
* **Exact Matching:** Phenomenal at catching exact keyword matches, serial numbers, product IDs, and domain-specific acronyms.
* **Interpretable:** Each non-zero weight directly corresponds to a specific token or term, unlike dense dimensions which are abstract features.

---

## ## Dense vs. Sparse Embeddings

| Feature | Dense Embeddings | Sparse Embeddings |
| :--- | :--- | :--- |
| **Example Algorithms** | Word2Vec, BERT, text-embedding-3 | BM25, TF-IDF, SPLADE |
| **Dimensionality** | Small/Medium (e.g., 256 to 1536) | Extremely Large (e.g., 30,000+) |
| **Zero Entries** | Few or none (dense values everywhere) | Mostly zeros (>95% empty) |
| **Primary Strength** | Semantic similarity, synonyms, context | Keyword relevance, exact matches, IDs |
| **Storage Strategy** | Fixed-size arrays | Inverted indices or Coordinate/CSR format |
| **Training Type** | Deep neural networks (Representation) | Statistical counting or Neural masking |

---

## ## Popular Models & Approaches

### 1. Traditional Statistical Methods
* **TF-IDF (Term Frequency-Inverse Document Frequency):** Weighs words based on how often they appear in a document relative to how common they are across the whole dataset.
* **BM25 (Best Matching 25):** The gold standard for keyword retrieval, optimizing TF-IDF with document length normalization and term frequency saturation limits.

### 2. Modern Neural Sparse Models
* **SPLADE (Sparse Lexical and Expansion):** Uses a masked language model (like BERT) to predict and weight words from the entire vocabulary, even expanding documents with relevant synonyms that weren't originally in the text.
* **BGE-M3 Sparse:** A highly versatile modern multi-lingual model capable of outputting dense, sparse, and multi-vector representations simultaneously.

---

## ## Practical Code Example

Here is a complete, self-contained Python implementation using `scikit-learn` to extract sparse vectors, convert them into an efficient memory footprint, and format them for production vector search databases.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Define a sample corpus
corpus = [
    "Deep learning models use dense embeddings for semantic search.",
    "Keyword matching algorithms rely heavily on sparse embeddings.",
    "Hybrid search combines both dense and sparse vectors for optimal retrieval."
]

print("--- 📝 Processing Corpus ---")
# 2. Initialize the sparse vectorizer (using word tokens)
vectorizer = TfidfVectorizer()
sparse_matrix = vectorizer.fit_transform(corpus)
vocab = vectorizer.get_feature_names_out()

print(f"Total Dictionary Vocabulary Size: {len(vocab)} dimensions")
print(f"Extracted Vocabulary Terms:\n{list(vocab)}\n")

# 3. Inspect a specific document vector (Document index 1)
doc_idx = 1
sample_vector = sparse_matrix[doc_idx]

print(f"--- 📊 Sparse Vector Breakdown for Doc {doc_idx} ---")
print(f"Raw Dense Array View (mostly zeros):")
print(np.round(sample_vector.toarray()[0], 2))

# 4. Convert to Vector DB format (Indices & Values)
# Production engines like Qdrant/Pinecone only store the non-zero positions to save memory.
non_zero_indices = sample_vector.indices
non_zero_values = sample_vector.data

sparse_payload = {
    "indices": non_zero_indices.tolist(),
    "values": np.round(non_zero_values, 4).tolist()
}

print("\n🚀 Production-Ready Vector Payload Format:")
print(sparse_payload)

# Map indices back to words to show interpretability
print("\n🔍 Meaning of Non-Zero Dimensions:")
for idx, val in zip(sparse_payload["indices"], sparse_payload["values"]):
    print(f"  • Token ID {idx:02d} ['{vocab[idx]}'] -> Weight: {val}")
