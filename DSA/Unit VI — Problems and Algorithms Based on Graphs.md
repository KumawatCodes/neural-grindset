

---

## Dijkstra's Shortest Path Algorithm

Finds shortest path from a single source to all vertices in a **weighted graph with non-negative weights**.

**Why min-heap (priority queue)?** We always want to process the currently known shortest path node next. A min-heap gives O(log V) extraction of the minimum. Without it, finding the minimum each time costs O(V) → total O(V²).

**Algorithm:**

1. dist[source] = 0, dist[all others] = INF. Push source into min-heap.
2. Extract min node u. For each neighbor v: if dist[u] + weight(u,v) < dist[v], update dist[v] and push v into heap.
3. Repeat until heap empty.

**Why doesn't Dijkstra work with negative weights?** Once a node is extracted from the heap, its distance is considered final. A negative edge could later provide a shorter path to an already-finalized node — Dijkstra won't revisit it.

**Edge cases:**

- Disconnected graph → unreachable nodes keep dist = INF.
- Graph with a single node → dist[source] = 0, no edges to process.
- Multiple edges between same pair → the relaxation handles it correctly, best edge wins.

```cpp
// Q: Dijkstra's algorithm using min-heap (adjacency list)

#include <bits/stdc++.h>
using namespace std;

vector<list<pair<int,int>>> graph;
void connect(int src,int dest,int wt){
  graph[src].push_back({wt,dest});
  graph[dest].push_back({wt,src});
}
vector<int> dijkstras(int src){
    vector<int> dist(graph.size(),INT_MAX);
    priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
    dist[src] = 0;
    pq.push({0,src});
    while(pq.size()>0){
      int currNode = pq.top().second;
      int currDistance = pq.top().first;
      pq.pop();
      if(dist[currNode]<currDistance)
        continue;
      
      for(auto neigh:graph[currNode]){
        int nextNode = neigh.second;
        int wt = neigh.first;
        if(wt+currDistance < dist[nextNode]){
          dist[nextNode] = wt+currDistance;
          pq.push({dist[nextNode],nextNode});
        }
      }
    }
    return dist;
}
int main(){
  int v,e;
  cin>>v>>e;
  
  graph.resize(v,list<pair<int,int>>());
  
  for(int i=0;i<e;i++){
    int src,dest,wt;
    cin>>src>>dest>>wt;
    connect(src,dest,wt);
  }
  
  vector<int> dist = dijkstras(0);
  for(int i=0;i<dist.size();i++){
    cout<<dist[i]<<" ";
  }
}
```

---

## Bellman-Ford Algorithm

Finds shortest paths from source, works with **negative weights**. Also detects **negative weight cycles**.

**Why relax V-1 times?** A shortest path in a graph with V vertices has at most V-1 edges (no cycles in a simple path). After i relaxations, we have correct shortest paths using at most i edges. After V-1 relaxations, all paths are correct.

**Negative cycle detection:** After V-1 relaxations, do one more pass. If any edge can still be relaxed → a negative cycle exists (distance would keep decreasing forever).

**Why Bellman-Ford over Dijkstra for negative weights?** Bellman-Ford relaxes all edges each round without assuming finality — it's allowed to re-relax nodes. Dijkstra's greedy finality assumption breaks with negative edges.

**Edge cases:**

- No negative weights → Dijkstra is faster, use that.
- Negative weight cycle reachable from source → no finite shortest path exists for nodes reachable through it.
- Disconnected graph → unreachable nodes remain INF.

```
// Q: Bellman-Ford algorithm with negative cycle detection


```

---

## Minimum Spanning Tree — Prim's Algorithm

Grows MST one vertex at a time. Always adds the cheapest edge connecting a visited vertex to an unvisited one.

**Why min-heap?** Same reason as Dijkstra — efficiently find the next minimum-weight edge.

**Greedy correctness:** Cut property — for any cut of the graph, the minimum weight edge crossing the cut is in some MST.

**Edge cases:**

- Disconnected graph → MST doesn't exist (only spanning forest possible).
- All edges same weight → any spanning tree is an MST.
- Graph with one node → MST has 0 edges.

```cpp
// Q: Prim's MST algorithm using min-heap

int prims(int src,int n){
  vector<bool>visited(n,false);
  int totalSum = 0;
  priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
  pq.push({0,src});
  // visited[src] = true;
  while(!pq.empty()){
    int curr = pq.top().second;
    int wt = pq.top().first;
    pq.pop();
    if(visited[curr])
      continue;
    
    visited[curr] = true;
    totalSum+=wt;
    
    for(auto neigh:graph[curr]){
      int nextNode= neigh.second;
      int nextwt= neigh.first;
      
      if(!visited[nextNode]){
        pq.push({nextwt,nextNode});
      }
    }
  }
  return totalSum;
}
```

