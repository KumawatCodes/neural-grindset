# Data Partitioning and Sharding

**Phase:** 3 (Big Data)  
**Prerequisites:** `03-Distributed-Systems-CAP-Theorem.md`  
**When to Skip:** Only if you can design partitioning strategies for any dataset and explain sharding trade-offs  
**Projects This Enables:** Scaling your WDI project, understanding Spark/Hive partitioning

## What to Cover

### 1. Partitioning (Horizontal Splitting)
- **Definition:** Splitting a table into smaller, more manageable pieces based on a column value
- **Goal:** Improve query performance by pruning irrelevant partitions
- **Types:**
  - **Range partitioning:** By date range (2020-01, 2020-02), by ID range (1-1000000)
  - **List partitioning:** By discrete values (country_code IN ('USA', 'CAN', 'MEX'))
  - **Hash partitioning:** By hash of key (even distribution, but no pruning)
  - **Composite partitioning:** Range + hash (e.g., date range, then hash within range)

### 2. Partitioning in Practice

#### PostgreSQL
```sql
CREATE TABLE fact_wdi_data (
    ...
    year INTEGER,
    ...
) PARTITION BY RANGE (year);

CREATE TABLE fact_wdi_data_2020 PARTITION OF fact_wdi_data
    FOR VALUES FROM (2020) TO (2021);
```
- Query `WHERE year = 2020` only scans the 2020 partition
- **Benefit:** Faster queries, easier maintenance (drop old partitions)
- **Cost:** Slightly slower writes (routing to correct partition)

#### Spark / Hive
```python
df.write.partitionBy("year", "country_code").parquet("/path")
```
- Creates directory structure: `/path/year=2020/country_code=USA/...`
- **Predicate pushdown:** Spark reads only relevant directories

### 3. Sharding (Distributed Partitioning)
- **Definition:** Distributing partitions across multiple servers (nodes)
- **Goal:** Horizontal scaling (add nodes to handle more data)
- **Types:**
  - **Hash sharding:** `shard = hash(key) % num_shards` (even distribution)
  - **Range sharding:** Each shard gets a range (Shard 1: A-M, Shard 2: N-Z)
  - **Directory sharding:** Shard by geographic region (US shard, EU shard)

### 4. Sharding Challenges
- **Hot spots:** Uneven distribution (one shard gets all the traffic)
- **Cross-shard queries:** JOINs across shards are expensive (no local joins)
- **Rebalancing:** Adding/removing shards requires data migration
- **Global ordering:** No global sort order across shards (only within shard)
- **Transactions:** Cross-shard transactions are complex (2PC, Saga pattern)

### 5. Partitioning vs Sharding

| Aspect | Partitioning | Sharding |
|--------|-------------|----------|
| Scope | Single node | Multiple nodes |
| Goal | Query performance | Scalability |
| Complexity | Low | High |
| Cross-partition queries | Possible (same node) | Expensive (network) |
| Rebalancing | Easy (same node) | Hard (data migration) |
| Examples | PostgreSQL partitions | MongoDB shards, Cassandra |

### 6. Best Practices
- **Partition on query filter columns:** If you filter by date, partition by date
- **Avoid too many partitions:** 1000+ partitions is worse than no partitioning (metadata overhead)
- **Use composite partitioning:** Range for pruning + hash for even distribution
- **Monitor partition sizes:** Rebalance if partitions grow unevenly
- **For time-series:** Always partition by date (drop old data easily)

### 7. Your WDI Project Analysis
- **Current:** No partitioning (8.9M rows, single PostgreSQL node)
- **Recommended:** Partition `fact_wdi_data` by `year` (20 years = 20 partitions)
- **Benefit:** Queries for specific years scan 1/20th of the data
- **Future:** If you add real-time data, consider monthly partitions
- **Sharding:** Not needed unless you grow to 100M+ rows or need global distribution

## Hands-On Exercise

1. Partition your WDI `fact_wdi_data` table by `year` in PostgreSQL
2. Compare query performance: partitioned vs non-partitioned for `WHERE year = 2020`
3. Write a Spark job that writes WDI data partitioned by `year` and `country_code`
4. Calculate the number of partitions created — is it reasonable?

## Why This Matters

Partitioning is the #1 performance optimization for large tables. It's free (no extra infrastructure), easy to implement, and dramatically improves query speed. Every data engineer must master this before reaching for bigger tools.

## Next File
→ `05-Replication-and-Fault-Tolerance.md`
