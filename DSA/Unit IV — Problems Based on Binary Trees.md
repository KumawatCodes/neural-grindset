
---

## Populate Inorder Successor for All Nodes

Each node needs a pointer to the next node in inorder traversal.

**Approach:** Do a reverse inorder traversal (Right → Root → Left). Maintain a `next` pointer that starts as null. As you visit each node in reverse inorder, set `node->next = next`, then update `next = node`.

**Why reverse inorder?** Normal inorder visits A before B. We need B's address when processing A. By going right-to-left, we visit B first, save it in `next`, then when processing A we already have B's address.

**Edge case:** Rightmost node (last in inorder) → its successor is null. The algorithm handles this naturally since `next` starts as null.

```
// Q: Populate inorder successor using reverse inorder traversal


```

---

## Find N-th Node of Inorder Traversal

Perform inorder traversal and count nodes. When count reaches n, return that node.

**Approach:** Pass a counter by reference. In inorder traversal, increment counter after visiting left subtree. When counter == n, record the node.

**Edge case:**

- n > total nodes → return null or indicate not found.
- n <= 0 → invalid, handle explicitly.
- n = 1 → leftmost node (smallest in BST).

```
// Q: Find nth node in inorder traversal


```

---

## Level Order Traversal in Spiral Form

Alternate direction per level: left-to-right at level 0, right-to-left at level 1, etc.

**Approach 1 — Two stacks:**

- Stack 1 processes left-to-right: pushes right child then left child into stack 2.
- Stack 2 processes right-to-left: pushes left child then right child into stack 1.
- Alternate until both empty.

**Why two stacks instead of one queue?** A queue always gives left-to-right. Stacks (LIFO) allow us to reverse the print order by controlling the push order.

**Why not flip a queue?** You'd need to reverse the entire level's data — requires extra storage. Two stacks handle it naturally.

```
// Q: Spiral level order traversal using two stacks


```

---

## Boundary Traversal of Binary Tree

Print: left boundary (top to bottom) + all leaf nodes (left to right) + right boundary (bottom to top).

**Three separate passes:**

1. Left boundary: go down the leftmost path, print each node (exclude leaf).
2. Leaves: any traversal, print only leaf nodes.
3. Right boundary: go down rightmost path, print in reverse (use recursion or stack) (exclude leaf).

**Why exclude leaves from boundary passes?** Leaves are already printed in step 2. Including them would cause duplicates.

**Edge case:**

- Root only → it's both left boundary and right boundary and a leaf → print once.
- Tree with only left children → right boundary is empty (root already printed in left boundary).

```
// Q: Boundary traversal of binary tree


```

---

## Finding Lowest Common Ancestor (LCA)

LCA of nodes u and v is the deepest node that has both u and v as descendants (a node is a descendant of itself).

**Recursive approach:**

- If root is null → return null.
- If root == u or root == v → return root (found one of the nodes).
- Recurse left and right.
- If both return non-null → current root is the LCA.
- If only one returns non-null → return that side.

**Why does this work?** The first node where the two search paths diverge (one goes left, one goes right) is the LCA.

**For BST specifically:** If both nodes are less than root → LCA is in left subtree. If both greater → right subtree. Otherwise → root is LCA. This is O(h) without extra space.

**Edge cases:**

- One node is ancestor of other → that ancestor is the LCA.
- Nodes not in tree → algorithm returns null or incorrect result. You may need to verify both nodes exist first.

```cpp
// Q: Find LCA in a binary tree (generic)


// Q: Find LCA in BST (optimized)
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {

        if(!root)

            return NULL;

        if(root == p || root == q)

            return root;

        TreeNode* left = lowestCommonAncestor(root->left,p,q);

        TreeNode* right = lowestCommonAncestor(root->right,p,q);

  

        if(left && right)

            return root;

        if(left)

            return left;

        return right;

    }

```

---

## Sum of Nodes Having Only Left Child

Traverse tree, at each node check: does it have a left child but NO right child? If yes, add node's value.

**Why this specific condition?** "Only left child" means left != null AND right == null. If both exist, it's not "only left."

**Edge case:** Leaf nodes have neither child — they don't qualify. Root with only left child qualifies if it has no right child.

```
// Q: Sum of nodes that have only left child


```

---

## Diameter of a Tree