---

## Minimum Spanning Tree — Kruskal's Algorithm

Sort all edges by weight. Add edge if it doesn't form a cycle (use DSU to check).

**Why DSU for cycle detection?** After sorting, we process edges greedily. DSU tells us in near O(1) whether two vertices are already connected. Adding an edge between already-connected vertices creates a cycle.

**Prim's vs Kruskal's:**

- Prim's: better for dense graphs (adjacency matrix + simple array → O(V²)).
- Kruskal's: better for sparse graphs (sort E edges → O(E log E)).
- Both always produce a correct MST but may produce different ones if multiple MSTs exist.

```cpp
// Q: Kruskal's MST algorithm using DSU
#include <bits/stdc++.h>
using namespace std;
class Edge{
public:
  int src;
  int dest;
  int wt;
};
bool cmp(Edge e1,Edge e2){
  return e1.wt < e2.wt;
}
int findParent(int child,vector<int>& parent){
  if(parent[child] == child){
    return child;
  }
  return parent[child]= findParent(parent[child],parent);
}

void Union(vector<int>& parent,vector<int>& rank,int child1,int child2){
  int parent1 = findParent(child1,parent);
  int parent2 = findParent(child2,parent);
  
  if(rank[parent1] > rank[parent2]){
    parent[parent2] = parent1;
  }
  else if(rank[parent1] < rank[parent2]){
      parent[parent1] = parent2;
  }
  else{
      parent[parent2] = parent1;
      rank[parent1]++;
  }
}
long long kruskalAlgorithm(vector<Edge>& edges,int v,int e){
  sort(edges.begin(),edges.end(),cmp);
  vector<int> parent(v);
  vector<int> rank(v,1);
  for(int i=0;i<v;i++){
    parent[i] = i;
  }
  int CountEdges=0;
  int i=0;
  long long ans=0;
  while(CountEdges<v-1 && i<e){
    Edge edge = edges[i];
    int parent1 = findParent(edge.src,parent);
    int parent2 = findParent(edge.dest,parent);
    
    if(parent1 != parent2){
      Union(parent,rank,edge.src,edge.dest);
      CountEdges++;
      ans+=edge.wt;
    }
    i++;
  }
  return ans;
}
int main(){
  int v,e;
  cin>>v>>e;
  vector<Edge> graph(e);
  for(int i=0;i<e;i++){
    Edge edge;
    cin>>graph[i].src>>graph[i].dest>>graph[i].wt;
  }
  cout<<kruskalAlgorithm(graph,v,e);
}

```

---

## Graph Colouring Problem

Assign colors to vertices such that no two adjacent vertices share the same color, using at most m colors.

**This is NP-complete in general.** We use backtracking.

**Backtracking approach:**

1. Try assigning color 1 to vertex 0.
2. For each subsequent vertex, try each color 1..m.
3. If color is safe (no adjacent vertex has same color) → assign it, recurse.
4. If no color works → backtrack.

**Chromatic number:** Minimum number of colors needed. Finding it is NP-hard.

**Special case:** Bipartite graphs are 2-colorable. Planar graphs need at most 4 colors (Four Color Theorem).

```
// Q: Graph colouring using backtracking


```

---

## Check if Graph is Bipartite

A graph is bipartite if vertices can be split into two groups such that every edge goes between groups (no edge within a group). Equivalent to: graph has no odd-length cycle.

**BFS/DFS 2-coloring approach:** Assign color 0 to source. For each neighbor, assign opposite color. If a neighbor already has the same color as current → not bipartite.

**Why 2-coloring works?** Bipartite = 2-colorable. If at any point two adjacent nodes have the same color, an odd cycle exists.

**Edge cases:**

- Disconnected graph → check each component separately.
- Single node → bipartite trivially.
- Graph with self-loop → never bipartite (self-loop = odd cycle of length 1).

```
// Q: Check if graph is bipartite using BFS coloring


```

---

## Detect Cycle in Graph

**Undirected Graph (DFS):** During DFS, if we reach a visited node that is not the parent of current node → cycle exists.

**Why check parent?** In undirected graphs, each edge appears in both directions. The edge back to parent is not a cycle — it's just the same undirected edge. Any other back edge is a real cycle.

**Directed Graph (DFS with colors):** Use 3 states: White (unvisited), Gray (in current DFS stack), Black (fully processed). If we reach a Gray node → back edge → cycle exists.

**Why 3 colors for directed?** In directed graphs, a node can be visited in a different DFS branch (not in current path) — that's not a cycle. Only a back edge (reaching a node currently in the recursion stack) indicates a cycle.

