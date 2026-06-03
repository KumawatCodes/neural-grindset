
---

## Types of Binary Tree

**Full Binary Tree:** Every node has 0 or 2 children. No node has exactly 1 child.

**Complete Binary Tree:** All levels fully filled except possibly the last, which is filled left to right. Heaps use this.

**Perfect Binary Tree:** All internal nodes have 2 children and all leaves are at the same level. A perfect tree with height h has 2^(h+1) - 1 nodes.

**Balanced Binary Tree (Height-Balanced):** Height difference between left and right subtree of any node is at most 1 (AVL definition). Ensures O(log n) operations.

**Degenerate / Skewed Tree:** Every parent has only one child. Looks like a linked list. All operations degrade to O(n). This is the worst case for BST if you insert sorted data.

**BST (Binary Search Tree):** Left subtree < root < right subtree. Enables O(log n) search on balanced trees.

---
## Construct Binary Tree
``` cpp
#include <bits/stdc++.h>
using namespace std;

class Node{
public:
  int val;
  Node* left;
  Node* right;
  Node(int val){
    this->val = val;
    left = NULL;
    right = NULL;
  }
};

Node* construct(vector<int> v){
  int n = v.size();
  queue<Node*> q;
  if(n == 0)
    return NULL;
  Node* root = new Node(v[0]);
  int i=1;
  int j=2;
  q.push(root);
  while(!q.empty() && i<n){
    Node* temp = q.front();
    q.pop();
    Node* l = NULL;
    Node* r = NULL;
    if(v[i]!=-1)
      l = new Node(v[i]);
    if(v[j]!=-1)
      r = new Node(v[j]);
    
    temp->left = l;
    temp->right = r;
    if(l!=NULL)
      q.push(l);
    if(r!=NULL)
      q.push(r);
    
    i+=2;
    j+=2;
  }
  return root;
}
int main() {
    vector<int> v = {1,2,3,4,5,-1,6,7,-1,8,9};
    Node* root = construct(v);
    postorder(root);
}
```

## Insertion in a Binary Tree

For a generic binary tree (not BST), insert at the first available position (level order). Use BFS — find the first node with a missing left or right child.

For BST: compare with root, go left if smaller, right if larger, insert when null is reached.

**Edge case:** Inserting into an empty tree → new node becomes root.

``` cpp
// Q: Insert node in a generic binary tree (level order)
Node* insert(Node* root,int val){
    Node* newNode = new Node(val);
    if(root == NULL)
      return newNode;
    
    queue<Node*> q;
    q.push(root);
    while(!q.empty()){
      Node* temp = q.front();
      q.pop();
      
      if(temp->left == NULL){
        temp->left = newNode;
        return root;
      }
      else{
        q.push(temp->left);
      }
      if(temp->right == NULL){
        temp->right = newNode;
        return root;
      }
      else{
        q.push(temp->right);
      }
    }
    return root;
}

// Q: Insert node in a BST

Node* insert(Node* root,int val){
    if(root == NULL)
      return new Node(val);
    if(val<root->val){
      root->left = insert(root->left,val);
    }
    else
      root->right = insert(root->right,val);
    return root;
}
```

---

## Deletion in a Binary Tree

**Generic Binary Tree deletion:**

1. Find the node to delete.
2. Find the deepest rightmost node.
3. Replace target node's value with deepest rightmost node's value.
4. Delete the deepest rightmost node.

**Why deepest rightmost?** Deleting from there maintains the complete binary tree structure.

**BST deletion** — three cases:

1. Node is a leaf → simply remove.
2. Node has one child → replace node with its child.
3. Node has two children → replace with inorder successor (smallest in right subtree) or inorder predecessor, then delete that successor/predecessor.

**Why inorder successor for BST deletion?** The inorder successor is the smallest value larger than the deleted node — it can replace the node while maintaining BST property.

**Edge case:** Deleting root with two children — apply case 3. Deleting a node that doesn't exist — handle gracefully.

