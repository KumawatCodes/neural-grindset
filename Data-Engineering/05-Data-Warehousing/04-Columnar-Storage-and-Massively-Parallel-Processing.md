# Columnar Storage & Massively Parallel Processing

**Phase:** 2 (Data Core)  
**Prerequisites:** `03-Modern-Cloud-Warehouses-Snowflake-BigQuery-Redshift.md`  
**When to Skip:** Only if you can explain why columnar is faster for analytics and how MPP distributes queries  
**Projects This Enables:** Understanding warehouse performance, optimizing your WDI queries

## What to Cover

### 1. Row-Oriented Storage (Traditional)
- **How it works:** Store entire rows together on disk
- **Layout:** Row 1 (all columns) → Row 2 (all columns) → Row 3 (all columns)
- **Good for:** OLTP (read/write entire rows, e.g., `SELECT * FROM orders WHERE order_id = 123`)
- **Bad for:** OLAP (scanning millions of rows but only a few columns)
- **Example:** PostgreSQL, MySQL, SQL Server (rowstore)

### 2. Columnar Storage (Analytics)
- **How it works:** Store each column together on disk
- **Layout:** Column A (all rows) → Column B (all rows) → Column C (all rows)
- **Good for:** OLAP (scanning specific columns, e.g., `SELECT SUM(sales) FROM fact_sales`)
- **Bad for:** OLTP (updating a row requires touching multiple column files)
- **Example:** Snowflake, BigQuery, Redshift, Parquet, ORC

### 3. Why Columnar is Faster for Analytics
- **Compression:** Same data type in a column compresses better (run-length encoding, dictionary encoding)
- **Vectorized processing:** CPU processes column data in batches (SIMD instructions)
- **Projection pushdown:** Only read columns you need (ignore others)
- **Predicate pushdown:** Filter at storage level (Parquet min/max statistics)
- **Cache efficiency:** Sequential reads of column data fit in CPU cache

### 4. Massively Parallel Processing (MPP)
- **Concept:** Distribute data and query processing across many nodes
- **Architecture:**
  - **Leader/Coordinator node:** Receives query, optimizes, distributes
  - **Compute/Worker nodes:** Execute query fragments in parallel
  - **Shared-nothing:** Each node has its own CPU, memory, disk
- **Data distribution:**
  - **Hash distribution:** Distribute by hash of key (even distribution)
  - **Round-robin:** Distribute sequentially (simple, no skew)
  - **Replication:** Copy small tables to all nodes (avoid shuffling)
- **Query execution:**
  - Query parsed → Optimized → Distributed → Executed in parallel → Results merged

### 5. MPP in Practice
- **Snowflake:** Virtual warehouses (clusters) auto-scale, query optimizer handles distribution
- **BigQuery:** Dremel engine, serverless MPP (no nodes to manage)
- **Redshift:** Configure distribution keys and sort keys for performance
- **Spark:** DataFrame operations distributed across executors

### 6. Key Performance Concepts
- **Data skew:** Uneven distribution (one node gets all the work)
- **Shuffle:** Moving data between nodes for joins/aggregations (expensive)
- **Broadcast join:** Copy small table to all nodes (avoid shuffle)
- **Sort-merge join:** Pre-sorted data, merge in parallel
- **Partition pruning:** Skip partitions that don't match query filters

### 7. Your WDI Project
- **PostgreSQL:** Row-oriented, single-node (no MPP)
- **For your 8.9M rows:** Single-node PostgreSQL is fine
- **If you scale to 100M+ rows:** Consider columnar (cstore_fdw extension for PostgreSQL, or migrate to Snowflake)
- **Parquet files:** Columnar storage for your data lake (if you add S3)

## Hands-On Exercise

1. Compare query performance on PostgreSQL:
   - `SELECT * FROM fact_wdi_data` (row-oriented, slow)
   - `SELECT country_id, AVG(value) FROM fact_wdi_data GROUP BY country_id` (still row-oriented, but fewer columns)
2. If you have access to BigQuery or Snowflake, run the same query and compare
3. Export your WDI data to Parquet and compare file size vs CSV

## Why This Matters

When your dataset grows from 8.9M to 890M rows, row-oriented PostgreSQL will choke. Columnar + MPP is why cloud warehouses handle PB-scale data. Understanding this now prevents painful migrations later.

## Next File
→ `05-Warehouse-Performance-Tuning.md`
