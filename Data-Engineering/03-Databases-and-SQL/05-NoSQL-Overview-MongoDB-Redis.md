# NoSQL Overview: MongoDB & Redis

**Phase:** 2 (Data Core) — **Lightweight coverage**  
**Prerequisites:** `04-Indexing-Query-Optimization.md`  
**When to Skip:** Only if you understand document stores, key-value stores, and when to use each  
**Projects This Enables:** Understanding when SQL isn't the answer, caching strategies

## What to Cover

### 1. Why NoSQL Exists
- Schema flexibility (agile development, varying data shapes)
- Horizontal scaling (sharding across many servers)
- Specific data models (documents, graphs, key-value, wide-column)
- CAP theorem trade-offs (Consistency vs Availability vs Partition tolerance)

### 2. Document Stores: MongoDB
- Documents (BSON, like JSON), collections, _id
- CRUD operations, queries, aggregation pipeline
- Indexing in MongoDB (similar concepts, different syntax)
- When to use: semi-structured data, rapid prototyping, content management
- When NOT to use: complex transactions, heavy joins, strict ACID needs

### 3. Key-Value Stores: Redis
- Strings, hashes, lists, sets, sorted sets
- TTL (Time To Live) for cache expiration
- Pub/Sub for messaging
- When to use: caching, session storage, real-time leaderboards, rate limiting
- When NOT to use: primary data store, complex queries, large datasets

### 4. Wide-Column Stores: Cassandra (Preview)
- Distributed, eventually consistent
- Column families, compound keys, clustering columns
- When to use: write-heavy workloads, time-series data, IoT
- When NOT to use: ad-hoc querying, complex joins

### 5. Graph Databases: Neo4j (Preview)
- Nodes, relationships, properties
- Cypher query language
- When to use: social networks, recommendation engines, fraud detection

### 6. When to Choose What

| Use Case | Best Choice | Why |
|----------|-------------|-----|
| Transactional app data | PostgreSQL | ACID, complex queries |
| Analytics warehouse | Snowflake/BigQuery | Columnar, MPP |
| Semi-structured logs | MongoDB | Flexible schema |
| Cache/session store | Redis | Sub-millisecond latency |
| Time-series IoT | Cassandra | Write-optimized, distributed |
| Social graph | Neo4j | Relationship queries |

## Hands-On Exercise

1. Install MongoDB and Redis with Docker
2. Store a JSON API response in MongoDB, query it
3. Use Redis as a cache for a slow database query
4. Compare query patterns: same data in PostgreSQL vs MongoDB

## Why This Matters for Data Engineering

You won't always get clean relational data. APIs return JSON, logs are semi-structured, caching is essential. Know the tools, but don't over-engineer — PostgreSQL handles 80% of use cases.

## Next File
→ `06-When-SQL-vs-NoSQL.md`
