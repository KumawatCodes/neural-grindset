# What is Data Engineering?

**Phase:** 2 (Data Core)  
**Prerequisites:** `01-Fundamentals/05-Python-Core-for-Data-Engineering.md`  
**When to Skip:** Never — this is the conceptual foundation  
**Projects This Enables:** Understanding the role, designing your first pipeline

## What to Cover

### 1. The Data Engineering Role
- Data Engineer vs Data Scientist vs Data Analyst vs ML Engineer
- The "data hierarchy of needs" (collect → store → process → analyze → AI/ML)
- Why data engineering is the bottleneck for AI/ML projects

### 2. The Data Lifecycle
1. **Ingestion** — getting data from sources (APIs, databases, files, streams)
2. **Storage** — landing raw data (data lake, warehouse, database)
3. **Transformation** — cleaning, modeling, aggregating (ETL/ELT)
4. **Serving** — making data available for analytics, dashboards, ML
5. **Governance** — quality, security, lineage, compliance

### 3. Types of Data Systems
- **OLTP** (Online Transaction Processing): Fast writes, normalized, row-oriented (PostgreSQL, MySQL)
- **OLAP** (Online Analytical Processing): Fast reads, denormalized, column-oriented (Snowflake, BigQuery)
- **Data Lakes:** Raw storage, schema-on-read (S3, HDFS)
- **Data Lakehouses:** Best of both (Delta Lake, Iceberg)

### 4. The Modern Data Stack
```
Sources → Ingestion (Fivetran/Airbyte) → 
Storage (Snowflake/S3) → 
Transformation (dbt) → 
Orchestration (Airflow) → 
Serving (BI tools, ML platforms)
```

### 5. Key Responsibilities
- Building and maintaining data pipelines
- Ensuring data quality and reliability
- Optimizing performance and cost
- Enabling data discovery and governance
- Supporting analytics and ML teams

## Hands-On Exercise

Map your WDI ETL pipeline to the data lifecycle:
- Where does ingestion happen? (`extract.py`)
- Where is storage? (PostgreSQL Bronze/Silver)
- Where is transformation? (`clean.py`, star schema creation)
- Where is serving? (Supabase Gold, Streamlit dashboard)
- What governance exists? (pytest data quality tests)

## Why This Matters

You can't build what you don't understand. This file is your compass — when confused, return here and ask: "Which part of the lifecycle am I working on?"

## Next File
→ `02-Data-Types-Formats-CSV-JSON-XML.md`
