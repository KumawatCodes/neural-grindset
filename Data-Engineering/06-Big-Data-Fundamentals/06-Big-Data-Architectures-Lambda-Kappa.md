# Big Data Architectures: Lambda vs Kappa

**Phase:** 3 (Big Data)  
**Prerequisites:** `05-Replication-and-Fault-Tolerance.md`  
**When to Skip:** Only if you can design both architectures and explain when to use each  
**Projects This Enables:** Designing streaming + batch hybrid systems

## What to Cover

### 1. Lambda Architecture (Nathan Marz, 2011)

```
                    ┌──────────────┐
                    │   Serving    │
                    │    Layer     │
                    │  (Merge both)│
                    └──────┬───────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │  Batch Layer │                 │ Speed Layer │
    │  (Hadoop/    │                 │ (Storm/     │
    │   Spark)     │                 │  Flink)     │
    └──────┬──────┘                 └──────┬──────┘
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │  Batch Views │                 │ Real-time   │
    │  (Precomputed│                 │ Views       │
    │   accurate)  │                 │ (Approximate)│
    └─────────────┘                 └─────────────┘
```

- **Batch layer:** Process all historical data, produce accurate views (high latency, correct)
- **Speed layer:** Process recent data in real-time, produce approximate views (low latency, fast)
- **Serving layer:** Merge batch and speed views for queries
- **Pros:** Accurate + real-time, fault-tolerant (batch recomputes)
- **Cons:** Two codebases (batch + speed), complex to maintain, operational overhead

### 2. Kappa Architecture (Jay Kreps, 2014)

```
    ┌──────────┐     ┌──────────────┐     ┌──────────────┐
    │  Sources │────▶│    Kafka     │────▶│ Stream Proc  │
    │          │     │  (Log store)  │     │  (Spark/Flink)│
    └──────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           ┌──────▼──────┐
                                           │  Serving    │
                                           │   Views     │
                                           └─────────────┘
```

- **Single codebase:** Only stream processing (no separate batch layer)
- **Replay capability:** Reprocess historical data by replaying Kafka topics
- **Pros:** One codebase, simpler operations, same code for batch and stream
- **Cons:** Requires durable log storage (Kafka), replaying large history is slow

### 3. Lambda vs Kappa Comparison

| Aspect | Lambda | Kappa |
|--------|--------|-------|
| Codebases | 2 (batch + stream) | 1 (stream only) |
| Complexity | High | Lower |
| Accuracy | Exact (batch) + Approximate (speed) | Exact (if replayed) |
| Latency | Low (speed layer) | Low (streaming) |
| Reprocessing | Batch recompute | Replay from Kafka |
| Storage | HDFS + Kafka | Kafka only |
| Maintenance | Hard (two systems) | Easier (one system) |
| Use case | Legacy, complex batch | Greenfield, simple streaming |

### 4. Modern Reality: Neither Pure
- **Most systems use a hybrid:** Batch for historical backfill, streaming for real-time
- **Spark Structured Streaming:** Micro-batch (near real-time) with batch API compatibility
- **Flink:** True streaming with batch mode (unified API)
- **Delta Lake / Iceberg:** Time travel + streaming + batch on same storage
- **The trend:** Kappa is preferred for new projects, Lambda persists in legacy systems

### 5. Your WDI Project Analysis
- **Current:** Pure batch (process full CSV once)
- **If you add monthly updates:** Batch (process new file monthly) or streaming (CDC from World Bank API)
- **Recommendation:** Batch is correct for your use case. Don't add streaming complexity until you have a real-time requirement.
- **Future:** If World Bank offers a real-time API, consider Kappa with Kafka + Spark Streaming

### 6. When to Choose What

```
Do you need real-time processing?
├── NO → Batch only (Airflow + Spark/SQL)
│
└── YES → Do you have historical data that needs reprocessing?
    ├── YES → Lambda (batch for history, stream for real-time)
    │         └── Is this a new project?
    │             ├── YES → Consider Kappa with replay
    │             └── NO  → Lambda (legacy constraint)
    └── NO  → Kappa (stream only, replay if needed)
```

## Hands-On Exercise

1. Draw your WDI pipeline as a Lambda architecture (even though it's batch-only, imagine the streaming layer)
2. Draw your WDI pipeline as a Kappa architecture
3. Compare complexity: which is simpler for your use case?
4. Research one company using Lambda (e.g., Twitter historically) and one using Kappa (e.g., LinkedIn)

## Why This Matters

Architecture decisions are expensive to reverse. Lambda vs Kappa is a fundamental choice that determines your team size, operational complexity, and development velocity. For your WDI project, batch is correct. Know when to upgrade.

## Next File
→ `07-Apache-Spark/01-Spark-Architecture-Driver-Executors.md`
