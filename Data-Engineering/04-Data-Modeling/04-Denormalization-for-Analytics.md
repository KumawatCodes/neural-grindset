# Denormalization for Analytics

**Phase:** 2 (Data Core)  
**Prerequisites:** `03-Normalization-1NF-2NF-3NF-BCNF.md`  
**When to Skip:** Only if you understand why star schemas are denormalized and can design one  
**Projects This Enables:** Your WDI star schema, all data warehouse design

## What to Cover

### 1. Why Denormalize?
- **Query performance:** Fewer joins = faster reads
- **Simpler queries:** Analysts write simpler SQL
- **Aggregation speed:** Pre-joined data aggregates faster
- **Trade-off:** More storage, harder updates, data redundancy

### 2. Denormalization Techniques
- **Pre-joining:** Store related data together (customer name in orders table)
- **Adding derived columns:** Store calculated values (total_price = quantity * unit_price)
- **Creating summary tables:** Pre-aggregate common queries (daily sales totals)
- **Vertical partitioning:** Split wide tables by access pattern (hot columns vs cold columns)
- **Horizontal partitioning:** Split by row (date ranges, regions)

### 3. When to Denormalize
- **Read-heavy workloads:** Analytics, reporting, BI tools
- **Known query patterns:** You know what queries will run
- **Data doesn't change much:** Historical data, append-only
- **Storage is cheaper than compute:** Cloud warehouses (Snowflake, BigQuery)

### 4. When NOT to Denormalize
- **Write-heavy workloads:** OLTP, transactional systems
- **Data changes frequently:** Updates cause inconsistency across copies
- **Storage is expensive:** Edge devices, embedded systems
- **Unknown query patterns:** You can't predict what to pre-join

### 5. The Analytics Database Spectrum
```
Highly Normalized (3NF) ←————————→ Highly Denormalized (Star Schema)
OLTP databases              Data warehouses
Complex writes              Fast reads
Data integrity              Query performance
Many joins                  Few joins
Small storage               Large storage
```

### 6. Materialized Views
- **Definition:** Pre-computed query results stored as a table
- **Pros:** Fast reads, automatic refresh
- **Cons:** Stale data, refresh overhead
- **Use case:** Expensive aggregations that run frequently
- **Tools:** PostgreSQL materialized views, Snowflake dynamic tables

## Hands-On Exercise

Take your normalized 3NF library schema from the normalization exercise and denormalize it for analytics:
1. What would a "loan summary" table look like?
2. What derived columns would you add?
3. What pre-aggregations make sense?
4. Compare query complexity: normalized vs denormalized

## Why This Matters for Your WDI Project

Your WDI dataset is 8.9M rows of observations. If you normalize it fully, every query joins 6+ tables. If you denormalize into a star schema, queries are simple and fast. This is the core trade-off of data warehousing.

## Next File
→ `05-Star-Schema-Design.md`
