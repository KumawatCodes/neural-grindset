# Spark SQL and Catalyst Optimizer

**Phase:** 3 (Big Data)  
**Prerequisites:** `03-PySpark-Core-Operations.md`  
**When to Skip:** Only if you can read query plans, understand optimization rules, and tune Spark SQL performance  
**Projects This Enables:** Writing efficient Spark SQL, debugging slow queries, interview preparation

## What to Cover

### 1. Spark SQL
- **Definition:** SQL interface on top of Spark's distributed engine
- **Usage:** `spark.sql("SELECT ...")` or DataFrame API (which compiles to Spark SQL)
- **Advantages:** Familiar syntax, optimization by Catalyst, interoperability with BI tools
- **Limitations:** Not all SQL features supported (no stored procedures, limited window functions vs PostgreSQL)

### 2. Catalyst Optimizer Architecture
```
User Query (SQL/DataFrame)
    ↓
Unresolved Logical Plan (parsed, not validated)
    ↓
Analysis (resolve columns, tables, types)
    ↓
Resolved Logical Plan
    ↓
Catalyst Optimizer (rules-based + cost-based)
    ↓
Optimized Logical Plan
    ↓
SparkPlanner (generate physical plans)
    ↓
Physical Plan (specific operations)
    ↓
Code Generation (Tungsten)
    ↓
RDD Execution
```

### 3. Optimization Rules (What Catalyst Does)
- **Predicate pushdown:** Filter early, at data source if possible
- **Column pruning:** Only read columns you need (especially important for Parquet)
- **Constant folding:** Replace `1 + 2` with `3` at compile time
- **Join reordering:** Smaller tables first, broadcast joins for small tables
- **Partition pruning:** Skip partitions that don't match query filters
- **Aggregate pushdown:** Push aggregates to data source if supported

### 4. Reading Query Plans
```python
# Explain plan
df.explain()           # Simple
df.explain(True)       # Extended (parsed, analyzed, optimized, physical)
df.explain("formatted") # Formatted tree
```

**Key indicators of good plan:**
- `FileScan parquet [only_needed_columns]` (column pruning works)
- `Filter [condition]` before `Exchange` (predicate pushdown works)
- `BroadcastHashJoin` (small table broadcasted, no shuffle)
- `PartitionFilters` (partition pruning works)

**Key indicators of bad plan:**
- `Exchange` (shuffle) on large datasets
- `SortMergeJoin` when one table is small (should be broadcast)
- `FileScan` reading all columns (no column pruning)
- `Filter` after `Exchange` (predicate not pushed down)

### 5. Tuning Spark SQL
- **Broadcast threshold:** `spark.sql.autoBroadcastJoinThreshold` (default 10MB, increase for larger small tables)
- **Shuffle partitions:** `spark.sql.shuffle.partitions` (default 200, tune based on data size)
- **Adaptive query execution (AQE):** `spark.sql.adaptive.enabled` (Spark 3.0+, automatically optimizes during execution)
- **Statistics:** `ANALYZE TABLE` for cost-based optimization

### 6. Spark SQL vs DataFrame API
- **Same execution:** Both compile to the same optimized plan
- **Choose based on:** Team skills, query complexity, readability
- **Recommendation:** Use SQL for complex analytics, DataFrame API for ETL pipelines
- **Hybrid:** `spark.sql()` for complex queries, DataFrame API for transformations

### 7. Your WDI Project with Spark SQL
```python
# Register tables
df.createOrReplaceTempView("wdi_raw")

# Complex analytics with SQL
result = spark.sql('''
    WITH gdp_data AS (
        SELECT CountryCode, Year, Value as GDP
        FROM wdi_raw
        WHERE IndicatorCode = 'NY.GDP.MKTP.CD'
    ),
    life_exp_data AS (
        SELECT CountryCode, Year, Value as LifeExp
        FROM wdi_raw
        WHERE IndicatorCode = 'SP.DYN.LE00.IN'
    )
    SELECT 
        g.CountryCode,
        g.Year,
        g.GDP,
        l.LifeExp,
        g.GDP / NULLIF(l.LifeExp, 0) as GDP_per_LifeExp
    FROM gdp_data g
    JOIN life_exp_data l ON g.CountryCode = l.CountryCode AND g.Year = l.Year
    WHERE g.Year >= 2000
    ORDER BY g.Year, g.GDP DESC
''')
```

## Hands-On Exercise

1. Take a complex query from your WDI project and run `explain(True)`
2. Identify which optimizations Catalyst applied
3. Force a bad plan (e.g., disable broadcast joins) and compare performance
4. Enable AQE and observe if performance improves on skewed data
5. Compare query plans: DataFrame API vs equivalent Spark SQL

## Why This Matters

Catalyst is why Spark is 100× faster than hand-written MapReduce. Understanding it helps you:
- Write queries that optimize well (filter early, avoid UDFs)
- Debug slow queries (read the plan, find the bottleneck)
- Tune configurations (shuffle partitions, broadcast threshold)
- Pass Spark optimization questions in interviews

## Next File
→ `05-Spark-Join-Strategies-Broadcast-SortMerge.md`
