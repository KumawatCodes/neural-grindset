
---

## What is a Heap?

A heap is a **complete binary tree** stored as an array where every parent satisfies the heap property with respect to its children. "Complete" means all levels are fully filled except possibly the last, which is filled left to right.

Two types:

- **Max Heap** — parent >= children. Root is the largest element.
- **Min Heap** — parent <= children. Root is the smallest element.

Why array representation? Because a complete binary tree maps perfectly to an array with zero wasted space and O(1) index arithmetic — no pointers needed.

---

## Array Representation

For a node at index `i` (0-based):

- Left child → `2i + 1`
- Right child → `2i + 2`
- Parent → `(i - 1) / 2`

Why does this work? A complete binary tree has a predictable structure. Level 0 has 1 node, level 1 has 2, level 2 has 4 — so index math directly encodes tree position.

**Edge case:** With 1-based indexing, formulas change to left = `2i`, right = `2i+1`, parent = `i/2`. Make sure you use consistent indexing throughout your code.

---

## Heap Operations

### Heapify (Fix one violation)

When a node violates the heap property, we fix it by swapping down (sift-down) or up (sift-up).

**Why sift-down for build-heap, sift-up for insert?**

- Insert adds at the end → violation can only go upward → sift-up.
- Build-heap processes internal nodes top-down → violations propagate down → sift-down.

**Sift-Down (Max Heapify)**

```cpp
// Q: Implement max heapify / sift-down for a subtree rooted at index i

#include <bits/stdc++.h>
using namespace std;

void heapify(vector<int>& arr, int n, int i){

    int largest = i;

    int left = 2*i + 1;
    int right = 2*i + 2;

    if(left < n && arr[left] > arr[largest])
        largest = left;

    if(right < n && arr[right] > arr[largest])
        largest = right;

    if(largest != i){

        swap(arr[i], arr[largest]);

        heapify(arr, n, largest);
    }
}

void heapSort(vector<int>& arr){

    int n = arr.size();

    // Build Max Heap
    for(int i = n/2 - 1; i >= 0; i--){
        heapify(arr, n, i);
    }

    // Heap Sort
    for(int i = n-1; i > 0; i--){

        swap(arr[0], arr[i]);

        heapify(arr, i, 0);
    }
}

int main(){

    vector<int> arr = {4, 10, 3, 5, 1};

    heapSort(arr);

    for(int x : arr){
        cout << x << " ";
    }

    return 0;
}
```

### Insert

Add at end of array, then sift-up until heap property restored.

```
// Q: Insert element into max heap


```

### Extract Max / Extract Min

Swap root with last element, reduce size by 1, sift-down from root.

Why swap instead of just removing root? Removing root creates a gap. Swapping with last element keeps the array contiguous, then sift-down restores the property.

```
// Q: Extract max from max heap


```

### Build Heap (Heapify all)

Start from last internal node `(n/2 - 1)` and sift-down each to index 0.

**Why start from n/2 - 1 and not from root?** Leaf nodes (indices n/2 to n-1) are trivially valid heaps of size 1. Starting from the last internal node and going backward ensures every subtree processed already has valid children.

**Why is build-heap O(n) and not O(n log n)?** Most nodes are near the bottom — they need very few sift-down steps. Mathematically, the sum works out to O(n). Calling insert n times would be O(n log n).

```
// Q: Build max heap from unsorted array


```

---

## Heap Sort

1. Build max heap from array — O(n)
2. Repeatedly extract max: swap root with last, reduce heap size, sift-down — O(n log n)
3. Result is sorted in ascending order in-place.

**Why does heap sort give ascending order with a max heap?** Each extraction puts the current maximum at the end of the array. After n extractions, the array is sorted ascending.

**Edge cases:**

- Array of size 1 → already sorted, no operations needed.
- All elements same → heap property always satisfied, sort runs but no actual swaps needed.
- Already sorted array → build-heap still runs in O(n), sort still O(n log n). No best-case benefit unlike quicksort.

