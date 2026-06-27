# Data Structures & Algorithms — Practical

**Phase:** 1 (Foundation) — **Lightweight version**  
**Prerequisites:** `05-Python-Core-for-Data-Engineering.md`  
**When to Skip:** Skip the LeetCode-hard stuff. Focus on the practical list below.  
**Projects This Enables:** Understanding why Spark does what it does, writing efficient transformations

## What to Cover (Practical Only)

### 1. Time & Space Complexity
- Big-O notation (O(1), O(n), O(n log n), O(n²))
- Amortized analysis (why Python list append is O(1))
- How to estimate memory usage

### 2. Essential Data Structures
- **Hash Maps (dicts):** O(1) lookup, used everywhere in data processing
- **Arrays/Lists:** Contiguous memory, indexing
- **Sets:** Uniqueness operations, O(1) membership testing
- **Trees:** File systems, database indexes (B-trees)
- **Graphs:** Data lineage, dependency graphs (Airflow DAGs are DAGs!)

### 3. Essential Algorithms
- **Sorting:** QuickSort, MergeSort (why Spark uses Timsort)
- **Searching:** Binary search (database indexes)
- **Hashing:** Consistent hashing (Kafka partitions, data sharding)
- **Two-pointer / Sliding window:** Stream processing patterns

### 4. What to SKIP (For Now)
- Dynamic programming
- Graph algorithms (BFS, DFS, Dijkstra) — return in Phase 6 for system design
- Greedy algorithms
- Advanced tree rotations (AVL, Red-Black)

## Hands-On Exercise

1. Implement a function that deduplicates a 10M row dataset using a hash set
2. Compare time complexity of `list.index()` vs `dict.get()`
3. Write a merge-join algorithm (this is what databases do)

## Why This Matters for Data Engineering

- Understanding why a Spark shuffle is expensive (it's sorting + merging)
- Why database indexes use B-trees (not hash maps for range queries)
- Why Kafka uses consistent hashing for partition assignment
- Writing efficient pandas/Spark operations

## Next File
→ `02-Data-Fundamentals/01-What-is-Data-Engineering.md`
