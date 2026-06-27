# RDDs vs DataFrames vs Datasets

**Phase:** 3 (Big Data)  
**Prerequisites:** `01-Spark-Architecture-Driver-Executors.md`  
**When to Skip:** Only if you can choose the right abstraction for any use case and explain performance implications  
**Projects This Enables:** Writing efficient Spark code, choosing the right API

## What to Cover

### 1. RDD (Resilient Distributed Dataset) — Low Level
- **Definition:** Spark's foundational abstraction — distributed collection of objects
- **Creation:** Parallelizing a Python list, reading from HDFS/S3, transforming existing RDDs
- **Characteristics:**
  - Immutable (transformations create new RDDs)
  - Lazy evaluation (nothing happens until action)
  - Fault-tolerant (lineage graph for recomputation)
  - Partitioned (distributed across executors)
- **Operations:**
  - **Transformations (lazy):** `map()`, `filter()`, `flatMap()`, `reduceByKey()`, `join()`
  - **Actions (eager):** `collect()`, `count()`, `reduce()`, `saveAsTextFile()`, `take()`
- **Pros:** Full control, flexibility, can handle any data type
- **Cons:** No optimization, verbose, slower (Python overhead), no SQL support

### 2. DataFrame — High Level (Recommended)
- **Definition:** Distributed collection of data organized into named columns (like pandas DataFrame)
- **Creation:** From RDD, from files (CSV, Parquet, JSON), from database, from pandas
- **Characteristics:**
  - Schema-aware (column names and types)
  - Catalyst optimizer (automatic query optimization)
  - Tungsten execution engine (code generation, memory management)
  - SQL support (`spark.sql()`)
- **Operations:**
  - **Transformations:** `select()`, `filter()`, `groupBy()`, `join()`, `orderBy()`, `withColumn()`
  - **Actions:** `show()`, `collect()`, `count()`, `write()`
- **Pros:** Optimized, concise, SQL-compatible, faster (Catalyst + Tungsten)
- **Cons:** Less flexible for complex objects, type safety at runtime

### 3. Dataset — Type-Safe (Scala/Java Only)
- **Definition:** Type-safe version of DataFrame (compile-time type checking)
- **Available in:** Scala, Java (NOT Python — Python is dynamically typed)
- **Characteristics:**
  - Same optimizations as DataFrame
  - Compile-time type safety (catches errors before runtime)
  - Functional API (map, filter with typed functions)
- **Pros:** Best of both worlds (optimization + type safety)
- **Cons:** Not available in Python (PySpark users use DataFrames)

### 4. Performance Comparison

| Aspect | RDD | DataFrame | Dataset |
|--------|-----|-----------|---------|
| Optimization | None | Catalyst + Tungsten | Catalyst + Tungsten |
| Type safety | Runtime | Runtime | Compile-time |
| SQL support | No | Yes | Yes |
| Python support | Yes | Yes | No |
| Performance | Slowest | Fast | Fast |
| Flexibility | Highest | Medium | Medium |
| Verbosity | High | Low | Low |

### 5. When to Use What

```
Need SQL-like operations or structured data?
├── YES → DataFrame (99% of use cases)
│         └── Need compile-time type safety?
│             ├── YES → Dataset (Scala/Java only)
│             └── NO  → DataFrame (Python/R)
└── NO  → RDD (unstructured data, custom partitioning, legacy code)
          └── Need fine-grained control over data layout?
              ├── YES → RDD
              └── NO  → Consider if DataFrame can work (it usually can)
```

### 6. DataFrame Best Practices
- **Use DataFrames for everything:** Unless you have a specific reason for RDDs
- **Avoid UDFs when possible:** Built-in functions are optimized (Catalyst knows them)
- **Use Spark SQL for complex logic:** Often cleaner than DataFrame API
- **Cache strategically:** `df.cache()` or `df.persist()` for reused DataFrames
- **Avoid `collect()` on large data:** Brings all data to driver (OOM risk)

### 7. Your WDI Project with Spark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, year

spark = SparkSession.builder.appName("WDI").getOrCreate()

# Read CSV (DataFrame API)
df = spark.read.csv("WDI.csv", header=True, inferSchema=True)

# SQL-style query
result = df.filter(col("IndicatorCode") == "NY.GDP.MKTP.CD")     .groupBy("CountryCode", year(col("Date")).alias("Year"))     .agg(avg("Value").alias("AvgGDP"))

# Or using Spark SQL
df.createOrReplaceTempView("wdi")
result = spark.sql('''
    SELECT CountryCode, YEAR(Date) as Year, AVG(Value) as AvgGDP
    FROM wdi
    WHERE IndicatorCode = 'NY.GDP.MKTP.CD'
    GROUP BY CountryCode, YEAR(Date)
''')

result.write.parquet("output/gdp_by_year")
```

## Hands-On Exercise

1. Rewrite your WDI `extract.py` and `clean.py` using PySpark DataFrames
2. Compare code verbosity: pandas vs PySpark
3. Run the same aggregation in both and compare performance (for 8.9M rows, pandas might be faster locally)
4. Increase data size (duplicate rows 10×) and compare again

## Why This Matters

DataFrame is the API you'll use 99% of the time. Understanding RDDs helps you debug and optimize, but don't write new RDD code unless absolutely necessary. The performance difference is 10-100× for complex queries due to Catalyst optimization.

## Next File
→ `03-PySpark-Core-Operations.md`
