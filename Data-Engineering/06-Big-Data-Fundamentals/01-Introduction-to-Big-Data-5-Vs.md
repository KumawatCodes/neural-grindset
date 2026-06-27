# Introduction to Big Data: The 5 V's

**Phase:** 3 (Big Data)  
**Prerequisites:** `05-Data-Warehousing/05-Warehouse-Performance-Tuning.md`  
**When to Skip:** Only if you can explain the 5 V's and their engineering implications  
**Projects This Enables:** Understanding when your data is "big" and needs distributed processing

## What to Cover

### 1. The 5 V's of Big Data

#### Volume
- **Definition:** The amount of data generated and stored
- **Scale:** Terabytes to petabytes to exabytes
- **Examples:** Facebook (4 PB/day), Twitter (500M tweets/day), IoT sensors
- **Engineering challenge:** Storage systems, distributed processing, cost management
- **Your WDI project:** 3.6GB is NOT big data (fits in RAM on a modern laptop)

#### Velocity
- **Definition:** The speed at which data is generated and processed
- **Scale:** Batch (hourly/daily) → Near real-time (seconds) → Real-time (milliseconds)
- **Examples:** Stock trades (microseconds), sensor data (continuous), clickstreams
- **Engineering challenge:** Streaming architectures, low-latency processing, backpressure
- **Your WDI project:** Batch (one-time load), velocity is low

#### Variety
- **Definition:** Different types and sources of data
- **Types:** Structured (SQL), semi-structured (JSON, XML), unstructured (images, video, text)
- **Examples:** CRM data + social media + IoT + logs + images
- **Engineering challenge:** Schema flexibility, data integration, polyglot persistence
- **Your WDI project:** Structured CSV with some categorical dimensions (low variety)

#### Veracity
- **Definition:** Quality, accuracy, and trustworthiness of data
- **Issues:** Inconsistencies, incompleteness, ambiguities, duplicates, latency
- **Examples:** User-entered data with typos, sensor malfunctions, API downtime
- **Engineering challenge:** Data quality frameworks, validation, cleansing, lineage
- **Your WDI project:** World Bank data is high veracity (authoritative source)

#### Value
- **Definition:** The usefulness and insights derived from data
- **Challenge:** Most data is never analyzed ("dark data")
- **Engineering challenge:** Efficient storage, fast querying, relevant aggregation
- **Your WDI project:** Value is clear (GDP vs life expectancy for NGO funding)

### 2. The Big Data Threshold

When do you need "big data" tools?

```
Data Size          | Tool
-------------------|------------------------------------------
< 1 GB             | Python + pandas (local)
1 GB - 10 GB       | Python + pandas (chunked) or DuckDB
10 GB - 100 GB     | Spark (local mode) or cloud warehouse
100 GB - 1 TB      | Spark cluster (3-5 nodes) or BigQuery/Snowflake
1 TB - 100 TB      | Spark cluster (10+ nodes) or cloud warehouse
> 100 TB           | Spark + data lake + cloud warehouse (hybrid)
```

### 3. Your WDI Project Analysis
- **Volume:** 3.6GB → Python + pandas (chunked) is correct ✅
- **Velocity:** Batch → No streaming needed ✅
- **Variety:** Structured CSV → No schema flexibility needed ✅
- **Veracity:** High → Minimal cleansing needed ✅
- **Value:** Clear → Star schema enables the analysis ✅
- **Conclusion:** You do NOT need Spark or Hadoop for this project. Using them would be over-engineering.

### 4. When Big Data Tools Become Necessary
- **Volume grows:** If WDI adds 10 years of data × 1000 indicators × 200 countries = 100M+ rows
- **Velocity increases:** Real-time development indicators (monthly updates)
- **Variety expands:** Add satellite imagery, social media sentiment, survey data
- **Processing complexity:** Machine learning on the data, complex graph analysis

### 5. The Big Data Ecosystem
- **Storage:** HDFS, S3, Azure Data Lake, GCS
- **Processing:** Hadoop MapReduce, Spark, Flink, Hive, Presto/Trino
- **Streaming:** Kafka, Kinesis, Pub/Sub, Pulsar
- **NoSQL:** HBase, Cassandra, MongoDB, Elasticsearch
- **Orchestration:** Airflow, Oozie, Azkaban
- **Query engines:** Hive, Impala, Presto, Drill

## Hands-On Exercise

1. Calculate the size of your WDI dataset in memory (rows × columns × avg bytes per cell)
2. Compare to your laptop's RAM — does it fit?
3. Estimate how big it would need to be to require Spark (10× current size? 100×?)
4. List 3 features you could add to your WDI project that would push it into "big data" territory

## Why This Matters

Big data tools are expensive (infrastructure, complexity, learning curve). Using Spark for 3.6GB is like using a freight truck to deliver a letter. Understand the threshold so you choose the right tool for the job.

## Next File
→ `02-Hadoop-Ecosystem-HDFS-MapReduce-YARN.md`
