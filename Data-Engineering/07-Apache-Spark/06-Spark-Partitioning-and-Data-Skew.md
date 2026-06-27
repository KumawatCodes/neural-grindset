# Spark Partitioning and Data Skew

**Phase:** 3 (Big Data)  
**Prerequisites:** `05-Spark-Join-Strategies-Broadcast-SortMerge.md`  
**When to Skip:** Only if you can diagnose skew, apply salting, and tune partitions for any dataset  
**Projects This Enables:** Fixing the #1 cause of slow Spark jobs

## What to Cover

### 1. What is Partitioning in Spark?
- **Definition:** Splitting data into chunks that can be processed in parallel
- **RDD partitions:** `rdd.getNumPartitions()`
- **DataFrame partitions:** `df.rdd.getNumPartitions()`
- **Default:** 200 for shuffles (`spark.sql.shuffle.partitions`), file-based for reads

### 2. Types of Partitioning

#### Narrow Transformations (No Shuffle)
- `map()`, `filter()`, `select()`, `withColumn()`
- Each input partition maps to one output partition
- **No data movement:** Fast, efficient

#### Wide Transformations (Shuffle Required)
- `groupBy()`, `join()`, `reduceByKey()`, `distinct()`, `orderBy()`
- Data from multiple input partitions must move to output partitions
- **Expensive:** Network transfer, disk I/O, serialization

### 3. Controlling Partitions

```python
# Repartition (full shuffle, expensive)
df.repartition(100)                    # 100 partitions
df.repartition("country")              # Partition by column
df.repartition(100, "country")       # 100 partitions, partitioned by country

# Coalesce (reduce partitions, no shuffle if possible)
df.coalesce(10)                        # Reduce to 10 partitions (only decreases)

# Partition by when writing
df.write.partitionBy("year", "country").parquet("output")
```

### 4. Data Skew — The #1 Performance Killer
- **Definition:** Uneven distribution of data across partitions
- **Symptom:** One partition has 90% of data, other partitions idle
- **Result:** One executor works for hours, others finish in seconds — job is as slow as the slowest partition
- **Common causes:**
  - Null keys in joins (`NULL` all goes to one partition)
  - Popular keys (e.g., "USA" in country data, "2020" in year data)
  - Natural data distribution (power law, Zipf's law)

### 5. Diagnosing Skew
```python
# Check partition sizes
from pyspark.sql.functions import spark_partition_id, count

df.withColumn("partition_id", spark_partition_id())   .groupBy("partition_id")   .agg(count("*").alias("num_rows"))   .orderBy(col("num_rows").desc())   .show()
```
- If max partition is > 10× average, you have skew

### 6. Fixing Skew

#### Salting (Add Random Prefix)
```python
from pyspark.sql.functions import lit, rand, concat, col

# Add random salt to skewed key
salt_count = 10
skewed_df = df.withColumn("salt", (rand() * salt_count).cast("int"))
skewed_df = skewed_df.withColumn("salted_key", concat(col("skewed_col"), lit("_"), col("salt")))

# Expand small table to match all salts
from pyspark.sql.functions import explode, array
small_df_salted = small_df.withColumn("salt", explode(array([lit(i) for i in range(salt_count)])))
small_df_salted = small_df_salted.withColumn("salted_key", concat(col("skewed_col"), lit("_"), col("salt")))

# Join on salted key, then remove salt
result = skewed_df.join(small_df_salted, "salted_key").drop("salt", "salted_key")
```

#### Isolate and Process Skewed Keys Separately
```python
# Split into skewed and non-skewed
skewed_keys = ["USA", "CHN", "IND"]  # known skewed keys
skewed_df = df.filter(col("country").isin(skewed_keys))
normal_df = df.filter(~col("country").isin(skewed_keys))

# Process separately with different strategies
skewed_result = skewed_df.repartition(100, "country").join(...)  # More partitions for skewed
normal_result = normal_df.join(...)

result = skewed_result.union(normal_result)
```

#### Adaptive Query Execution (Spark 3.0+)
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```
- Spark automatically detects skew and splits partitions

### 7. Best Practices
- **Rule of thumb:** 2-4 tasks per CPU core in cluster
- **Too few partitions:** Under-utilization (cores idle)
- **Too many partitions:** Overhead (task scheduling > processing)
- **For 100GB data:** 200-400 partitions (256-512MB per partition)
- **For 1TB data:** 1000-2000 partitions
- **Shuffle partitions:** `spark.sql.shuffle.partitions` (default 200, increase for large data)
- **Input partitions:** Match to input file sizes (avoid small file problem)

### 8. Your WDI Project Analysis
- **Current size:** 8.9M rows, 3.6GB → fits in single partition locally
- **If scaled to 100M rows:** Partition by `year` (20 partitions) or `country` (200+ partitions)
- **Potential skew:** Some countries have more data points (more indicators, more years)
- **Check:** Run the skew diagnosis query on your WDI data

## Hands-On Exercise

1. Check partition distribution of your WDI DataFrame after loading
2. Create an artificial skew (duplicate one country's rows 100×)
3. Run a `groupBy("country")` and observe one partition taking forever
4. Apply salting and measure improvement
5. Enable AQE and compare

## Why This Matters

Data skew is the most common cause of Spark job failures in production. A job that should take 10 minutes takes 10 hours because one partition has all the data. Learning to diagnose and fix skew separates junior from senior data engineers.

## Next File
→ `07-Spark-Performance-Tuning-Checklist.md`
