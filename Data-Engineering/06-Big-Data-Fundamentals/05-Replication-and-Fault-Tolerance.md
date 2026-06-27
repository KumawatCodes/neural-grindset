# Replication and Fault Tolerance

**Phase:** 3 (Big Data)  
**Prerequisites:** `04-Data-Partitioning-and-Sharding.md`  
**When to Skip:** Only if you can design replication strategies and explain exactly-once vs at-least-once semantics  
**Projects This Enables:** Building reliable pipelines, understanding Kafka/Spark fault tolerance

## What to Cover

### 1. Why Replication?
- **Fault tolerance:** If one node fails, another has the data
- **High availability:** Serve reads from replicas if primary is down
- **Load distribution:** Spread read traffic across replicas
- **Disaster recovery:** Geographic replication for regional failures
- **Backup:** Replicas as hot backups (faster recovery than cold backups)

### 2. Replication Strategies

#### Master-Slave (Primary-Secondary)
- **Architecture:** One master (writes), one or more slaves (reads)
- **Replication:** Async or sync from master to slaves
- **Pros:** Simple, read scaling, failover possible
- **Cons:** Write bottleneck (only master), replication lag (async), split-brain risk
- **Examples:** PostgreSQL streaming replication, MySQL replication, MongoDB replica sets

#### Master-Master (Multi-Primary)
- **Architecture:** Multiple nodes accept writes
- **Pros:** Write scaling, geographic distribution
- **Cons:** Conflict resolution (same key written to two masters), complex consistency
- **Examples:** MySQL Group Replication, Cassandra (tunable), CockroachDB

#### Leaderless (Dynamo-style)
- **Architecture:** Any node accepts writes, read from multiple nodes, quorum
- **Pros:** High availability, no single point of failure
- **Cons:** Eventual consistency, complex conflict resolution
- **Examples:** Cassandra, DynamoDB, Riak, Voldemort

### 3. Replication Modes
- **Synchronous:** Master waits for slave acknowledgment → Strong consistency, higher latency
- **Asynchronous:** Master doesn't wait → Better performance, replication lag, risk of data loss
- **Semi-synchronous:** Master waits for at least one slave → Balance of consistency and performance

### 4. Fault Tolerance in Data Pipelines
- **Idempotency:** Running the same operation twice produces the same result
  - Example: `INSERT OR REPLACE` vs `INSERT` (duplicate error)
  - Example: `MERGE` (upsert) vs `INSERT` (append)
- **Checkpointing:** Save progress so you can resume from failure point (Spark, Flink)
- **Dead letter queues:** Save failed records for later analysis (Kafka, SQS)
- **Circuit breakers:** Stop processing if error rate exceeds threshold (prevent cascading failures)
- **Retries with backoff:** Exponential backoff for transient failures (network timeouts)

### 5. Exactly-Once vs At-Least-Once vs At-Most-Once

| Guarantee | Meaning | Use Case | Implementation |
|-----------|---------|----------|----------------|
| At-most-once | Message may be lost, never duplicated | Metrics, logs where loss is OK | Fire-and-forget |
| At-least-once | Message delivered ≥1 times, may be duplicated | Most streaming (deduplicate later) | Ack after processing |
| Exactly-once | Message delivered exactly 1 time | Financial transactions, inventory | Idempotent writes + transactional offsets |

- **Exactly-once is expensive:** Requires idempotent sinks + transactional coordination
- **Most systems claim exactly-once:** Actually "effectively exactly-once" (idempotent writes + at-least-once delivery)

### 6. Your WDI Project Analysis
- **Current:** Single PostgreSQL node, no replication
- **GitHub Actions:** If a run fails, you re-run manually (at-least-once, manual dedup)
- **Improvements:**
  - Add PostgreSQL streaming replication for read scaling
  - Make pipeline idempotent (check if data already loaded before inserting)
  - Add checkpointing (track which chunks were processed)

## Hands-On Exercise

1. Set up PostgreSQL streaming replication (primary + replica in Docker)
2. Test failover: stop primary, promote replica, verify reads continue
3. Make your WDI `load.py` idempotent (handle re-runs without duplicates)
4. Research how Kafka achieves "exactly-once" (transactions + idempotent producers)

## Why This Matters

Production pipelines fail. Networks timeout, disks fill up, nodes crash. Fault tolerance isn't an afterthought — it's the difference between a demo and a production system. Your WDI pipeline currently has none. This is your gap.

## Next File
→ `06-Big-Data-Architectures-Lambda-Kappa.md`
