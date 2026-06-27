# Distributed Systems: CAP Theorem

**Phase:** 3 (Big Data)  
**Prerequisites:** `02-Hadoop-Ecosystem-HDFS-MapReduce-YARN.md`  
**When to Skip:** Only if you can explain CAP, PACELC, and choose systems based on these trade-offs  
**Projects This Enables:** Understanding database trade-offs, designing resilient systems

## What to Cover

### 1. The CAP Theorem (Eric Brewer, 2000)
- **Statement:** In a distributed data store, you can only guarantee two of three:
  - **C**onsistency: Every read gets the most recent write (or an error)
  - **A**vailability: Every request gets a response (not necessarily the most recent)
  - **P**artition tolerance: System continues operating despite network partitions

- **Reality:** Network partitions happen (P is mandatory), so you choose CP or AP

### 2. The Trade-offs

#### CP Systems (Consistency + Partition tolerance)
- **Sacrifice:** Availability (system may refuse requests during partition)
- **Examples:** PostgreSQL, HBase, MongoDB (configured), ZooKeeper, etcd
- **Use case:** Financial transactions, inventory management, where wrong data is worse than no data
- **Behavior during partition:** Return error or wait until partition heals

#### AP Systems (Availability + Partition tolerance)
- **Sacrifice:** Consistency (may return stale data)
- **Examples:** Cassandra, DynamoDB, Couchbase, Riak
- **Use case:** Social media feeds, session stores, where stale data is acceptable
- **Behavior during partition:** Continue serving requests, reconcile later

#### CA Systems (Consistency + Availability)
- **Sacrifice:** Partition tolerance
- **Examples:** Traditional single-node databases (MySQL, PostgreSQL without replication)
- **Reality:** Not truly distributed, so partition tolerance is trivially satisfied (no network to partition)

### 3. PACELC Theorem (Extended CAP)
- **Statement:** If there is a Partition (P), choose between Availability (A) and Consistency (C). Else (E), choose between Latency (L) and Consistency (C).
- **Insight:** Even without partitions, you trade latency for consistency

### 4. Practical Examples

| System | CAP Choice | Why |
|--------|-----------|-----|
| PostgreSQL (single node) | CA | No distribution, so no partition issue |
| PostgreSQL (replicated) | CP | Synchronous replication ensures consistency |
| Cassandra | AP | Tunable consistency (ONE, QUORUM, ALL) |
| MongoDB (default) | CP | Primary-secondary, writes to primary |
| DynamoDB | AP | Eventually consistent by default (can request strong) |
| Kafka | CP (for ordering) | Partition leader, ISR list |
| Redis (cluster) | AP | Async replication, may lose writes |

### 5. Consistency Models (Beyond CAP)
- **Strong consistency:** Every read sees the latest write (CP systems)
- **Eventual consistency:** Reads may see stale data, but will converge (AP systems)
- **Causal consistency:** Preserves因果关系 (if A caused B, everyone sees A before B)
- **Read-your-writes:** Your reads see your writes (session guarantee)
- **Monotonic reads:** If you read a value, subsequent reads see same or newer value

### 6. Your WDI Project Analysis
- **PostgreSQL (single node):** CA (not distributed, so trivially partition-tolerant)
- **If you add read replicas:** CP (synchronous replication) or AP (async replication)
- **Supabase (cloud):** Depends on configuration, likely CP with read replicas
- **Kafka (if you add streaming):** CP for ordering, AP for availability with configurable ISR

### 7. Engineering Implications
- **Banking:** CP (can't afford to double-spend)
- **Social media:** AP (stale feed is better than no feed)
- **E-commerce cart:** AP (add to cart must work), CP at checkout (inventory check)
- **Analytics:** AP (stale data is fine for dashboards), CP for financial reports

## Hands-On Exercise

1. For 5 scenarios, choose CP or AP and justify:
   - ATM withdrawal
   - Instagram like count
   - Airline seat reservation
   - Real-time analytics dashboard
   - Medical records system
2. Configure Cassandra consistency levels (ONE, QUORUM, ALL) and observe behavior
3. Research how your favorite app handles network partitions (e.g., WhatsApp offline messages)

## Why This Matters

Every database choice is a CAP trade-off. You can't have it all. Understanding this prevents you from choosing Cassandra for banking (AP) or PostgreSQL for a global social feed (single-node CA).

## Next File
→ `04-Data-Partitioning-and-Sharding.md`
