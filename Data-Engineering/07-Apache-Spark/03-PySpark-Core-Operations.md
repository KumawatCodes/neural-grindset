# PySpark Core Operations

**Phase:** 3 (Big Data)  
**Prerequisites:** `02-RDDs-vs-DataFrames-vs-Datasets.md`  
**When to Skip:** Only if you can write complex PySpark pipelines with joins, aggregations, and window functions without reference  
**Projects This Enables:** Rewriting your WDI pipeline in PySpark, all big data transformations

## What to Cover

### 1. Reading Data
```python
# CSV
df = spark.read.csv("path", header=True, inferSchema=True, sep=",")

# Parquet (recommended for big data)
df = spark.read.parquet("path")

# JSON
df = spark.read.json("path")

# JDBC (databases)
df = spark.read.jdbc(url, table, properties)

# Options
spark.read.option("mode", "DROPMALFORMED")  # Skip bad rows
spark.read.option("nullValue", "NA")        # Treat "NA" as null
```

### 2. Basic Transformations
```python
from pyspark.sql.functions import col, lit, when, coalesce, concat, substring

# Select columns
df.select("col1", "col2")
df.select(col("col1").alias("new_name"))

# Filter rows
df.filter(col("age") > 18)
df.where((col("country") == "USA") & (col("year") >= 2020))

# Add/modify columns
df.withColumn("new_col", col("old_col") * 2)
df.withColumn("category", when(col("score") > 90, "A").otherwise("B"))
df.withColumn("full_name", concat(col("first"), lit(" "), col("last")))

# Drop columns
df.drop("unnecessary_col")

# Rename
df.withColumnRenamed("old_name", "new_name")
```

### 3. Aggregations
```python
from pyspark.sql.functions import count, sum, avg, max, min, stddev, countDistinct

# Simple aggregation
df.groupBy("country").agg(
    count("*").alias("total_records"),
    avg("gdp").alias("avg_gdp"),
    sum("population").alias("total_pop")
)

# Multiple groupings
df.groupBy("country", "year").agg(max("value").alias("max_value"))

# Global aggregation (no groupBy)
df.agg(sum("value").alias("total"))
```

### 4. Joins
```python
# All join types
inner_df = df1.join(df2, "common_col", "inner")
left_df = df1.join(df2, "common_col", "left")
right_df = df1.join(df2, "common_col", "right")
full_df = df1.join(df2, "common_col", "full")

# Multi-column join
joined = df1.join(df2, ["col1", "col2"], "inner")

# Join with different column names
joined = df1.join(df2, df1.id == df2.user_id, "left")

# Broadcast join (for small tables, avoid shuffle)
from pyspark.sql.functions import broadcast
joined = df1.join(broadcast(df2), "common_col")
```

### 5. Window Functions
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead, sum as window_sum

# Define window
window_spec = Window.partitionBy("country").orderBy("year")

# Row number per country
 df.withColumn("rn", row_number().over(window_spec))

# Running total
window_spec = Window.partitionBy("country").orderBy("year").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df.withColumn("running_total", window_sum("value").over(window_spec))

# Year-over-year growth
window_spec = Window.partitionBy("country").orderBy("year")
df.withColumn("prev_year", lag("value", 1).over(window_spec))
df.withColumn("yoy_growth", (col("value") - col("prev_year")) / col("prev_year"))
```

### 6. Writing Data
```python
# Parquet (partitioned)
df.write.partitionBy("year", "country").parquet("output/path")

# Overwrite mode
df.write.mode("overwrite").parquet("output/path")

# Append mode
df.write.mode("append").parquet("output/path")

# JDBC
df.write.jdbc(url, "table", mode="append", properties)
```

### 7. DataFrame ↔ Pandas
```python
# Convert small DataFrame to pandas (careful with memory!)
pandas_df = spark_df.toPandas()

# Convert pandas to Spark DataFrame
spark_df = spark.createDataFrame(pandas_df)

# Arrow optimization (faster conversion)
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
```

## Hands-On Exercise

Rewrite your WDI star schema creation in PySpark:
1. Read the WDI CSV into a DataFrame
2. Create `dim_country` by selecting distinct countries with attributes
3. Create `dim_indicator` by selecting distinct indicators
4. Create `fact_wdi_data` with foreign keys (join with dimension tables)
5. Write each table as Parquet, partitioned appropriately
6. Compare performance and code complexity with your pandas implementation

## Why This Matters

PySpark is the lingua franca of big data engineering. Every cloud data platform (Databricks, AWS Glue, GCP Dataproc, Azure Synapse) uses it. Mastering these operations opens every big data job opportunity.

## Next File
→ `04-Spark-SQL-and-Catalyst-Optimizer.md`