``` cpp
// Q: Delete node from generic binary tree


// Q: Delete node from BST
  

TreeNode* iop(TreeNode* root){

  root = root->left;

  while(root->right){

    root = root->right;

  }

  return root;

}

TreeNode* deleteNode(TreeNode* root,int key){

    if(root == NULL)

        return NULL;

    if(root->val == key){

      // case 1 no child

      if(!root->left && !root->right){

        return NULL;

      }

      else if(root->left && root->right){

        TreeNode* pred = iop(root);

        root->val = pred->val;

        root->left = deleteNode(root->left,pred->val);

      }

      else{

        if(root->left) return root->left;

        else return root->right;

      }

    }

    else if(root->val > key){

      root->left = deleteNode(root->left,key);

    }

    else{

      root->right = deleteNode(root->right,key);

    }

    return root;

}

```

---

## Tree Traversals

All three traversals visit every node exactly once → O(n) time, O(h) space for recursion stack where h = height.

### Inorder (Left → Root → Right)

For BST, inorder gives elements in sorted ascending order. This is the most useful property of inorder traversal.

```cpp
// Q: Inorder traversal (recursive)

void inorder(Node* root){
  if(root == NULL)
    return;
  cout<<root->val<<" ";
  inorder(root->left);
  inorder(root->right);
}
```

### Preorder (Root → Left → Right)

Used to create a copy of the tree or serialize it. Root is always printed first.

```cpp
// Q: Preorder traversal (recursive)

void preorder(Node* root){
  if(root == NULL)
    return;
  cout<<root->val<<" ";
  preorder(root->left);
  preorder(root->right);
}
```

### Postorder (Left → Right → Root)

Used to delete a tree (process children before parent) or evaluate expression trees. Root is always printed last.

```cpp
// Q: Postorder traversal (recursive)

void postorder(Node* root){
  if(root == NULL)
    return;
  cout<<root->val<<" ";
  postorder(root->left);
  postorder(root->right);
}
```

---

## Inorder Traversal Without Recursion

Use an explicit stack to simulate the call stack.

**Why stack?** Recursion internally uses the call stack. We just make it explicit. Stack gives LIFO order — we push nodes going left, then pop and process, then go right.

**Algorithm:**

1. Current = root.
2. While current != null OR stack not empty:
    - Push current and go left until null.
    - Pop from stack, visit node, go right.

**Why this order?** We need to reach the leftmost node first (smallest in BST), which requires pushing all left nodes. Popping processes them in reverse order (left before root before right).

**Edge case:** Empty tree → stack never fills, loop exits immediately.

```cpp
// Q: Inorder traversal without recursion using stack
vector<int> inorderTraversal(TreeNode* root) {

        if(!root)

            return {};

        stack<TreeNode*> st;

        // st.push(root);

        vector<int> ans;

        TreeNode* node =root;

        while(st.size()>0 || node){

            if(node){

                st.push(node);

                node=node->left;

            }

            else{

                TreeNode* temp = st.top();

                st.pop();

                ans.push_back(temp->val);

                node = temp->right;

            }

        }

        return ans;

    }

```

---

## Print Postorder from Inorder and Preorder

Given inorder and preorder arrays, reconstruct and print postorder.

**Key insight:**

- First element of preorder is always the root.
- Find root in inorder → elements left of it are left subtree, right are right subtree.
- Recursively solve for each subtree.

**Why does this work uniquely?** Inorder + preorder (or inorder + postorder) uniquely identifies a binary tree. Preorder alone or postorder alone does not.

**Note:** Preorder + Postorder does NOT uniquely identify a tree (ambiguity when a node has only one child).

**Edge case:** Inorder and preorder must have the same elements. Duplicate values cause ambiguity.

