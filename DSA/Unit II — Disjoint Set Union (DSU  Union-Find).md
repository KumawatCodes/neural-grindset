
---

## What is DSU?

DSU is a data structure that tracks a collection of elements partitioned into **disjoint (non-overlapping) sets**. It answers one question efficiently: "Do two elements belong to the same set?"

Two core operations:

- **Find(x)** — returns the representative (root) of the set containing x.
- **Union(x, y)** — merges the sets containing x and y.

Use cases: Kruskal's MST, detecting cycles in undirected graphs, connected components, network connectivity.

---

## Naive Implementation (No Optimization)

Use a `parent[]` array where `parent[i] = i` initially (each element is its own set).

**Find:** Follow parent pointers until `parent[x] == x`. **Union:** Set parent of one root to the other.

**Problem:** Without optimization, trees can become a chain (like a linked list) → Find takes O(n) per call → total O(n²) for n operations. This is the degenerate case.

```
// Q: Implement naive union-find without any optimization


```

---

## Why We Use `parent[]` and `rank[]`

**parent[]** stores the representative of each element's set. It's the core structure — without it, you have no way to trace which set an element belongs to.

**rank[]** (or size[]) is used to keep trees shallow. Without rank, repeatedly unioning sets can create a chain of height n. rank stores an upper bound on the tree height so we always attach the shorter tree under the taller one.

**Why rank and not actual height?** Tracking actual height after path compression is complex. Rank is an upper bound that's cheap to maintain and gives the same asymptotic guarantees.

---

## Union by Rank

When merging two sets, attach the root of the **smaller rank** tree under the root of the **larger rank** tree.

Rule:

- If rank[x] < rank[y] → parent[x] = y
- If rank[x] > rank[y] → parent[y] = x
- If rank[x] == rank[y] → parent[x] = y (or either), rank[y]++

**Why increment rank only when ranks are equal?** When two trees of equal height merge, the resulting tree is one level taller. If heights differ, the taller tree absorbs the shorter one with no height increase.

**Edge case:** Never increment rank after path compression. Path compression makes the tree flatter but we don't update rank (that's why rank is an upper bound, not exact height).

```
// Q: Implement union by rank


```

---

## Path Compression

During Find, make every node on the path point directly to the root.

**Why?** Future Find calls on those nodes become O(1) instead of O(depth).

Two variants:

1. **Full path compression (two-pass):** First pass finds root, second pass updates all nodes.
2. **Path halving (one-pass):** Make every node point to its grandparent. Slightly simpler, same amortized complexity.

**Why does path compression not break the structure?** The representative (root) of the set doesn't change — only intermediate pointers are shortcut. The root still correctly identifies the set.

```
// Q: Implement find with path compression


```

---

## Combined: Union by Rank + Path Compression

Together they give amortized **O(α(n))** per operation, where α is the inverse Ackermann function. For all practical values of n, α(n) ≤ 4. This is effectively O(1) amortized.

**Why use both together?**

- Path compression alone: good amortized complexity but rank matters for worst case.
- Union by rank alone: O(log n) per operation.
- Together: nearly O(1) amortized — the best achievable.

```
// Q: Full DSU with union by rank and path compression


```

---

## Cycle Detection Using DSU

For an undirected graph, process each edge (u, v):

- If Find(u) == Find(v) → they're in the same set → adding this edge creates a cycle.
- Else → Union(u, v).

**Why does same representative mean a cycle?** If both endpoints are already connected (same component), adding another edge between them creates an extra path → cycle.

```
// Q: Detect cycle in undirected graph using DSU


```

---

## Edge Cases and Failure Points

- **Self-loop:** Edge (u, u) — Find(u) == Find(u) always → detected as cycle correctly.
- **Disconnected graph:** DSU handles it naturally; separate components have different roots.
- **Union of already-same-set:** Safe to call, just does nothing useful (no structural change, rank doesn't increase).
- **Find on uninitialized parent:** Always initialize parent[i] = i and rank[i] = 0 for all i.

---

## Complexity Table

|Operation|Naive|With Rank Only|With Compression Only|Both (Rank + Compression)|
|---|---|---|---|---|
|Find|O(n) worst|O(log n)|O(log n) amortized|O(α(n)) amortized|
|Union|O(n) worst|O(log n)|O(log n) amortized|O(α(n)) amortized|
|Space|O(n)|O(n)|O(n)|O(n)|
|Build (n unions)|O(n²)|O(n log n)|O(n log n)|O(n α(n)) ≈ O(n)|

α(n) = inverse Ackermann function. For n ≤ 10^600, α(n) ≤ 4.

---

## Quick Viva Q&A

**Q: Why do we need a separate rank array? Can't we just use the parent array?** No. The parent array encodes the tree structure. Rank is metadata about tree height — mixing them would lose structural information.

**Q: After path compression, is the rank still accurate?** No, rank becomes an upper bound, not the exact height. That's intentional — keeping exact height is expensive, and rank as upper bound still guarantees O(log n) tree height before compression.

**Q: Can DSU handle weighted unions (like merging groups with counts)?** Yes — replace rank with size. Attach smaller-size tree under larger-size tree. Update size of new root as sum of both. This is "union by size."

**Q: Why is path compression applied during Find and not during Union?** Union only looks at roots (which are found via Find). Path compression happens along the path from a node to its root, which only occurs during Find traversal.

**Q: What's the difference between DSU and BFS/DFS for connectivity?** BFS/DFS: O(V+E) per query, works on static or dynamic graphs, gives full traversal info. DSU: O(α(n)) amortized per query, best for dynamic edge additions and simple connectivity checks. DSU is preferred when you're adding edges incrementally.

**Q: Can DSU detect cycles in a directed graph?** Not directly. DSU-based cycle detection assumes undirected edges. For directed graphs, use DFS with coloring (white/gray/black).