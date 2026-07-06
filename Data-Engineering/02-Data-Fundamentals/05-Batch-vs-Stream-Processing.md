
**Prerequisites:** `04-ETL-vs-ELT-Architecture.md`  
**When to Skip:** Only if you can explain watermarks, windowing, and exactly-once semantics  
**Projects This Enables:** Choosing the right processing paradigm for each use case

---

### PART 1: The Core Distinction — Bounded vs Unbounded Data

The fundamental difference is not "size" or "speed"—it is **boundedness**.

- **Batch Processing:** Operates on **bounded** datasets. The total data volume is finite and known at processing time (e.g., all log files from yesterday). You process this finite set, produce a finite result, and terminate the job.
- **Stream Processing:** Operates on **unbounded** datasets. The data source is infinite and continuously arriving (e.g., user clicks, GPS pings). The processing job runs indefinitely, never reaching a natural termination point.

**The Engineering Implication:** Batch processing has a clear start and end. You can use sorting, shuffling, and multiple passes over data. Stream processing operates under *continuous time pressure*—you must process each event as it arrives, using only the data seen so far, without the luxury of a full picture.

---

### PART 2: Batch Processing — Deep Technical Dive

#### 2.1 Definition & Architecture
```
Input Storage (HDFS/S3)
    |
    | [Read Full Dataset] -- Scanner reads all blocks via FileInputFormat
    v
Stage 1: Map / Partition (Shuffle)
    |
    | -- Data partitioned by key (hash or range)
    | -- Intermediate writes to local disk (spill files)
    v
Stage 2: Reduce / Aggregate (Sort-Merge)
    |
    | -- External sort of spilled files
    | -- Merging, aggregation
    v
Output Storage (HDFS/S3/Warehouse)
```

**Core Technologies:** Apache Spark (RDD/DataFrame), Hadoop MapReduce, Presto/Trino (SQL-on-Engine), Airflow (orchestration).

#### 2.2 Internal Execution Mechanics (Spark as reference)

1. **DAG Generation:** The logical plan is converted to a Directed Acyclic Graph of stages. Shuffle dependencies create stage boundaries.
2. **Pipelined Execution:** Within a stage, transformations are pipelined in-memory. `map()` → `filter()` → `flatMap()` are fused into a single function, avoiding writes to disk between them.
3. **Shuffle Write:** When a stage ends (e.g., `groupByKey` or `join`), each executor partitions its output by the key's hash and writes these partitioned files to *local ephemeral disk*. 
4. **Shuffle Read:** Executors in the next stage read these files from remote executors over the network (HTTP). This is the most expensive operation—network bandwidth + disk I/O.
5. **External Sort:** If the input to a reduce operation exceeds available memory, Spark performs an **external sort**. It fills memory, spills sorted blocks to disk, and then performs a k-way merge on the spills. This is an O(n log n) operation involving significant disk I/O.

#### 2.3 Production Characteristics

