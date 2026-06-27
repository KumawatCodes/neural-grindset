# PostgreSQL Deep Dive

**Phase:** 2 (Data Core)  
**Prerequisites:** `01-Relational-Database-Fundamentals.md`  
**When to Skip:** Only if you can tune PostgreSQL for analytics workloads, configure replication, and use advanced features  
**Projects This Enables:** Your WDI Silver layer, local development environment

## What to Cover

### 1. PostgreSQL Architecture
- Process vs thread model (PostgreSQL uses processes)
- Shared memory, WAL (Write-Ahead Logging)
- Tablespaces, schemas, databases
- Configuration files (`postgresql.conf`, `pg_hba.conf`)

### 2. Advanced Data Types
- Arrays (`INTEGER[]`, `TEXT[]`)
- JSON/JSONB (semi-structured data in a relational database)
- `ENUM`, `UUID`, `INET`, `CIDR`
- `TIMESTAMP` vs `TIMESTAMPTZ` (always use `TIMESTAMPTZ`)
- Custom types with `CREATE TYPE`

### 3. Advanced SQL Features
- Common Table Expressions (CTEs) — recursive CTEs for hierarchical data
- Window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LEAD`, `LAG`, `FIRST_VALUE`, `LAST_VALUE`)
- `LATERAL` joins
- `FILTER` clause for conditional aggregation
- `DISTINCT ON` (PostgreSQL-specific)

### 4. Performance Tuning
- `VACUUM`, `ANALYZE`, `REINDEX`
- Query planner statistics
- Partitioning (range, list, hash)
- Parallel query execution
- Connection pooling (PgBouncer)

### 5. Replication & High Availability
- Streaming replication (primary → standby)
- Logical replication (table-level, cross-version)
- Hot standby, read replicas
- Failover with Patroni

### 6. PostgreSQL for Data Engineering
- `COPY` for bulk loading (much faster than `INSERT`)
- Foreign Data Wrappers (FDW) — query other databases from PostgreSQL
- `pg_stat_statements` for query performance analysis
- TimescaleDB extension for time-series data

## Hands-On Exercise

1. Set up PostgreSQL with Docker (`docker run -d -p 5432:5432 postgres`)
2. Load 1M rows using `COPY` and compare speed with `INSERT`
3. Create a partitioned table and compare query performance
4. Set up a read replica (or at least understand the concept)
5. Use window functions to calculate running totals and YoY growth

## Why This Matters for Your WDI Project

Your WDI pipeline uses PostgreSQL as the Silver layer. You need to:
- Efficiently load 8.9M rows (use `COPY`, not row-by-row `INSERT`)
- Design indexes for the star schema (dimension table PKs, fact table FKs)
- Understand partitioning if the dataset grows
- Use `JSONB` if you need to store semi-structured metadata

## Next File
→ `03-Advanced-SQL-Window-Functions-CTEs.md`
