# Relational Database Fundamentals

**Phase:** 2 (Data Core)  
**Prerequisites:** `02-Data-Fundamentals/06-Data-Pipeline-Components-Overview.md`  
**When to Skip:** Only if you can write complex queries with CTEs, window functions, and explain query plans  
**Projects This Enables:** Your WDI PostgreSQL database, all SQL-based transformations

## What to Cover

### 1. Database Concepts
- Tables, rows, columns, schemas
- Primary keys, foreign keys, constraints
- ACID properties (Atomicity, Consistency, Isolation, Durability)
- Transactions (`BEGIN`, `COMMIT`, `ROLLBACK`)
- Isolation levels (Read Uncommitted → Serializable)

### 2. Basic SQL
- `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- `WHERE`, `ORDER BY`, `LIMIT`, `OFFSET`
- `GROUP BY`, `HAVING`, aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
- `JOIN` types: INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF
- `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`

### 3. Intermediate SQL
- Subqueries (correlated vs non-correlated)
- `CASE` expressions
- `COALESCE`, `NULLIF`, `IS NULL` handling
- `EXISTS`, `IN`, `NOT IN` (beware of NULLs with `NOT IN`)
- String functions, date functions, type casting

### 4. Database Design
- Normalization (1NF, 2NF, 3NF, BCNF) — covered deeper in `04-Data-Modeling`
- Indexes (B-tree, hash, composite, partial)
- Views (simple, materialized)
- Stored procedures, functions, triggers (when to use, when to avoid)

### 5. Practical Skills
- Reading query execution plans (`EXPLAIN`, `EXPLAIN ANALYZE`)
- Connection strings and pooling
- `psql` CLI basics
- Backup and restore (`pg_dump`, `pg_restore`)

## Hands-On Exercise

1. Create a database for a simple e-commerce system (orders, customers, products)
2. Write queries using all JOIN types
3. Find slow queries with `EXPLAIN ANALYZE` and add indexes
4. Practice transactions: transfer money between two accounts safely

## Why This Matters

PostgreSQL is your Silver layer in the WDI project. Every data engineer must be fluent in SQL — it's the lingua franca of data.

## Next File
→ `02-PostgreSQL-Deep-Dive.md`
