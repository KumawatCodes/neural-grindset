# Warehouse Performance Tuning

**Phase:** 2 (Data Core) — **Preview, Deep Dive in Phase 5**  
**Prerequisites:** `04-Columnar-Storage-and-Massively-Parallel-Processing.md`  
**When to Skip:** Skip now. Return when you have performance problems.  
**Projects This Enables:** Optimizing slow queries, reducing cloud costs

## What to Cover (Preview)

### 1. Query Optimization
- **EXPLAIN ANALYZE:** Read execution plans
- **Index selection:** B-tree, hash, bitmap, partial, expression
- **Join optimization:** Join order, join type (nested loop, hash, merge)
- **Predicate pushdown:** Filter early, filter at storage
- **Partition pruning:** Only scan relevant partitions

### 2. Schema Design for Performance
- **Denormalization:** Pre-join for read performance
- **Materialized views:** Pre-compute expensive aggregations
- **Aggregate tables:** Pre-aggregate common queries
- **Surrogate keys:** Integer keys join faster than string keys
- **Data types:** Smaller is faster (INT vs BIGINT, VARCHAR vs TEXT)

### 3. Cloud-Specific Tuning
- **Snowflake:** Warehouse size (XS → 6XL), clustering keys, result caching
- **BigQuery:** Partitioning, clustering, query optimization (avoid SELECT *), slot reservations
- **Redshift:** Distribution keys, sort keys, vacuum, analyze, compression encoding

### 4. Caching Strategies
- **Result caching:** Cache query results (Snowflake, BigQuery)
- **BI engine:** In-memory caching for dashboards (BigQuery)
- **Materialized views:** Pre-computed results
- **Application caching:** Redis for frequently accessed data

### 5. Cost Optimization
- **BigQuery:** Use partitions, avoid full table scans, use sandbox for testing
- **Snowflake:** Auto-suspend warehouses, use XS for development, monitor credit usage
- **Redshift:** Reserved instances for predictable workloads, pause clusters when idle

## Hands-On Exercise (When You Return)

1. Identify your slowest WDI query
2. Run `EXPLAIN ANALYZE` and identify the bottleneck
3. Add an index, a materialized view, or rewrite the query
4. Measure improvement

## Why Defer Deep Dive?

Premature optimization is the root of all evil. Your WDI dataset is small enough that PostgreSQL defaults are fine. Learn the concepts now, apply them when you have real performance problems or cost concerns.

## Return Here After
→ `16-Performance-Optimization/01-Query-Optimization-Techniques.md`

## Next File (Continue Phase 2)
→ `06-Big-Data-Fundamentals/01-Introduction-to-Big-Data-5-Vs.md`
