# Spark Unit Testing and Debugging

**Phase:** 3 (Big Data)  
**Prerequisites:** `08-Spark-Streaming-Structured-Streaming.md` (overview)  
**When to Skip:** Only if you have a robust testing strategy for Spark pipelines  
**Projects This Enables:** Production-quality Spark code, CI/CD for big data

## What to Cover

### 1. Testing Philosophy for Spark
- **Unit tests:** Test logic in isolation (small data, local mode)
- **Integration tests:** Test with realistic data sizes (small cluster or local with larger data)
- **End-to-end tests:** Test full pipeline with production-like data
- **Data quality tests:** Schema validation, row count checks, null checks (Great Expectations)

### 2. Unit Testing with pytest

```python
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder         .appName("Test")         .master("local[2]")         .getOrCreate()

@pytest.fixture
def sample_data(spark):
    data = [
        ("USA", 2020, 21000000),
        ("IND", 2020, 13800000),
        ("CHN", 2020, 14300000),
    ]
    return spark.createDataFrame(data, ["country", "year", "population"])

def test_filter_by_year(spark, sample_data):
    result = sample_data.filter(col("year") == 2020)
    assert result.count() == 3

def test_aggregate_population(spark, sample_data):
    from pyspark.sql.functions import sum
    result = sample_data.groupBy("year").agg(sum("population").alias("total"))
    assert result.collect()[0]["total"] == 49100000
```

### 3. Testing Patterns
- **Small data:** Use `createDataFrame()` with 5-10 rows
- **Local mode:** `master("local[2]")` for fast tests
- **Schema validation:** Assert expected columns and types
- **Data quality:** Assert no nulls in critical columns, assert row counts
- **Transformation testing:** Test each transformation function independently
- **End-to-end:** Test full pipeline with sample data

### 4. Debugging Techniques

#### Spark UI
- Identify slow stages and tasks
- Check for data skew (uneven task durations)
- Monitor memory usage and GC time

#### Logging
```python
# Enable debug logging
spark.sparkContext.setLogLevel("DEBUG")

# Add custom logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing partition with {df.count()} rows")
```

#### Local Debugging
```python
# Run on small sample locally
df_sample = df.limit(100).cache()
result = transform(df_sample)
result.show()  # Inspect output
```

#### Checkpoints
```python
# Save intermediate results for inspection
df.write.parquet("debug/intermediate_step_1")
```

### 5. Common Testing Challenges
- **Non-deterministic operations:** `collect()` order may vary (use `sorted()`)
- **Floating point comparisons:** Use approximate equality (`pytest.approx`)
- **Null handling:** Explicitly test null inputs and null outputs
- **Schema evolution:** Test with old and new schema versions
- **Time-dependent tests:** Mock timestamps, don't use `now()` in tests

### 6. CI/CD for Spark
- **GitHub Actions:** Run tests on every PR
- **Small cluster tests:** Use AWS EMR / Databricks for integration tests (nightly)
- **Data generation:** Use libraries like `faker` or `mimesis` for test data
- **Test data versioning:** Store test datasets in Git LFS or S3

### 7. Your WDI Project Testing
- **Current:** `tests/test_data_quality.py` with pytest
- **Spark migration:** Add `tests/test_spark_transformations.py`
- **Test data:** Create a 100-row sample of WDI data for fast tests
- **CI/CD:** GitHub Actions already runs tests — add Spark tests when you migrate

## Hands-On Exercise

1. Write pytest tests for your WDI transformations (in pandas or Spark)
2. Test edge cases: null values, empty strings, invalid dates, duplicate rows
3. Add a test that validates the star schema (correct columns, correct types, FK constraints)
4. Set up GitHub Actions to run Spark tests (use `local[2]` mode, no cluster needed)
5. Measure code coverage with `pytest-cov`

## Why This Matters

Untested Spark code fails in production. The cost of a failed 10-hour Spark job is thousands of dollars. Unit tests catch logic errors before they reach production. Data quality tests catch bad data before it corrupts your warehouse.

## Next File (Phase 4)
→ `08-Data-Lake-and-Lakehouse/01-Data-Lake-Concepts-Design.md`
