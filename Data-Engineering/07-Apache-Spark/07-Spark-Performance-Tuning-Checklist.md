# Spark Performance Tuning Checklist

**Phase:** 3 (Big Data)  
**Prerequisites:** `06-Spark-Partitioning-and-Data-Skew.md`  
**When to Skip:** Only if you can systematically tune any Spark job and diagnose performance issues  
**Projects This Enables:** Production Spark optimization, cost reduction, interview preparation

## What to Cover

### 1. The Tuning Process
```
1. Measure baseline (current performance)
2. Identify bottleneck (CPU, memory, network, disk)
3. Apply targeted optimization
4. Measure improvement
5. Repeat until satisfied
```

### 2. Configuration Tuning

#### Memory Configuration
```python
# Executor memory (total)
spark.executor.memory = 4g

# Memory split: execution vs storage (default 0.6 / 0.4)
spark.memory.fraction = 0.8       # Increase if caching heavily
spark.memory.storageFraction = 0.3  # Decrease if mostly transformations

# Off-heap memory (for large shuffles)
spark.executor.memoryOffHeap.enabled = true
spark.executor.memoryOffHeap.size = 2g

# Driver memory (for collect(), broadcast variables)
spark.driver.memory = 2g
```

#### Shuffle Tuning
```python
spark.sql.shuffle.partitions = 400  # Increase for large data (default 200)
spark.shuffle.file.buffer = 1mb   # Larger buffer = fewer disk writes
spark.reducer.maxSizeInFlight = 96m  # Increase for faster shuffle reads
spark.shuffle.sort.bypassMergeThreshold = 200  # Bypass sort for small partitions
```

#### Serialization
```python
# Kryo serialization (faster than Java serialization)
spark.serializer = org.apache.spark.serializer.KryoSerializer
spark.kryo.registrationRequired = false
```

#### Garbage Collection
```python
# Use G1GC for large heaps
spark.executor.extraJavaOptions = -XX:+UseG1GC -XX:MaxGCPauseMillis=200
```

### 3. Code-Level Optimizations

#### Avoid Shuffle
- **Broadcast joins:** For small tables (avoids shuffle)
- **Map-side joins:** Pre-partition data on join key (avoids shuffle)
- **Reduce data before shuffle:** Filter early, select only needed columns
- **Use `reduceByKey` instead of `groupByKey`:** `reduceByKey` combines locally before shuffle

#### Caching Strategy
```python
# Cache only if reused
df.cache()  # or df.persist()
# Unpersist when done
df.unpersist()

# Storage levels
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)  # Spill to disk if memory full
df.persist(StorageLevel.MEMORY_ONLY_SER)  # Serialized in memory (less memory, more CPU)
```

#### Avoid UDFs
- **Built-in functions are optimized by Catalyst:** `when()`, `coalesce()`, `concat()`, `regexp_replace()`
- **UDFs are black boxes:** Catalyst can't optimize inside them
- **Pandas UDFs (Vectorized UDFs):** Faster than regular UDFs, but still avoid if possible
- **Spark SQL expressions:** Prefer `expr()` or `spark.sql()` over UDFs

#### File Format Selection
| Format | Read Speed | Write Speed | Compression | Splittable | Recommendation |
|--------|-----------|-------------|-------------|------------|----------------|
| CSV | Slow | Slow | Poor | Yes | Avoid for big data |
| JSON | Slow | Slow | Poor | No | Avoid for big data |
| Parquet | Fast | Medium | Excellent | Yes | **Default choice** |
| ORC | Fast | Medium | Excellent | Yes | Good for Hive |
| Avro | Medium | Fast | Good | Yes | Good for streaming |

### 4. Monitoring and Debugging

#### Spark UI (http://driver:4040)
- **Jobs tab:** Overall job progress, identify stuck jobs
- **Stages tab:** Task duration, shuffle read/write sizes, identify slow stages
- **Tasks tab:** Individual task metrics, identify skewed tasks
- **Storage tab:** Cached data size, memory usage
- **SQL tab:** Query plans, optimization details
- **Environment tab:** Configuration values

#### Key Metrics to Watch
- **Task time:** Should be roughly equal across tasks (skew = problem)
- **Shuffle read/write:** Large shuffle = bottleneck
- **Spill (memory/disk):** Memory pressure, increase executor memory or reduce partitions
- **GC time:** Should be < 10% of task time (tune GC if higher)

### 5. Common Performance Issues and Fixes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| One task takes forever | Data skew | Salting, AQE, isolate skewed keys |
| All tasks slow | Too much data | Filter early, partition pruning, increase cluster size |
| Shuffle read huge | Unnecessary shuffle | Broadcast joins, map-side joins, reduce data |
| GC time high | Memory pressure | Increase executor memory, reduce cached data, tune GC |
| Spill to disk | Not enough memory | Increase memory, reduce partitions, avoid wide transformations |
| Small files | Too many partitions | Coalesce, adjust input split size |
| Driver OOM | `collect()` on large data | Use `take()`, write to file, increase driver memory |

### 6. Your WDI Project Tuning
- **Current:** Local mode, pandas-based, no tuning needed
- **If migrated to Spark:**
  - Use Parquet instead of CSV (10× faster reads)
  - Partition by `year` when writing
  - Broadcast `dim_country` and `dim_indicator` in joins
  - Cache dimension tables (reused across joins)
  - Tune `spark.sql.shuffle.partitions` based on data size

## Hands-On Exercise

1. Take a slow Spark job (or create one with artificial complexity)
2. Use the Spark UI to identify the bottleneck stage
3. Apply one optimization from this checklist
4. Measure improvement (time, shuffle size, memory usage)
5. Document the before/after in your notes

## Why This Matters

Spark tuning is the difference between a $10/hour job and a $100/hour job. In cloud environments (AWS EMR, Databricks), poor tuning directly translates to higher costs. This checklist is your systematic approach to optimization.

## Next File
→ `08-Spark-Streaming-Structured-Streaming.md`
