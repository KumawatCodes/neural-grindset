# Data Pipeline Components Overview

**Phase:** 2 (Data Core)  
**Prerequisites:** `05-Batch-vs-Stream-Processing.md`  
**When to Skip:** Never — this is the blueprint for every pipeline you build  
**Projects This Enables:** Designing your WDI pipeline and all future pipelines

## What to Cover

### 1. The Universal Pipeline Pattern
Every data pipeline, regardless of complexity, has these components:

```
[Sources] → [Ingestion] → [Storage/Staging] → [Transformation] → [Serving] → [Consumption]
                ↓                ↓                    ↓                ↓
           [Monitoring]    [Quality Checks]    [Orchestration]   [Governance]
```

### 2. Component Breakdown

#### Sources
- Databases (CDC, full extract, incremental)
- APIs (REST, GraphQL, webhooks)
- Files (CSV, JSON, Parquet, logs)
- Streams (Kafka, Kinesis, Pub/Sub)
- **Key skill:** Understanding source limitations (rate limits, schema changes, downtime)

#### Ingestion
- **Full load:** Extract everything (good for small, static data)
- **Incremental:** Extract only changes (good for large, changing data)
- **CDC (Change Data Capture):** Real-time change streaming (Debezium)
- **Tools:** Airbyte, Fivetran, custom Python, Kafka Connect
- **Key skill:** Handling failures, retries, idempotency

#### Storage / Staging
- **Raw zone:** Data as-is (data lake, S3, HDFS)
- **Cleaned zone:** Validated, typed data
- **Modeled zone:** Star schema, aggregates
- **Tools:** S3, PostgreSQL, Snowflake, Delta Lake
- **Key skill:** Partitioning, compression, lifecycle policies

#### Transformation
- **Cleansing:** Remove duplicates, handle nulls, fix types
- **Normalization/Denormalization:** Star schema design
- **Aggregation:** Summaries, rollups, KPIs
- **Enrichment:** Join with reference data, geocoding
- **Tools:** dbt, Spark, Python, SQL
- **Key skill:** Writing idempotent transformations

#### Serving
- **Data warehouse:** For BI tools (Snowflake, BigQuery)
- **Data marts:** Department-specific views
- **Feature store:** For ML models
- **APIs:** For applications
- **Tools:** dbt, REST APIs, GraphQL
- **Key skill:** Performance optimization, caching

#### Consumption
- BI tools (Tableau, Looker, Metabase)
- Jupyter notebooks
- ML platforms (SageMaker, Vertex AI)
- Applications (backend services)

### 3. Cross-Cutting Concerns

#### Orchestration
- DAGs (Directed Acyclic Graphs)
- Scheduling, dependencies, retries
- Tools: Airflow, Prefect, Dagster, cron

#### Monitoring & Alerting
- Pipeline success/failure
- Data freshness (SLA monitoring)
- Data volume anomalies
- Tools: Datadog, PagerDuty, custom alerts

#### Data Quality
- Schema validation
- Row count checks
- Null checks
- Referential integrity
- Tools: Great Expectations, dbt tests, custom pytest

#### Governance & Security
- Access control (RBAC)
- Data classification (PII, sensitive)
- Lineage tracking
- Compliance (GDPR, CCPA)

### 4. Your WDI Pipeline Mapped

| Component | Your Implementation | Gap |
|-----------|-------------------|-----|
| Source | World Bank CSV | ✅ |
| Ingestion | `extract.py` (chunked) | ✅ |
| Storage | PostgreSQL (Bronze/Silver) | ✅ |
| Transformation | `clean.py` + star schema | ✅ |
| Serving | Supabase (Gold) | ✅ |
| Orchestration | GitHub Actions | ⚠️ (basic) |
| Monitoring | None | ❌ |
| Data Quality | pytest | ⚠️ (basic) |
| Governance | None | ❌ |

## Hands-On Exercise

Draw your WDI pipeline architecture diagram. Label each component above. Identify 3 gaps you need to fill to make it production-ready.

## Why This Matters

When you design a pipeline, you don't start with tools. You start with this component checklist. "Do I have ingestion? Yes. Do I have quality checks? No." This prevents you from building a pipeline that works once but fails silently in production.

## Next File
→ `03-Databases-and-SQL/01-Relational-Database-Fundamentals.md`