```cpp
// Q: Print postorder given inorder and preorder
// By construcuting Tree
TreeNode* build(vector<int>& pre,vector<int>& ino,int prelo,int prehi,int inlo,int inhi){

        if(prelo>prehi)

            return NULL;

        TreeNode* root = new TreeNode(pre[prelo]);

        if(prelo == prehi)

            return root;

        int i=inlo;

        while(i<=inhi){    

            if(ino[i] == pre[prelo])

                break;

            i++;

        }

        int leftCount = i-inlo;

        int rightCount = inhi-i;

        root->left = build(pre,ino,prelo+1,prelo+leftCount,inlo,i-1);

        root->right = build(pre,ino,prelo+leftCount+1,prehi,i+1,inhi);

        return root;

    }

    TreeNode* buildTree(vector<int>& pre, vector<int>& ino) {

        int n = pre.size();

        return build(pre,ino,0,n-1,0,n-1);

    }


//Direct way
void getPostorder(vector<int>& pre, vector<int>& ino,  
int prelo, int prehi,  
int inlo, int inhi,  
vector<int>& post){  
  
if(prelo > prehi)  
return;  
  
int rootVal = pre[prelo];  
  
int i = inlo;  
while(i <= inhi){  
if(ino[i] == rootVal)  
break;  
i++;  
}  
  
int leftCount = i - inlo;  
  
getPostorder(pre, ino,  
prelo + 1,  
prelo + leftCount,  
inlo,  
i - 1,  
post);  
  
getPostorder(pre, ino,  
prelo + leftCount + 1,  
prehi,  
i + 1,  
inhi,  
post);  
  
post.push_back(rootVal);  
}

```

---

## Level Order Traversal (BFS)

Visit nodes level by level, left to right. Use a queue.

**Why queue?** Queue is FIFO. We enqueue left child then right child. The order they come out preserves level order. A stack would give a different (non-level) order.

**Why not recursion?** Recursion follows a single path (depth-first). Level-order needs to process all nodes at a level before going deeper (breadth-first).

``` cpp
// Q: Level order traversal using queue
vector<vector<int>> levelOrder(TreeNode* root) {

        vector<vector<int>> ans;

        queue<TreeNode*> q;

        if(!root)

            return ans;

        q.push(root);

        while(!q.empty()){

            int size = q.size();

            vector<int> v;

            for(int i=0;i<size;i++){

                TreeNode* temp = q.front();

                q.pop();

                if(temp->left!=NULL)

                    q.push(temp->left);

                if(temp->right!=NULL)

                    q.push(temp->right);

                v.push_back(temp->val);

            }

            ans.push_back(v);

        }

        return ans;

    }

```

---

## Edge Cases Across All Traversals

- Empty tree → output nothing, no crash.
- Single node → root is leaf, all traversals print just the root.
- Skewed tree (all left or all right) → recursion depth = n, risk of stack overflow for large n. Iterative versions handle this.
- Tree with only left children → inorder prints in order, preorder prints root first each time.

---

## Complexity Table

|Operation|Time|Space|Notes|
|---|---|---|---|
|Insert (generic)|O(n)|O(n)|BFS to find first empty spot|
|Insert (BST)|O(h)|O(h)|h = height; O(log n) balanced, O(n) skewed|
|Delete (generic)|O(n)|O(n)|Find node + find deepest rightmost|
|Delete (BST)|O(h)|O(h)|Find + fix|
|Any traversal (recursive)|O(n)|O(h)|h = height for call stack|
|Inorder without recursion|O(n)|O(h)|Explicit stack|
|Level order|O(n)|O(w)|w = max width of tree|
|Postorder from inorder+preorder|O(n²)|O(n)|O(n) with hashmap for inorder index|

---

## Quick Viva Q&A

**Q: What traversal gives sorted output for a BST?** Inorder (Left → Root → Right).

**Q: Can you reconstruct a tree from preorder alone?** No. You need inorder + preorder, or inorder + postorder.

**Q: Why is postorder used for tree deletion?** You must delete children before deleting the parent (otherwise you lose references). Postorder processes children first.

**Q: What's the space complexity of recursive traversal on a skewed tree?** O(n) — the call stack grows to depth n.

**Q: Why does level order use a queue and not a stack?** Queue is FIFO — nodes added at one level come out before nodes of the next level are added. A stack would process nodes in a DFS manner.

**Q: Difference between complete and full binary tree?** Full: every node has 0 or 2 children. Complete: filled left to right at each level. A complete tree can have nodes with 1 child (the last node at the last level).

**Q: What is the maximum number of nodes in a binary tree of height h?** 2^(h+1) - 1 (perfect binary tree). Minimum is h+1 (skewed).