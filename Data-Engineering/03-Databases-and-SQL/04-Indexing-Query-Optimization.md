# Indexing & Query Optimization

**Phase:** 2 (Data Core)  
**Prerequisites:** `03-Advanced-SQL-Window-Functions-CTEs.md`  
**When to Skip:** Only if you can read execution plans, choose index types, and optimize slow queries systematically  
**Projects This Enables:** Fast queries on your WDI star schema, production database performance

## What to Cover

### 1. How Indexes Work
- B-tree indexes (default, good for equality and range queries)
- Hash indexes (equality only, rarely used)
- GiST, GIN, SP-GiST (PostgreSQL-specific for complex types)
- Partial indexes (index subset of table)
- Expression indexes (index on function result)
- Covering indexes (index-only scans)

### 2. Index Selection Strategy
- When to index: read-heavy tables, WHERE clauses, JOIN columns
- When NOT to index: small tables, write-heavy tables, low cardinality columns
- Composite index column order (most selective first)
- Index trade-offs: faster reads, slower writes, more storage

### 3. Query Optimization
- Reading `EXPLAIN` and `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` output
- Sequential scan vs index scan vs bitmap index scan
- Join strategies: nested loop, hash join, merge join
- Cost model: how PostgreSQL estimates query cost
- `ANALYZE` for statistics update

### 4. Common Performance Anti-Patterns
- `SELECT *` (fetching unnecessary columns)
- Functions on indexed columns (`WHERE UPPER(name) = 'JOHN'` prevents index usage)
- Implicit type conversion (string vs integer comparison)
- `OR` conditions (sometimes prevents index usage)
- N+1 queries (in application code)
- Missing foreign key indexes

### 5. Advanced Optimization
- Partition pruning (only scan relevant partitions)
- Parallel query execution
- Materialized views for expensive aggregations
- Query plan hints (use sparingly)
- Connection pooling impact

## Hands-On Exercise

1. Take a slow query from your WDI dataset and optimize it:
   - Add appropriate indexes
   - Rewrite to avoid anti-patterns
   - Compare `EXPLAIN ANALYZE` before and after
2. Benchmark write performance with and without indexes
3. Create a materialized view for a common aggregation

## Why This Matters for Your WDI Project

Your star schema has:
- `dim_country` (small, heavily read) → index on country_code
- `dim_indicator` (small, heavily read) → index on indicator_code
- `fact_wdi_data` (8.9M rows, read and write) → composite index on (country_id, indicator_id, year)

Without proper indexing, your "query in seconds" becomes "query in minutes."

## Next File
→ `05-NoSQL-Overview-MongoDB-Redis.md`
