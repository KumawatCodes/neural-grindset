# Batch vs Stream Processing

**Phase:** 2 (Data Core)  
**Prerequisites:** `04-ETL-vs-ELT-Architecture.md`  
**When to Skip:** Only if you can explain watermarks, windowing, and exactly-once semantics  
**Projects This Enables:** Choosing the right processing paradigm for each use case

## What to Cover

### 1. Batch Processing
- **Definition:** Process data in chunks (hours, days, weeks)
- **Analogy:** Washing a full load of laundry
- **Tools:** Spark, Hadoop MapReduce, Airflow, cron jobs
- **When to use:** Historical analysis, daily reports, large datasets, cost-sensitive
- **Latency:** Minutes to hours
- **Your WDI pipeline:** Batch (process the full 3.6GB file at once)

### 2. Stream Processing
- **Definition:** Process data as it arrives, record by record
- **Analogy:** Washing each item as it gets dirty
- **Tools:** Kafka Streams, Spark Streaming, Flink, Storm
- **When to use:** Real-time dashboards, fraud detection, IoT, alerts
- **Latency:** Milliseconds to seconds
- **Complexity:** Much higher (state management, fault tolerance, ordering)

### 3. Key Differences

| Aspect | Batch | Stream |
|--------|-------|--------|
| Data scope | All historical data | Recent data (window) |
| Latency | High (hours) | Low (ms-sec) |
| Complexity | Lower | Higher |
| Fault tolerance | Replay batch | State recovery, exactly-once |
| Cost | Lower (spot instances) | Higher (always-on) |
| Use case | Reports, analytics | Alerts, real-time decisions |

### 4. Micro-Batch (The Middle Ground)
- **Definition:** Process small batches frequently (every few seconds)
- **Tools:** Spark Structured Streaming (micro-batch under the hood)
- **Pros:** Near real-time with simpler fault tolerance
- **Cons:** Not true streaming, latency in seconds not ms

### 5. Lambda Architecture (Historical)
```
Source → [Batch Layer] → Batch Views (Hadoop)
     → [Speed Layer] → Real-time Views (Storm)
     → [Serving Layer] → Merge both → Query
```
- **Problem:** Two codebases, complex to maintain
- **Status:** Mostly deprecated, replaced by Kappa

### 6. Kappa Architecture (Modern)
```
Source → [Kafka] → [Stream Processor] → [Serving Layer] → Query
```
- Single codebase for batch and stream
- Replay Kafka topics for batch processing
- **Status:** Preferred for greenfield projects

### 7. When to Use What (Decision Tree)
```
Do you need results in < 1 minute?
├── YES → Stream processing (Kafka + Flink/Spark Streaming)
│         └── Do you need exact aggregation?
│             ├── YES → Windowed processing with watermarks
│             └── NO  → Simple consumer loop
└── NO  → Batch processing (Airflow + Spark/SQL)
          └── How big is the data?
              ├── < 1GB → Python/pandas
              ├── 1GB-100GB → Spark
              └── > 100GB → Spark cluster / cloud warehouse
```

## Hands-On Exercise

Classify these scenarios:
1. Your WDI pipeline (Batch — one-time full load)
2. A stock trading alert system (Stream — real-time)
3. A daily sales report (Batch — daily cron)
4. A live website analytics dashboard (Stream or Micro-batch)

## Why This Matters

This decision determines your entire technology stack. Batch = Airflow + Spark. Stream = Kafka + Flink. Wrong choice = 10x cost and complexity.

## Next File
→ `06-Data-Pipeline-Components-Overview.md`
