
# Hybrid Embeddings

Hybrid embeddings combine two or more complementary representation techniques to improve retrieval, similarity, or downstream task performance. The most common flavour is **dense + sparse** (neural + bag‑of‑words), but hybrids can also mix static + contextual, word + subword, or late interaction mechanisms like ColBERT.

## Why Hybrid?

- **Semantic + lexical** – Dense handles meaning, synonyms, paraphrasing; sparse handles exact matches, rare terms, and out‑of‑domain keywords.
- **Better zero‑shot** – Sparse provides a safety net when dense models encounter unfamiliar concepts.
- **Interpretability** – Sparse contributions can be highlighted (e.g., which exact terms matched).
- **Performance boost** – Many retrieval benchmarks show hybrid outperforms either alone (e.g., BM25 + DPR).

## Common Hybrid Strategies

| Strategy                     | Components                         | How they combine                     |
|------------------------------|------------------------------------|--------------------------------------|
| Score fusion (linear)        | Dense + sparse (e.g., BM25)        | Weighted sum of normalised scores    |
| Reciprocal Rank Fusion (RRF) | Multiple rankers (any embeddings)  | `RRF = Σ 1/(k + rank)`               |
| Concatenated vectors         | Dense + sparse (projected)         | Combine vectors after dimension reduction |
| Late interaction             | Term‑level dense + query term scores | ColBERT: MaxSim over token embeddings |
| Model ensemble               | Two separate encoders              | Average logits / probabilities       |

## Dense + Sparse Hybrid (Most Popular)

### Architecture (ASCII)

```text
Query ──┬──────────────────┬─────────────────┬──────────┐
        │                  │                 │          │
        ▼                  ▼                 ▼          ▼
   [Dense Encoder]    [Sparse Encoder]   [Dense Enc.]  [Sparse Enc.]
   (e.g., SBERT)      (e.g., BM25/TF‑IDF)   (same)       (same)
        │                  │                 │            │
        ▼                  ▼                 ▼            ▼
   dense_q_vec         sparse_q_vec      dense_d_vec   sparse_d_vec
        │                  │                 │            │
        └─────────┬────────┘                 └──────┬─────┘
                  ▼                                 ▼
           dense_similarity                   sparse_similarity
           (cosine / dot)                     (e.g., dot over sparse)
                  │                                 │
                  └──────────────┬──────────────────┘
                                 ▼
                    Score Fusion (weighted sum / RRF)
                                 │
                                 ▼
                           final relevance
