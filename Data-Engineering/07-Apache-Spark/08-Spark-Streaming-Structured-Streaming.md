# Spark Streaming: Structured Streaming

**Phase:** 3 (Big Data) — **Preview, Deep Dive in Phase 4**  
**Prerequisites:** `07-Spark-Performance-Tuning-Checklist.md`  
**When to Skip:** Skip now. Return in Phase 4 (Streaming). Read overview to understand the concept.  
**Projects This Enables:** Real-time data processing, event-driven pipelines

## What to Cover (Overview)

### 1. Spark Streaming Evolution
- **DStreams (Spark 1.x):** Original API, RDD-based, micro-batch
- **Structured Streaming (Spark 2.0+):** DataFrame-based, unified batch/streaming API
- **Continuous Processing (Spark 2.3+):** Experimental, true streaming (ms latency)

### 2. Structured Streaming Concepts
- **Unbounded table:** Stream = table that keeps growing
- **Trigger:** How often to process new data (micro-batch interval)
- **Watermark:** Late data tolerance (how long to wait for late events)
- **Output modes:**
  - **Append:** Only new rows (for streaming aggregations with watermark)
  - **Complete:** Entire result table (for aggregations without watermark)
  - **Update:** Changed rows only (for stateful operations)

### 3. Basic Example
```python
from pyspark.sql.functions import col, window

# Read stream from Kafka
stream_df = spark.readStream     .format("kafka")     .option("kafka.bootstrap.servers", "localhost:9092")     .option("subscribe", "wdi-updates")     .load()

# Process
result = stream_df.selectExpr("CAST(value AS STRING)")     .select(from_json(col("value"), schema).alias("data"))     .select("data.*")     .groupBy(window(col("timestamp"), "1 hour"), col("country"))     .agg(avg("gdp").alias("avg_gdp"))

# Write stream
query = result.writeStream     .outputMode("append")     .format("parquet")     .option("path", "output/streaming")     .option("checkpointLocation", "checkpoint")     .start()

query.awaitTermination()
```

### 4. Key Concepts (Preview)
- **Exactly-once semantics:** Idempotent sinks + transactional offsets
- **Fault tolerance:** Checkpointing and WAL (Write-Ahead Log)
- **State store:** For stateful operations (aggregations over windows), stored in HDFS/S3
- **Joins with static data:** Stream + batch join (e.g., stream of events + lookup table)
- **Joins with streams:** Stream + stream join (complex, requires watermarking)

### 5. When to Use Spark Streaming
- **Micro-batch processing:** Near real-time (seconds to minutes latency)
- **Complex stateful operations:** Windowed aggregations, sessionization
- **Integration with Spark ecosystem:** MLlib, GraphX, Spark SQL
- **Not for:** True real-time (ms latency — use Flink), simple event routing (use Kafka Streams)

### 6. Your WDI Project (Future)
- **Current:** Batch processing of full CSV
- **Future scenario:** World Bank publishes monthly updates via API
  - **Option 1:** Monthly batch job (Airflow + Spark) — simpler, sufficient
  - **Option 2:** Streaming ingestion (Kafka + Spark Streaming) — overkill for monthly updates
  - **Recommendation:** Batch until you have daily or hourly updates

## Hands-On Exercise (When You Return in Phase 4)

1. Set up a local Kafka broker
2. Produce WDI-like messages to a topic
3. Consume with Spark Structured Streaming
4. Apply windowed aggregation (hourly average by country)
5. Handle late data with watermarks

## Why Defer Deep Dive?

Streaming adds massive complexity (fault tolerance, state management, exactly-once). Your WDI project has no real-time requirement. Master batch processing first, then add streaming when you have a genuine use case.

## Return Here After
→ `09-Data-Ingestion-and-Streaming/01-Data-Ingestion-Patterns-and-Strategies.md`

## Next File (Continue Phase 3)
→ `09-Spark-Unit-Testing-and-Debugging.md`
