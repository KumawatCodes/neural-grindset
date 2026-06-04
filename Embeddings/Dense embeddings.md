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

## Popular Dense Embedding Models

| Model / Family        | Output type         | Dims (typical) | Key feature                        |
|-----------------------|---------------------|----------------|-------------------------------------|
| Word2Vec / GloVe      | Static word vectors | 100–300        | One vector per word (no context)    |
| FastText              | Subword‑aware       | 100–300        | Handles OOV with character n‑grams  |
| BERT (CLS token)      | Contextual sentence | 768–1024       | Bidirectional transformer           |
| Sentence‑BERT (SBERT) | Sentence similarity | 384–768        | Optimised for cosine similarity     |
| Instructor            | Task‑aware          | 768            | Instruction‑tuned embeddings        |
| OpenAI `text-embedding-3` | API‑based      | 256–3072       | Large‑scale, proprietary            |

## How They Are Created

### Static embeddings (Word2Vec)

- Train a shallow neural network to predict a word from its neighbours (CBOW) or neighbours from a word (Skip‑gram).
- The hidden layer weights become the embedding matrix.

### Contextual embeddings (BERT)

- Fine‑tune a transformer with masked language modelling (MLM) and next‑sentence prediction.
- Extract hidden states from the final layer, then pool (e.g., `[CLS]` token or mean pooling).

### Sentence‑Transformers

- Start from a pre‑trained BERT.
- Fine‑tune with siamese networks on natural language inference (NLI) or sentence similarity datasets (e.g., STS‑Benchmark).
- Result: semantically meaningful sentence embeddings where cosine similarity correlates with human judgement.

## Training Details (For the Curious)

- **Loss functions** – Triplet loss, contrastive loss (InfoNCE), multiple negatives ranking (MNR), cosine embedding loss.
- **Negative sampling** – Essential for scalability (e.g., Word2Vec uses 5–20 negatives per positive).
- **Hard negatives** – Mining difficult examples improves quality (e.g., in retrieval tasks).
- **Normalisation** – Often embeddings are L2‑normalised so that dot product equals cosine similarity.

## Evaluation Metrics for Embeddings

| Task                  | Metrics                                       |
|-----------------------|-----------------------------------------------|
| Word similarity       | Spearman correlation (e.g., on SimLex-999)    |
| Sentence similarity   | Pearson / Spearman (STS‑Benchmark)            |
| Retrieval (IR)        | NDCG@k, Recall@k, MRR, MAP                    |
| Clustering            | V‑measure, adjusted Rand index                |
| Downstream tasks      | Accuracy, F1 (e.g., on GLUE tasks)            |

## Practical Code Example (Sentence‑Transformers)

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')   # 384-dim dense embeddings

sentences = ["A man is playing guitar", "Someone is strumming a musical instrument"]
embeddings = model.encode(sentences)  # shape: (2, 384)

# Cosine similarity
cos_sim = util.cos_sim(embeddings[0], embeddings[1])
print(cos_sim)  # ~0.85 (semantically similar)

# Search example
query = "guitar performance"
query_emb = model.encode(query)
results = util.semantic_search(query_emb, embeddings, top_k=2)
