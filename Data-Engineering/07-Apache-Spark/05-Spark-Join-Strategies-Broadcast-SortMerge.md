# Spark Join Strategies: Broadcast, Sort-Merge, Shuffle-Hash

**Phase:** 3 (Big Data)  
**Prerequisites:** `04-Spark-SQL-and-Catalyst-Optimizer.md`  
**When to Skip:** Only if you can choose the right join strategy for any dataset size and explain the trade-offs  
**Projects This Enables:** Optimizing join performance, avoiding shuffle bottlenecks

## What to Cover

### 1. Why Joins Matter
- Joins are the most expensive operation in distributed processing
- They require data movement (shuffle) across the network
- Wrong join strategy = 10-100× slower performance
- Understanding join strategies is essential for Spark optimization

### 2. Broadcast Hash Join (Small + Large)
- **When:** One table is small (default < 10MB, configurable)
- **How:** Copy small table to all executors, hash join locally with large table partitions
- **Network cost:** O(size of small table) — broadcast to all nodes
- **Memory cost:** Small table replicated on each executor
- **Pros:** No shuffle of large table, very fast
- **Cons:** Small table must fit in memory on each executor
- **Trigger:** Automatic when `spark.sql.autoBroadcastJoinThreshold` is met, or explicit `broadcast()`

```python
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "join_col")
```

### 3. Sort-Merge Join (Large + Large)
- **When:** Both tables are large, or neither fits broadcast threshold
- **How:**
  1. Shuffle both tables by join key (expensive network transfer)
  2. Sort each partition by join key
  3. Merge sorted partitions (like merge sort)
- **Network cost:** O(size of both tables) — full shuffle
- **Memory cost:** Low (streams sorted data, minimal memory)
- **Pros:** Handles any size, stable performance
- **Cons:** Expensive shuffle, requires sorting
- **Spark default:** For large-large joins

### 4. Shuffle Hash Join (Medium + Medium)
- **When:** Both tables are medium-sized, one is slightly smaller
- **How:**
  1. Shuffle smaller table by join key (build side)
  2. Build hash table in memory on each executor
  3. Stream larger table (probe side) and lookup in hash table
- **Network cost:** O(size of smaller table) — partial shuffle
- **Memory cost:** Hash table of smaller table partition
- **Pros:** Faster than sort-merge if build side fits in memory
- **Cons:** Build side must fit in memory, risk of OOM
- **Spark behavior:** Attempts shuffle hash, falls back to sort-merge if OOM

### 5. Cartesian Join (Cross Join)
- **When:** No join condition, or explicit cross join
- **How:** Every row of table A joined with every row of table B
- **Cost:** O(rows_A × rows_B) — explosive growth
- **Use case:** Very rare, usually a mistake
- **Warning:** Spark disables by default, must enable explicitly

### 6. Join Strategy Selection

```
Is one table small (< 10MB or < broadcast threshold)?
├── YES → Broadcast Hash Join (fastest, no shuffle)
│         └── Does small table fit in executor memory?
│             ├── YES → Use broadcast()
│             └── NO  → Increase executor memory or use Sort-Merge
└── NO  → Are both tables sorted on join key?
    ├── YES → Sort-Merge Join (efficient, no extra sort)
    └── NO  → Is one table significantly smaller?
        ├── YES → Shuffle Hash Join (try first, fallback to Sort-Merge)
        └── NO  → Sort-Merge Join (default, safest)
```

### 7. Tuning Joins
- **Increase broadcast threshold:** `spark.sql.autoBroadcastJoinThreshold=100MB` (if executors have memory)
- **Force broadcast:** `broadcast(small_df)` hint
- **Salting for skew:** Add random prefix to skewed keys to distribute load
- **Avoid cross joins:** Always specify join condition
- **Filter before join:** Reduce data size before shuffling
- **Partition both tables on join key:** If already partitioned, skip shuffle

### 8. Your WDI Project Joins
- **Dimension → Fact joins:** `dim_country` (small) joined with `fact_wdi_data` (large)
  - **Strategy:** Broadcast `dim_country` (small dimension table)
- **Fact → Fact joins:** GDP fact joined with Life Expectancy fact (both large)
  - **Strategy:** Sort-Merge Join (both are large)
  - **Optimization:** Ensure both are partitioned on `country_id` + `year`

## Hands-On Exercise

1. Join your WDI `fact_wdi_data` with `dim_country` using different strategies:
   - Default (let Catalyst choose)
   - Force broadcast: `fact.join(broadcast(dim_country), ...)`
   - Force sort-merge: `spark.conf.set("spark.sql.join.preferSortMergeJoin", "true")`
2. Compare execution time and query plans
3. Create a skewed dataset (one country has 50% of rows) and observe performance
4. Apply salting to fix skew and measure improvement

## Why This Matters

Joins are where pipelines die. A broadcast join on a 10MB table takes seconds. A sort-merge join on two 100GB tables takes hours. Choosing the right strategy is the difference between a working pipeline and a failed job.

## Next File
→ `06-Spark-Partitioning-and-Data-Skew.md`
