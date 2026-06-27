# Hadoop Ecosystem: HDFS, MapReduce, YARN

**Phase:** 3 (Big Data)  
**Prerequisites:** `01-Introduction-to-Big-Data-5-Vs.md`  
**When to Skip:** If you understand distributed storage and batch processing concepts, skim this for historical context  
**Projects This Enables:** Understanding Spark's heritage, distributed systems fundamentals

## What to Cover

### 1. Hadoop Overview
- **History:** Created by Doug Cutting (2006), inspired by Google papers (GFS, MapReduce, Bigtable)
- **Goal:** Store and process petabytes of data on commodity hardware
- **Core principle:** Move computation to data, not data to computation
- **Status:** Legacy — still used in enterprises, but Spark has largely replaced MapReduce

### 2. HDFS (Hadoop Distributed File System)
- **Architecture:** Master (NameNode) + Workers (DataNodes)
- **Block storage:** Files split into 128MB blocks, distributed across nodes
- **Replication:** Each block replicated 3× (default) for fault tolerance
- **Write once, read many:** Optimized for batch processing, not random updates
- **Rack awareness:** Replicas placed on different racks for disaster recovery
- **Limitations:** High latency (not for real-time), small file problem, no transactions

### 3. MapReduce
- **Programming model:** Map → Shuffle → Reduce
- **Map phase:** Transform input data into key-value pairs (parallel across nodes)
- **Shuffle phase:** Sort and group by key (network transfer between nodes)
- **Reduce phase:** Aggregate values by key (parallel across nodes)
- **Example:** Word count
  ```
  Input: "hello world hello"
  Map: (hello, 1), (world, 1), (hello, 1)
  Shuffle: (hello, [1, 1]), (world, [1])
  Reduce: (hello, 2), (world, 1)
  ```
- **Limitations:** High latency (batch only), complex programming model, not iterative

### 4. YARN (Yet Another Resource Negotiator)
- **Purpose:** Resource management and job scheduling
- **Architecture:** ResourceManager (master) + NodeManagers (workers) + ApplicationMasters (per job)
- **Benefits:** Multi-tenancy (run MapReduce, Spark, Hive simultaneously)
- **Resource allocation:** Memory and CPU containers per task

### 5. Hadoop Ecosystem Components
- **Hive:** SQL-like interface on MapReduce (replaced by Spark SQL, Presto)
- **Pig:** Scripting language for data flows (largely deprecated)
- **HBase:** NoSQL database on HDFS (column-family, still used)
- **Sqoop:** Import/export between RDBMS and HDFS (replaced by Spark connectors)
- **Flume:** Log ingestion (replaced by Kafka, Fluentd)
- **Oozie:** Workflow scheduler (replaced by Airflow)
- **Zookeeper:** Coordination service (still used by Kafka, HBase)

### 6. Why Learn Hadoop (Even if Legacy)?
- **Enterprise reality:** Many companies still run Hadoop clusters
- **Spark runs on YARN:** Understanding YARN helps tune Spark on Hadoop
- **HDFS concepts:** Apply to S3, GCS (object storage with similar principles)
- **Distributed systems fundamentals:** Fault tolerance, replication, data locality

### 7. Modern Replacements

| Hadoop Component | Modern Replacement | Why |
|------------------|-------------------|-----|
| MapReduce | Spark | 100× faster, easier programming |
| HDFS | S3 / GCS / Azure Blob | Cheaper, managed, unlimited scale |
| Hive | Spark SQL / Presto / BigQuery | Faster, more features |
| Pig | Spark / dbt | More expressive, better ecosystem |
| Sqoop | Spark JDBC / Kafka Connect | More flexible, streaming support |
| Flume | Kafka / Fluentd / Logstash | Better reliability, ecosystem |
| Oozie | Airflow / Dagster | Better UI, Python-native, more integrations |

## Hands-On Exercise

1. Set up a local Hadoop cluster (Docker) or use a cloud sandbox
2. Run the classic WordCount MapReduce job
3. Compare the code complexity to the equivalent PySpark version
4. Write a reflection: "Would I use Hadoop for a new project in 2026? Why or why not?"

## Why This Matters

Hadoop is the foundation of modern big data. Spark was built to fix MapReduce's problems. Understanding HDFS teaches you distributed storage concepts that apply to S3. Understanding YARN teaches you resource management that applies to Kubernetes.

## Next File
→ `03-Distributed-Systems-CAP-Theorem.md`