```
// Q: Implement heap sort


```

---

## K'th Largest Element in Array

**Approach 1 — Min Heap of size K:** Maintain a min heap of the K largest elements seen so far. For each new element, if it's larger than the heap's root (current Kth largest), replace root and heapify.

**Why min heap, not max heap?** The root of a min heap of size K is the smallest among K largest — i.e., the Kth largest. A max heap of size K would need extra work to find the Kth largest.

**Approach 2 — Build max heap, extract K times:** O(n + K log n). Good when K is small.

**Edge cases:**

- K > n → invalid input, handle explicitly.
- K = 1 → just find the maximum.
- Duplicate elements → depends on whether question asks for Kth distinct or Kth in sorted order.

```
// Q: Find Kth largest element using min heap of size K


```

---

## Sort an Almost Sorted Array

"Almost sorted" (k-sorted) means every element is at most `k` positions away from its sorted position.

**Why use a min heap of size k+1?** If every element is within k positions of its correct place, then the minimum of any window of k+1 elements is guaranteed to be the next element in sorted order. A larger window wastes memory; a smaller one might miss the correct minimum.

**Steps:**

1. Insert first k+1 elements into min heap.
2. For each remaining element: extract min → place in output, insert new element.
3. Drain remaining heap.

**Time:** O(n log k). **Why better than O(n log n)?** Because k << n in practice, log k is much smaller.

```
// Q: Sort a k-sorted array using min heap


```

---

## Connect N Ropes with Minimum Cost

Cost to connect two ropes = sum of their lengths. Goal: minimize total cost.

**Why greedy with min heap works:** Always connect the two shortest ropes first. This is a greedy choice — connecting longer ropes later means they contribute to fewer addition operations. Proof by exchange argument: swapping any two operations to connect longer ropes earlier only increases cost.

**Steps:**

1. Insert all rope lengths into a min heap.
2. While more than one rope: extract two minimums, add them, push sum back, add sum to total cost.

**Edge case:** Only one rope → cost is 0, no connections needed.

**This is essentially Huffman encoding applied to rope lengths.**

```
// Q: Connect n ropes with minimum cost


```

---

## Complexity Table

|Operation|Time|Space|Notes|
|---|---|---|---|
|Build Heap|O(n)|O(1)|Not O(n log n) — mathematical proof|
|Insert|O(log n)|O(1)|Sift-up|
|Extract Max/Min|O(log n)|O(1)|Sift-down after swap|
|Peek (get max/min)|O(1)|O(1)|Just read root|
|Heap Sort|O(n log n)|O(1)|In-place, not stable|
|Kth Largest (min heap)|O(n log k)|O(k)|Better than sorting when k << n|
|Sort k-sorted array|O(n log k)|O(k)|Better than O(n log n) when k small|
|Connect n ropes|O(n log n)|O(n)|Greedy + min heap|
|Heapify (sift-down)|O(log n)|O(1)|Single node fix|

---

## Quick Viva Q&A

**Q: Is heap sort stable?** No. Swapping non-adjacent elements can change relative order of equal elements.

**Q: When would you prefer heap sort over merge sort?** When memory is a constraint — heap sort is O(1) space. Merge sort needs O(n) extra.

**Q: Can a heap be stored as a linked list?** Technically yes, but you lose O(1) parent/child access. Array is always preferred.

**Q: What's the difference between a heap and a BST?** Heap only enforces parent > children (no ordering between siblings). BST enforces left < root < right (full ordering). Heap is better for priority queue; BST is better for search.

**Q: Why is the last internal node at index n/2 - 1?** Leaf nodes start at index n/2 (0-based). So last non-leaf is n/2 - 1.

**Q: Can a min heap have the largest element at the root?** No by definition. But the largest element can be anywhere in the heap except positions guaranteed to be smaller — it's always a leaf node.

**Q: What happens if you call extract on an empty heap?** Undefined behavior / crash. Always check size > 0 before extracting.