```
// Q: Detect cycle in undirected graph using DFS


// Q: Detect cycle in directed graph using DFS (3-color)


```

---

## Strongly Connected Components (SCC)

An SCC is a maximal subset of vertices such that every vertex is reachable from every other.

**Kosaraju's Algorithm:**

1. Run DFS on original graph, push nodes to stack in finish order.
2. Transpose the graph (reverse all edges).
3. Pop from stack, run DFS on transposed graph — each DFS tree is one SCC.

**Why reverse the graph?** In the original graph, a node finishing last in DFS is in a "source SCC." In the reversed graph, DFS from that node only reaches its own SCC (outgoing edges of source SCC in original become incoming in reversed).

**Tarjan's Algorithm:** Single DFS pass, uses discovery time and low-link values. More efficient in practice (one pass vs two).

```
// Q: Find SCCs using Kosaraju's algorithm


```

---

## Other Problems (Brief)

### Shortest Path from 1 to n

Standard Dijkstra from node 1, answer is dist[n].

### Minimum Product Spanning Tree

Replace edge weights with their logarithms (log w). Then find MST on log-weights using Kruskal/Prim. Product of weights is minimized because log(a*b) = log(a) + log(b) — minimizing sum of logs = minimizing product.

### Distance of Nearest Cell Having 1 (0-1 Matrix)

Multi-source BFS: enqueue all cells with value 1 simultaneously at distance 0. BFS outward fills minimum distances. Single-source BFS from each 0-cell would be O(n²m²); multi-source is O(nm).

### Count Number of Trees in a Forest

Run DFS/BFS from each unvisited node. Each traversal = one tree. Count = number of traversals needed.

### Snake and Ladder Problem

Model board as unweighted graph. Each cell is a node. BFS from cell 1, answer is minimum moves to reach cell n. Why BFS? Each dice roll = 1 move (unweighted). BFS gives minimum moves.

```
// Q: Snake and Ladder minimum moves using BFS


```

---

## Complexity Table

|Algorithm|Time|Space|Notes|
|---|---|---|---|
|Dijkstra (min-heap)|O((V+E) log V)|O(V)|No negative weights|
|Dijkstra (array)|O(V²)|O(V)|Better for dense graphs|
|Bellman-Ford|O(VE)|O(V)|Handles negative weights|
|Prim's (min-heap)|O((V+E) log V)|O(V)|Better for dense with matrix: O(V²)|
|Kruskal's|O(E log E)|O(V)|Better for sparse graphs|
|Graph Colouring|O(m^V) worst|O(V)|NP-complete, backtracking|
|Bipartite Check|O(V+E)|O(V)|BFS/DFS 2-coloring|
|Cycle Detection (undirected)|O(V+E)|O(V)|DFS + parent check|
|Cycle Detection (directed)|O(V+E)|O(V)|DFS + 3-color|
|Kosaraju's SCC|O(V+E)|O(V+E)|Two DFS passes|
|Tarjan's SCC|O(V+E)|O(V)|One DFS pass|
|Multi-source BFS (0-1 matrix)|O(V*W)|O(V*W)|V,W = grid dimensions|

---

## Quick Viva Q&A

**Q: Why does Dijkstra fail on negative weights?** It marks nodes as finalized when extracted from the heap. A negative edge found later could give a shorter path to a finalized node, but Dijkstra won't reprocess it.

**Q: When would you use Bellman-Ford over Dijkstra even without negative weights?** When you need to detect negative cycles. Also, Bellman-Ford is simpler to implement in distributed systems (each node only needs to know its neighbors).

**Q: What's the difference between MST and shortest path tree?** MST minimizes total edge weight of the spanning tree. Shortest path tree minimizes path weight from a source to each vertex. They can be different trees.

**Q: Why does Kruskal's need DSU but Prim's doesn't?** Kruskal's processes edges in arbitrary order — DSU checks if adding an edge creates a cycle. Prim's always grows from a connected component, so the next edge can never create a cycle.

**Q: Can Prim's and Kruskal's give different MSTs?** Yes, when multiple edges have equal weight — multiple valid MSTs may exist. Both algorithms are correct, just different.

**Q: Why is graph colouring NP-complete?** No known polynomial algorithm exists to determine the chromatic number. The decision version (can we color with k colors?) is NP-complete for k >= 3.

**Q: What's the key difference between cycle detection in directed vs undirected graphs?** Undirected: any back edge (not to parent) = cycle. Directed: only a back edge to a node currently in the DFS stack = cycle. A cross edge in directed graph is not a cycle.

**Q: Why does multi-source BFS work for nearest-1 cell problem?** BFS from all 1-cells simultaneously ensures each 0-cell is first reached via the closest 1-cell. Distance filled by BFS = minimum distance.