- **Latency:** Minutes to hours. The overhead of task scheduling, shuffle, and disk spills dominates.
- **Cost:** Lower. You can use spot/preemptible instances because a failed batch job can simply be re-run (idempotent). Cluster can be torn down immediately after completion.
- **Fault Tolerance:** Straightforward. If an executor dies, the stage is re-run from the last lineage checkpoint. Since data is bounded, recomputation is deterministic.
- **Data Scope:** Processes **all** historical data in the window (e.g., all of 2024's sales). This allows global sorts, accurate counts, and joins that require the full dataset.

---

### PART 3: Stream Processing — Deep Technical Dive

#### 3.1 Definition & Architecture
```
Event Source (Kafka / Kinesis / Pulsar)
    |
    | [Continuous Polling] -- Consumer groups, partition assignment
    v
Stream Processor (Flink / Kafka Streams / Spark Streaming)
    |
    | -- Stateful operations (windows, joins, aggregations)
    | -- Checkpointing (periodic barrier snapshots)
    v
Serving Layer (Elasticsearch / Druid / Materialized Views)
```

**Core Technologies:** Apache Flink (true streaming), Kafka Streams (library), Apache Storm (legacy), Spark Structured Streaming (micro-batch).

#### 3.2 Fundamental Internal Concepts

**A. Windowing (The Bounded Subset)**
Since the stream is unbounded, you cannot aggregate over "all time." You must define windows. The three primary types:

| Window Type | Definition | Use Case |
| :--- | :--- | :--- |
| **Tumbling Window** | Fixed, non-overlapping intervals. e.g., 1-minute windows: [0:00, 0:01), [0:01, 0:02). | Hourly aggregated metrics. |
| **Sliding Window** | Fixed length, overlaps. e.g., 1-minute window sliding every 10 seconds. | Moving averages, rolling trends. |
| **Session Window** | Dynamic length. Closes after a period of inactivity. e.g., user session ends after 5 minutes of no clicks. | User engagement, product journeys. |

**B. Watermarks (Handling Late Data)**
*Problem:* Events arrive out-of-order. A 10:00:01 event might arrive at 10:00:05 due to network latency.
*Solution:* Watermarks are **timestamps** indicating the processor's progress. A watermark of `10:00:05` means: *"I am confident that I will not see any more events with a timestamp <= 10:00:05."*
- **Implementation:** The source injects a periodic watermark. For example, if the maximum timestamp seen so far is T, the watermark might be `T - 5 seconds` (allowing for 5 seconds of latency).
- **Late Data Handling:** Events arriving *after* the watermark passes are discarded, or routed to a side-output for manual correction (if allowed by configuration). Dropping late events is the engineering trade-off for maintaining bounded memory.

**C. State Backends (Distributed In-Memory / On-Disk Storage)**
Stream processors maintain *state*—data that persists across events (e.g., the current aggregation sum for a key).
- **RocksDB (Flink default):** An embedded key-value store that writes to local disk (SSD). This allows state to exceed available RAM. The processor caches hot keys in memory and spills cold keys to disk.
- **Heap-based:** Stores state in the JVM heap. Faster but limited to the container's RAM. If state grows, OOM triggers a catastrophic restart.

**D. Checkpoints & Exactly-Once Semantics**
*The Failure Problem:* If a worker dies, how do we ensure no data is lost (at-least-once) or no data is double-counted (exactly-once)?
- **Barrier Alignment:** Flink injects a "checkpoint barrier" into the source stream. These barriers flow through the DAG. When a subtask receives all barriers from its inputs, it snapshots its current state to durable storage (HDFS/S3).
- **Recovery:** On failure, the entire pipeline rolls back to the last successful checkpoint. All downstream sinks are idempotent or participate in a transaction (e.g., Two-Phase Commit to Kafka).
- **Exactly-Once:** Achieved by the combination of *barrier alignment* (which isolates the snapshot from the processing thread) and *transactional sinks*. The sink writes data to an external system, but only commits the transaction when the checkpoint completes.

#### 3.3 Production Characteristics

- **Latency:** Milliseconds to seconds. Events are processed as they arrive.
- **Cost:** Higher. The pipeline runs 24/7/365 (always-on infrastructure). Requires reserved instances or savings plans to manage cloud costs.
- **Fault Tolerance:** Complex. Requires periodic checkpointing (adds overhead), state recovery (can take minutes for large state), and exactly-once contracts with sinks.
- **Data Scope:** Processes **recent** events. Global historical analysis is impossible without external batch joiners.

---

### PART 4: Micro-Batch — The Engineering Compromise

**Definition:** Process small batches of events at extremely short intervals (e.g., every 5 seconds) rather than event-by-event.
**Implementation:** Spark Structured Streaming uses micro-batch by default. The source is polled for records, and a mini-RDD is built for the batch interval.

**Internal Mechanism (Spark):**
1. The driver periodically (trigger interval) queries the source for new offsets.
2. A new RDD is created containing only the new records.
3. This RDD is processed through the physical plan (scheduled as a regular Spark job).
4. The sink writes the output. A commit protocol ensures exactly-once per micro-batch.

**Pros:** 
- Simpler fault tolerance—re-run the micro-batch if it fails.
- Shuffles and joins work exactly as they do in batch mode (no complex state backends required for simple operations).

**Cons:** 
- Latency floor equals the trigger interval (~1-5 seconds minimum). Not true real-time.
- Processing overhead for each micro-batch (scheduling, task serialization) is high.

**Production Use:** LinkedIn uses micro-batch for notification streams; okay for 10-second latency, not acceptable for fraud detection (needs milliseconds).

---

### PART 5: Historical Evolution — Lambda to Kappa

#### 5.1 Lambda Architecture (2010s)
*Why it existed:* Batch processing (Hadoop) was robust but slow. Stream processing (Storm) was fast but couldn't handle recomputation or global aggregations. 

**The Architecture:**
```
Source (Kafka)
    |
    +----------------------------------+
    |                                  |
    v                                  v
[Batch Layer] (Hadoop)      [Speed Layer] (Storm)
    |                                  |
    | Computes batch views             | Computes real-time views
    | (accurate, high latency)         | (approximate, low latency)
    v                                  v
    +---------> [Serving Layer] <------+
                    |
                    v
                Query Engine
                (merges both views for complete answer)
```

**Internal Pain Points:**
- **Code Duplication:** Logic written twice (MapReduce/Spark for batch; Storm/Flink for speed).
- **Complex Serving:** The serving layer had to merge the two outputs (e.g., "Take batch sum + speed incremental"). This produced inconsistent results due to the speed layer missing late data.
- **Maintenance Nightmare:** Deploying a change required updating both pipelines and ensuring they produced identical logical results.

#### 5.2 Kappa Architecture (Current Standard)
*Why it replaced Lambda:* Apache Kafka (or similar log-based systems) proved capable of retaining massive amounts of data (weeks or months). The *replay* capability made the batch layer redundant.

**The Architecture:**
```
Source -> [Kafka (Unbounded Log)]
            |
            | [Stream Processor] (Flink / Kafka Streams)
            |   -- Consumes from the log
            |   -- Stateful operations
            v
         [Serving Layer] (Materialized views, Elasticsearch, DB)
```

**Core Principle: "Just a stream, replayable"**
- For **Stream processing (real-time):** Consumer reads from the *end* of the Kafka topic.
- For **Batch processing (historical recompute):** The *same* consumer logic is replayed from the *beginning* of the Kafka topic (or from a specific offset). 
- **Single Codebase:** The exact same application binary handles both use cases. To "reprocess," you just start a new consumer instance with an earlier offset.

**Production Adoption:** Uber, Netflix, and LinkedIn largely moved to Kappa. Kafka's retention is set to 7-30 days. For "forever" historical analysis, data is dumped to S3 (Parquet) via Kafka → S3 connectors, and Trino/Presto queries it externally. This merges Kappa for real-time with Data Lake for historical, avoiding the dual-codebase problem.

---

### PART 6: Definitive Technical Comparison Matrix

| Aspect | Batch Processing | Stream Processing | Micro-Batch |
| :--- | :--- | :--- | :--- |
| **Data Boundedness** | Bounded (finite set) | Unbounded (infinite) | Unbounded (segmented into finite mini-batches) |
| **Latency** | Minutes - Hours | Milliseconds - Seconds | 1 - 60 seconds |
| **Processing Model** | DAG / Shuffle / Sort | DAG / Stateful + Windowing | DAG / Mini-batch shuffle |
| **Fault Tolerance** | Re-run failed stage (lineage) | Checkpoint + State recovery (RocksDB) | Re-run mini-batch (atomic) |
| **State Management** | Stateless (data is passed via shuffle) | Stateful (RocksDB/heap for aggregations) | Stateful (RDD checkpointing) |
| **Out-of-Order Data** | Handled by sorting (global time sort) | Handled by Watermarks & Side-outputs | Handled within micro-batch window |
| **Throughput** | Extremely High (Petabytes/day) | Moderate-High (Millions events/sec) | High (depends on interval) |
| **Cost Model** | Spot instances, transient clusters | Always-on instances, reserved | Always-on instances (smaller footprint) |
| **Code Complexity** | Low (standard SQL/RDD) | High (windowing, watermarks, state management) | Medium (structured streaming APIs) |
| **Use Cases** | Daily financial reports, ML model training | Fraud detection, live dashboard, IoT alerts | Clickstream analysis, near-real-time monitoring |

---

### PART 7: Production Engineering View — Failure Scenarios

| Scenario | Batch Response | Stream Response |
| :--- | :--- | :--- |
| **Worker Node Dies** | Task re-assigned to another worker; stage re-run from previous RDD stage. | Checkpoint restoration; state is restored from last durable snapshot; pipeline backfills from that offset. |
| **Network Partition** | Shuffle fetch fails; task retries with backoff. If repeated, job fails and must be manually restarted. | Checkpointing fails; pipeline pauses; after network recovers, it continues from last committed offset. |
| **Storage (Sink) Unavailable** | Job holds the final aggregation in memory/disk; retries the write with exponential backoff; ultimately fails if sink stays down. | Sink commits are transactional; if sink unavailable, the pipeline stalls until sink recovers (prevents data loss but causes backpressure). |
| **Data Skew (Hot Key)** | Shuffle partitions are uneven; one reduce task processes 90% of data. Suffers severe disk spilling and timeouts. | State backend experiences hotspotting; RocksDB takes high read/write load for that key; eventually causes backlog on that partition. Resolved by salting keys. |
| **Schema Change** | Pipeline code must be updated and the entire batch re-run. | If using schema registry, the deserializer may fail on incompatible schemas; strict evolution rules are enforced (Avro/Protobuf). |

---

### PART 8: Expert Decision Tree & Real-World Use Cases

**Decision Framework (Architect's View):**

1. **Latency Requirement:**
   - `> 1 hour` → Batch (Airflow + Spark).
   - `1 min - 1 hour` → Micro-batch (Spark Structured Streaming) or scheduled Batch.
   - `< 1 sec` → Stream (Flink/Kafka Streams).

2. **Data Volume & Retention:**
   - Historical > 30 days → Batch re-processing (Kappa replay from Kafka) or dump to S3/Parquet.
   - Real-time only → Stream with short retention.

3. **State Complexity:**
   - Simple aggregations (count, sum) → Micro-batch works.
   - Complex joins across different streams (e.g., `customer_updates` join `orders`) → True Stream with RocksDB state.

**Real Production Examples:**

| Company | Use Case | Paradigm | Justification |
| :--- | :--- | :--- | :--- |
| **Uber** | Surge Pricing (EAT/POOL) | Stream (Flink) | Milliseconds latency; stateful windowing over location pings; exactly-once for billing accuracy. |
| **Netflix** | Recommendation Pipeline | Batch (Spark) + Kappa (Kafka replay) | User feature generation uses batch (daily recompute for offline models); real-time rank uses streaming. |
| **Robinhood** | Price/Order Execution | Stream (Kafka + Flink) | Sub-second latency required; session windowing over order books. |
| **Stripe** | Fraud Detection | Stream + Batch Hybrid | Stream for immediate low-confidence alerts; Batch for weekly retraining of ML models on full historical transaction logs. |
| **Your WDI Pipeline** | Country Indicators | Batch (Python/Postgres) | 3.6GB static file; no real-time requirement; daily/weekly update is acceptable. Cost minimization dominates. |

---

### PART 9: Your Provided Structure (Augmented with Technical Depth)

#### 1. Batch Processing
- **Definition:** Process data in finite chunks (hours, days). Input dataset is fully bounded.
- **Internal:** Uses Shuffle/Sort/External Merge. Spark DAG with disk spills. Fault tolerance via lineage recomputation.
- **Tools:** Spark, Hadoop MapReduce, Airflow, Cron, SQL engines (Presto).
- **When to use:** Historical analysis, daily reports, large datasets, cost-sensitive. Latency: Minutes to hours.
- **Your WDI:** Batch (full 3.6GB CSV read in Pandas).

#### 2. Stream Processing
- **Definition:** Process events as they arrive in an unbounded sequence.
- **Internal:** Stateful backends (RocksDB), Windowing (Tumbling/Sliding/Session), Watermarks for late events, Checkpointing for exactly-once.
- **Tools:** Flink, Kafka Streams, Storm, Spark Streaming.
- **When to use:** Real-time dashboards, fraud detection, IoT, alerts. Latency: Milliseconds to seconds.
- **Complexity:** High due to state management and out-of-order handling.

#### 3. Key Differences
| Aspect | Batch | Stream |
|--------|-------|--------|
| Data scope | All historical data | Recent data (windowed) |
| Latency | High (hours) | Low (ms-sec) |
| Complexity | Lower | Higher |
| Fault tolerance | Replay batch | State recovery + exactly-once |
| Cost | Lower (spot) | Higher (always-on) |
| Use case | Reports, analytics | Alerts, real-time decisions |

#### 4. Micro-Batch (The Middle Ground)
- **Definition:** Process small batches frequently (every few seconds).
- **Tools:** Spark Structured Streaming (default mode), Flink's mini-batch optimization.
- **Internal:** Standard RDD shuffles executed at fixed intervals. Exactly-once via commit protocol per batch.
- **Pros:** Simpler fault tolerance than true streaming.
- **Cons:** Latency floor equals trigger interval; not true millisecond real-time.

#### 5. Lambda Architecture (Historical)
```
Source → [Batch Layer] → Batch Views (Hadoop)
     → [Speed Layer] → Real-time Views (Storm)
     → [Serving Layer] → Merge both → Query
```
- **Problem:** Two codebases (batch vs speed). Inconsistent merging logic. High maintenance overhead.
- **Status:** Deprecated. Replaced by Kappa.

#### 6. Kappa Architecture (Modern)
```
Source → [Kafka] → [Stream Processor] → [Serving Layer] → Query
```
- Single codebase for batch and stream. Replay the Kafka log for "batch" processing.
- **Preferred** for greenfield projects.
- **Implementation:** Use `kafka.timestamp = ...` to reprocess historical data by setting consumer offset to specific partition/timestamp.

#### 7. When to Use What (Decision Tree)
```
Do you need results in < 1 minute?
├── YES → Stream processing (Kafka + Flink/Spark Streaming)
│         └── Do you need exact aggregation?
│             ├── YES → Windowed processing with watermarks
│             └── NO  → Simple consumer loop
└── NO  → Batch processing (Airflow + Spark/SQL)
          └── How big is the data?
              ├── < 1GB → Python/pandas
              ├── 1GB-100GB → Spark (local mode)
              └── > 100GB → Spark cluster / cloud warehouse
```

---

### PART 10: Why This Matters — The Architect's View

This decision determines:
- **Infrastructure:** Always-on instances vs transient spot clusters.
- **Fault Tolerance:** Replay vs Checkpointing/State Recovery.
- **Data Freshness:** Stale reports vs real-time actionability.
- **Team Skillset:** SQL/DataFrame scripting vs complex stateful application development (event time processing, watermarking, state backends).

**The Expert Rule:** Start with **Batch** unless the business cannot tolerate the latency. Batch is simpler, cheaper, and easier to debug. Only adopt Stream when latency is a binding constraint. Adopt Lambda only for legacy—always prefer Kappa for new design.

---
