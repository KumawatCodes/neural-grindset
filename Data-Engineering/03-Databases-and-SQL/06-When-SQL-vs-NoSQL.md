# When SQL vs NoSQL

**Phase:** 2 (Data Core) — **Decision Framework**  
**Prerequisites:** `05-NoSQL-Overview-MongoDB-Redis.md`  
**When to Skip:** Never — this is the decision framework you'll use for every project  
**Projects This Enables:** Technology selection for all future projects

## What to Cover

### 1. The Decision Framework

Ask these questions in order:

```
1. Do you need ACID transactions?
   ├── YES → SQL (PostgreSQL, MySQL)
   └── NO → Continue...

2. Is your data highly structured and relational?
   ├── YES → SQL
   └── NO → Continue...

3. Do you need horizontal scaling beyond single server?
   ├── YES → NoSQL (MongoDB, Cassandra) or Cloud SQL
   └── NO → Continue...

4. Is your schema evolving rapidly?
   ├── YES → Document store (MongoDB)
   └── NO → Continue...

5. Is this primarily for caching or real-time lookups?
   ├── YES → Key-value (Redis)
   └── NO → Continue...

6. Do you need complex analytics (OLAP)?
   ├── YES → Data warehouse (Snowflake, BigQuery)
   └── NO → Probably SQL is fine
```

### 2. The Modern Reality: Polyglot Persistence
- Most systems use multiple databases
- PostgreSQL for transactional data + Redis for cache + Snowflake for analytics
- Data engineers bridge these systems (ETL/ELT pipelines)

### 3. Common Mistakes
- Using MongoDB because "it's modern" when PostgreSQL would work
- Using PostgreSQL for massive write-heavy workloads (consider Cassandra)
- Not using Redis for caching (hitting the database for every request)
- Choosing a database before understanding the data model

### 4. Your WDI Project Analysis
- **Silver layer (PostgreSQL):** Structured, relational, ACID needed → SQL ✅
- **Gold layer (Supabase):** PostgreSQL-based, analytics queries → SQL ✅
- **Cache layer:** None currently, but Redis could cache dashboard queries
- **Raw data (S3):** Object storage, not a database, but "schema-on-read" for data lake

## Hands-On Exercise

For 3 hypothetical projects, choose the database stack and justify:
1. A real-time ride-sharing app (Uber-like)
2. A financial reporting system for a bank
3. A social media analytics platform

## Why This Matters

Wrong database choice = expensive migration later. Right choice = scalable, maintainable system. This decision framework prevents "shiny object syndrome."

## Next File
→ `04-Data-Modeling/01-Data-Modeling-Introduction.md`