Diameter = longest path between any two nodes (path doesn't need to go through root).

**Key insight:** For any node, the diameter passing through it = left_height + right_height. The actual diameter is the max of this value across all nodes.

**Naive approach:** O(n²) — for each node, compute left and right heights separately.

**Optimized (O(n)):** Compute height and diameter simultaneously in a single DFS. Return height from each recursive call; update a global/reference `diameter` variable with `left_height + right_height` at each node.

**Why does the path not always go through root?** In a skewed tree or unbalanced tree, the two farthest nodes might both be in the left subtree.

**Edge case:** Empty tree → diameter = 0. Single node → diameter = 0 (no edges).

``` cpp
// Q: Find diameter of binary tree in O(n)
int dia=0;

    int height(TreeNode* root){

        if(root==NULL)

            return 0;

        int left = height(root->left);

        int right = height(root->right);

        dia = max(dia,left+right);

        return 1+max(left,right);

    }

    int diameterOfBinaryTree(TreeNode* root) {

        height(root);

        return dia;

    }

```

---

## Determine if Binary Tree is Height Balanced

Height balanced = for every node, |height(left) - height(right)| <= 1.

**Naive:** O(n²) — call height at every node.

**Optimized (O(n)):** Return -1 from recursive call if subtree is unbalanced; otherwise return actual height. If left or right returns -1, propagate -1 upward immediately.

**Why return -1 as a sentinel?** Height is always >= 0, so -1 is a safe signal for "unbalanced." This avoids a separate boolean flag.

**Edge case:** Empty tree → height = 0, trivially balanced. Single node → balanced.

```
// Q: Check if binary tree is height balanced (optimized O(n))


```

---

## Convert BST to Min Heap

Result must satisfy: complete binary tree + min heap property + all original BST values.

**Approach:**

1. Do inorder traversal of BST → get sorted array (ascending).
2. Do level order assignment: assign sorted values level by level, left to right. OR: do preorder assignment to the flattened tree (preorder visits in same order as level-order fill for a complete tree).

**Why inorder first?** Inorder of BST gives sorted order. Min heap requires parent < children — filling level by level from a sorted array guarantees this.

**Why does level-order fill from sorted array give a min heap?** The first element (smallest) goes to root. Next two go to level 1, next four to level 2 — each level's values are all larger than the level above → min heap property holds.

**Edge case:** BST with duplicate values → min heap still valid. Empty BST → empty heap.

```
// Q: Convert BST to min heap


```

---

## Complexity Table

|Problem|Time|Space|Notes|
|---|---|---|---|
|Inorder Successor|O(n)|O(h)|Reverse inorder|
|Nth Inorder Node|O(n)|O(h)|Early exit when count = n|
|Spiral Traversal|O(n)|O(n)|Two stacks|
|Boundary Traversal|O(n)|O(h)|Three separate passes|
|LCA (generic)|O(n)|O(h)|Single DFS|
|LCA (BST)|O(h)|O(1)|Compare values|
|Sum of left-child-only nodes|O(n)|O(h)|Simple DFS|
|Diameter (optimized)|O(n)|O(h)|Combined height+diameter DFS|
|Height Balanced (optimized)|O(n)|O(h)|Return -1 as sentinel|
|BST to Min Heap|O(n)|O(n)|Inorder + level-order fill|

h = height of tree. O(log n) for balanced, O(n) for skewed.

---

## Quick Viva Q&A

**Q: Why can the diameter not always pass through the root?** Because the two deepest nodes might both be in the same subtree. Example: left subtree is a tall chain, right subtree has only one node.

**Q: What's the difference between height and depth of a node?** Depth = distance from root to node. Height = distance from node to farthest leaf. Tree height = root's height.

**Q: In boundary traversal, what if the tree has no right subtree?** Right boundary is empty. Only left boundary and leaves are printed.

**Q: Why does LCA work without knowing the path explicitly?** The recursion implicitly explores all paths. When both left and right recursions return non-null, the current node is the split point — the LCA.

**Q: Can diameter be calculated using BFS?** Yes, but it's more complex. Two BFS calls from arbitrary nodes (farthest-node trick) works for unweighted trees. The DFS approach is simpler.

**Q: In BST-to-min-heap, can we do it without extra array?** It's harder. The standard approach uses O(n) extra space for the sorted values. In-place conversion is complex.