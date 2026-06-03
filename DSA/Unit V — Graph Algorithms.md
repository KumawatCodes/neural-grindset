
## Graph Representations

**Adjacency Matrix:** 2D array `adj[V][V]`. `adj[i][j] = 1` if edge exists.

- Space: O(V²)
- Check edge: O(1)
- Get all neighbors: O(V)
- Use when: dense graph (E ≈ V²), or need fast edge lookup.

**Adjacency List:** Array of vectors/lists. `adj[i]` contains all neighbors of i.

- Space: O(V + E)
- Check edge: O(degree)
- Get all neighbors: O(degree)
- Use when: sparse graph (E << V²). Preferred in most problems.

**Why adjacency list is almost always preferred:** Real-world graphs are sparse. Matrix wastes O(V²) space and iterating neighbors costs O(V) even if a node has 2 neighbors.

---

## Breadth First Traversal (BFS)

Visit all nodes level by level. Uses a **queue**.

**Why queue and not stack?** Queue is FIFO — nodes added at one level are processed before nodes of the next level are enqueued. This guarantees level-by-level exploration. A stack would give DFS behavior (depth-first).

**Algorithm:**

1. Enqueue source, mark visited.
2. While queue not empty: dequeue node u, process u, enqueue all unvisited neighbors, mark them visited.

**Why mark visited when enqueuing, not when dequeuing?** If you mark visited only on dequeue, the same node can be enqueued multiple times before it's processed → incorrect results and wasted work.

**Applications:** Shortest path in unweighted graph, level order traversal, bipartite check, connected components.

**Edge cases:**

- Disconnected graph → run BFS from every unvisited node to cover all components.
- Self-loop → visited check prevents infinite loop.
- Graph with no edges → each node is its own component.

``` cpp
// Q: BFS of a graph (adjacency list, handle disconnected)
#include <bits/stdc++.h>
using namespace std;

vector<list<int>> graph;
unordered_set<int> visited;
queue<int> helper;
vector<int> result;
void connect(int src,int dest){
  graph[src].push_back(dest);
  graph[dest].push_back(src);
}
void bfs(int ele){
  helper.push(ele);
  visited.insert(ele);
  while(!helper.empty()){
    int ele = helper.front();
    helper.pop();
    result.push_back(ele);
    for(auto neigh:graph[ele]){
      if(! visited.count(neigh)){
        helper.push(neigh);
        visited.insert(neigh);
      }
    }
  }
}
int main(){
  int v,e;
  cin>>v>>e;
  
  graph.resize(v,list<int>());
  
  for(int i=0;i<e;i++){
    int src,dest;
    cin>>src>>dest;
    connect(src,dest);
  }
  
  bfs(0);
  for(int i=0;i<v;i++){
    cout<<result[i]<<" ";
  }
}

```

---

## Depth First Traversal (DFS)

Explore as deep as possible before backtracking. Uses recursion (implicit stack) or explicit stack.

**Why recursion naturally implements DFS?** Each recursive call goes deeper into one neighbor before returning. The call stack is literally a stack — LIFO order means we always explore the most recently added path first.

**Algorithm (recursive):**

1. Mark current node visited, process it.
2. For each unvisited neighbor, recurse.

**Applications:** Cycle detection, topological sort, SCC, path finding, solving mazes.

**Edge cases:**

- Disconnected graph → same as BFS, call DFS from each unvisited node.
- Deep recursion on large graphs → stack overflow risk. Use iterative DFS with explicit stack for large inputs.

``` cpp
// Q: DFS of a graph (recursive, handle disconnected)
void dfs(int ele){
  if(visited.count(ele))
    return ;
  visited.insert(ele);
  result.push_back(ele);
  for(auto neigh:graph[ele]){
    if(not visited.count(neigh)){
      dfs(neigh);
    }
  }
}
// Q: DFS iterative using explicit stack
void dfs(int ele){
  visited.insert(ele);
  stack<int> st;
  st.push(ele);
  while(st.size()>0){
    int temp = st.top();
    st.pop();
    result.push_back(temp);
    for(auto neigh:graph[temp]){
      if(not visited.count(neigh)){
        st.push(neigh);
        visited.insert(neigh);
      }
    }
  }
}

```

