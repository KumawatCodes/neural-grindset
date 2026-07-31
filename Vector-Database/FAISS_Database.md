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
