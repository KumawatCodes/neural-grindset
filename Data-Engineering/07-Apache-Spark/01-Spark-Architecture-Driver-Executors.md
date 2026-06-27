# Spark Architecture: Driver, Executors, Cluster Manager

**Phase:** 3 (Big Data)  
**Prerequisites:** `06-Big-Data-Fundamentals/06-Big-Data-Architectures-Lambda-Kappa.md`  
**When to Skip:** Only if you can explain Spark's execution model, memory management, and tune a cluster  
**Projects This Enables:** Scaling your WDI project to 100M+ rows, all distributed processing

## What to Cover

### 1. Spark Overview
- **History:** Created at UC Berkeley (2009), open-sourced (2010), donated to Apache (2013)
- **Goal:** General-purpose distributed processing engine, 100× faster than MapReduce
- **Key innovation:** In-memory computing (vs MapReduce's disk-based shuffle)
- **Languages:** Scala (native), Java, Python (PySpark), R (SparkR)
- **Use cases:** ETL, machine learning, graph processing, streaming, SQL analytics

### 2. Spark Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│                    Spark Application                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ Driver  │    │Executor 1│    │Executor 2│    ...     │
│  │ (main)  │◄──►│(worker)  │◄──►│(worker)  │            │
│  └────┬────┘    └────┬────┘    └────┬────┘            │
│       │              │              │                   │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐            │
│  │SparkContext│   │Task 1   │    │Task 3   │            │
│  │/SparkSession│  │Task 2   │    │Task 4   │            │
│  └──────────┘    └─────────┘    └─────────┘            │
└─────────────────────────────────────────────────────────┘
         │
    ┌────▼────┐
    │ Cluster │
    │ Manager│ (YARN, Mesos, Kubernetes, Standalone)
    └─────────┘
```

#### Driver
- **Role:** Main program, runs `main()` method, creates SparkContext/SparkSession
- **Responsibilities:**
  - Convert user code into tasks (DAG of operations)
  - Schedule tasks on executors
  - Coordinate with cluster manager for resources
  - Collect results from executors
- **Location:** Runs on client machine (client mode) or cluster node (cluster mode)
- **Memory:** Critical — if driver OOMs, application fails

#### Executors
- **Role:** Worker processes that run tasks and store data
- **Responsibilities:**
  - Execute tasks assigned by driver (map, filter, reduce, etc.)
  - Store computed data in memory (caching) or disk
  - Read from/write to data sources (HDFS, S3, databases)
- **One per worker node:** Each node runs one executor process with multiple tasks
- **Memory:** Split between execution (computation) and storage (cached data)

#### Cluster Manager
- **Role:** Allocates resources (CPU, memory) across applications
- **Options:**
  - **Standalone:** Spark's built-in manager (simple, development)
  - **YARN:** Hadoop's resource manager (enterprise Hadoop clusters)
  - **Mesos:** General cluster manager (less common now)
  - **Kubernetes:** Modern cloud-native choice (recommended for new projects)

### 3. Spark Application Lifecycle
1. **Submit application:** `spark-submit` or notebook
2. **Driver starts:** Creates SparkSession, connects to cluster manager
3. **Request resources:** Cluster manager allocates executors
4. **DAG creation:** Driver builds logical plan, optimizes, generates physical plan
5. **Task scheduling:** Driver sends tasks to executors
6. **Execution:** Executors run tasks, shuffle data, write results
7. **Completion:** Driver collects final results, releases resources

### 4. Deployment Modes

| Mode | Driver Location | Use Case |
|------|----------------|----------|
| Local | Same JVM as application | Development, testing |
| Client | User's machine | Interactive (notebooks, REPL) |
| Cluster | Worker node | Production, long-running jobs |

### 5. Key Configuration
- `spark.executor.instances`: Number of executors
- `spark.executor.memory`: Memory per executor (e.g., 4g)
- `spark.executor.cores`: Cores per executor (e.g., 2)
- `spark.driver.memory`: Driver memory (e.g., 2g)
- `spark.sql.shuffle.partitions`: Number of partitions for shuffle (default 200, tune for data size)

### 6. Common Issues
- **Driver OOM:** Collecting too much data to driver (`collect()` on large dataset)
- **Executor OOM:** Too much data cached, or too large partitions
- **Shuffle spill:** Not enough memory for shuffle, spills to disk (slow)
- **Data skew:** Uneven partition sizes (one executor does all the work)
- **Small files problem:** Too many tiny partitions (overhead > processing)

## Hands-On Exercise

1. Start a local Spark session:
   ```python
   from pyspark.sql import SparkSession
   spark = SparkSession.builder        .appName("WDI-Analysis")        .master("local[*]")        .getOrCreate()
   ```
2. Load your WDI CSV into a Spark DataFrame
3. Check the number of partitions (`df.rdd.getNumPartitions()`)
4. Repartition by `year` and compare performance
5. Monitor the Spark UI (http://localhost:4040) during execution

## Why This Matters

Spark is the industry standard for big data processing. Even if your WDI project doesn't need it now, understanding Spark architecture prepares you for:
- Scaling to 100M+ rows
- Cloud data engineering jobs (AWS Glue, Databricks, GCP Dataproc)
- Streaming pipelines (Spark Structured Streaming)
- ML feature engineering (Spark MLlib)

## Next File
→ `02-RDDs-vs-DataFrames-vs-Datasets.md`
