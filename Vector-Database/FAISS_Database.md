# neural-grindset / LLM Concepts / FAISS.md

# FAISS (Facebook AI Similarity Search)

FAISS (Facebook AI Similarity Search) is an open‑source library developed by Meta's Fundamental AI Research (FAIR) team. It is purpose‑built for **efficient similarity search and clustering of dense vectors**. It is one of the most mature and popular approximate nearest neighbor (ANN) libraries, capable of searching **billion‑scale** vector sets entirely in memory on a **single server**.

## Core Positioning: Algorithm Library, Not a Database

FAISS is strictly an **algorithm library**, not a full‑fledged vector database. It focuses on one thing: **given a set of vectors, quickly find the ones most similar to a query vector**. It does **not** provide:

- HTTP API / network services
- CRUD operations (beyond limited add/remove)
- Data persistence (must manually save indexes to disk)
- Access control, multi‑tenancy, high availability, or replication

> **Analogy:** FAISS is like `scikit-learn` or `OpenCV` – a powerful algorithmic toolbox, not a production‑grade database system.

## Core Concepts

FAISS is built around the concept of an **Index**. An index is a data structure that stores a set of vectors and provides a search interface.

### Basic Workflow

1. **Build an Index** – Choose the appropriate index type.
2. **Train (optional)** – Some indexes (e.g., IVF, PQ) require training before vectors can be added.
3. **Add Vectors** – Populate the index with your vector data.
4. **Search** – Execute a similarity search against a query vector, returning the top‑k nearest vectors and their distances.

```text
Build Index → Train (optional) → Add Vectors → Search
     ↓              ↓                ↓            ↓
  Choose type    Learn params    Fill data    Get results
```
# Installation
FAISS provides pre‑built packages via Conda:
```
# CPU version
conda install -c pytorch faiss-cpu

# GPU version (CUDA support)
conda install -c pytorch faiss-gpu

# Or via pip
pip install faiss-cpu      # CPU version
pip install faiss-gpu      # GPU version
```
Code Examples

Basic Example: Brute‑Force Search
```
python

import faiss
import numpy as np

# 1. Generate synthetic data: 10,000 vectors of dimension 128
d = 128                           # Vector dimension
nb = 10000                        # Database size
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((1, d)).astype('float32')  # Query vector

# 2. Build index (exact L2 search)
index = faiss.IndexFlatL2(d)      # 
print(f"Index trained: {index.is_trained}")  # True (Flat doesn't need training)

# 3. Add vectors
index.add(xb)
print(f"Total vectors: {index.ntotal}")

# 4. Search: return the 4 nearest neighbours
k = 4
distances, indices = index.search(xq, k)
print(f"Distances: {distances}")
print(f"Indices: {indices}")
```
## IVF + PQ Combined Index (Billion‑Scale)
```
python
import faiss
import numpy as np

d = 128
nb = 1000000
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((1, d)).astype('float32')

# 1. Build IVF + PQ index
nlist = 4096              # Number of clusters
m = 16                    # Number of sub‑vectors (must divide d)
index = faiss.IndexIVFPQ(faiss.IndexFlatL2(d), d, nlist, m, 8)

# 2. Train the index (IVF and PQ both require training)
print(f"Trained before: {index.is_trained}")  # False
index.train(xb)
print(f"Trained after: {index.is_trained}")   # True

# 3. Add vectors
index.add(xb)

# 4. Search (tune nprobe to balance speed vs. accuracy)
index.nprobe = 10         # Number of clusters to probe during search
distances, indices = index.search(xq, k=4)
```

HNSW Index (No Training Required)
```
python
import faiss
import numpy as np

d = 128
nb = 100000
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((1, d)).astype('float32')

# HNSW does not require training
index = faiss.IndexHNSWFlat(d, 32)  # 32 = M parameter
index.add(xb)
distances, indices = index.search(xq, k=4)
```
Saving and Loading an Index from Disk
```
python
# Save index to disk
faiss.write_index(index, "my_index.faiss")

# Load index from disk
index_loaded = faiss.read_index("my_index.faiss")
```