---

## Eulerian Path and Circuit

**Eulerian Circuit:** A closed walk that visits every **edge** exactly once and returns to the start.

**Eulerian Path:** A walk that visits every edge exactly once (start and end can differ).

**Conditions for Undirected Graph:**

- Eulerian Circuit exists if: graph is connected AND every vertex has **even degree**.
- Eulerian Path exists if: graph is connected AND exactly **2 vertices have odd degree** (those are the start and end).

**Why even degree for circuit?** Every time you enter a vertex, you must also leave. If a vertex has odd degree, at some point you'll enter and have no unused edge to leave → stuck.

**Why exactly 2 odd-degree vertices for path?** The start and end vertices are the only ones where entering and leaving counts don't need to match. Exactly 2 odd-degree nodes means exactly one start and one end.

**Edge cases:**

- Isolated vertices (degree 0) → ignore them for Eulerian check (they're not part of any edge).
- Graph with all even degrees but disconnected → no Eulerian circuit (connectivity required).

```
// Q: Check if Eulerian path/circuit exists in undirected graph


```

**Hierholzer's Algorithm** finds the actual Eulerian circuit in O(V+E):

1. Start at any vertex, follow edges (removing used ones) until stuck.
2. If stuck at start → done. Else find a vertex in current path with unused edges, splice in a new sub-circuit.

```
// Q: Find Eulerian circuit using Hierholzer's algorithm


```

---

## Hamiltonian Path

A path that visits every **vertex** exactly once. (Unlike Eulerian which is about edges.)

**No efficient algorithm exists.** Hamiltonian path is NP-complete. We use backtracking.

**Backtracking approach:**

1. Start from each vertex, try to extend the path.
2. At each step, add an unvisited adjacent vertex.
3. If all vertices included → found Hamiltonian path.
4. If stuck → backtrack.

**Why is Hamiltonian NP-complete but Eulerian is polynomial?** Eulerian path has simple degree-based conditions. Hamiltonian requires checking vertex visits which has no known polynomial-time characterization.

**Edge cases:**

- Complete graph → Hamiltonian path always exists.
- Path graph (1-2-3-...-n) → exactly one Hamiltonian path.

```
// Q: Find Hamiltonian path using backtracking


```

---

## Complexity Table

|Algorithm|Time|Space|Notes|
|---|---|---|---|
|BFS|O(V + E)|O(V)|Queue + visited array|
|DFS|O(V + E)|O(V)|Recursion stack / explicit stack|
|Check Eulerian|O(V + E)|O(V)|Degree check + connectivity check|
|Hierholzer's (Eulerian circuit)|O(V + E)|O(V + E)|Stack-based|
|Hamiltonian Path (backtracking)|O(V!) worst|O(V)|NP-complete, exponential|
|Adjacency list build|O(V + E)|O(V + E)||
|Adjacency matrix build|O(V²)|O(V²)||

---

## Quick Viva Q&A

**Q: Why does BFS give shortest path in unweighted graphs?** BFS explores nodes in order of distance from source. The first time a node is reached, it's via the shortest path (fewest edges).

**Q: Can DFS find shortest path?** Not reliably. DFS explores one path fully before backtracking — the first path found may not be the shortest.

**Q: What's the difference between Eulerian path and Hamiltonian path?** Eulerian: every edge exactly once. Hamiltonian: every vertex exactly once. Eulerian is solvable in polynomial time; Hamiltonian is NP-complete.

**Q: BFS on a weighted graph — does it give shortest path?** No. BFS treats all edges as equal weight. Use Dijkstra for weighted graphs.

**Q: Why do we need a visited array in graph traversal but not in tree traversal?** Trees have no cycles — you can never revisit a node. Graphs can have cycles, so without a visited array you'd loop infinitely.

**Q: Can a graph have an Eulerian circuit but no Hamiltonian circuit?** Yes. Example: a graph where all vertices have even degree (Eulerian circuit exists) but no single cycle visits every vertex exactly once.