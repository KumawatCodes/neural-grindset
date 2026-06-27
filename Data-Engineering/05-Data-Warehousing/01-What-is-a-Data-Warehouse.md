# What is a Data Warehouse?

**Phase:** 2 (Data Core)  
**Prerequisites:** `04-Data-Modeling/08-Data-Vault-Modeling-Overview.md`  
**When to Skip:** Only if you can explain OLAP vs OLTP, columnar storage, and warehouse architecture  
**Projects This Enables:** Understanding your WDI Silver/Gold layers, all analytics infrastructure

## What to Cover

### 1. Definition
- A **centralized repository** for integrated data from multiple sources
- Optimized for **analytical queries** (reads), not transactional processing (writes)
- **Subject-oriented:** Organized by business concepts (sales, customers, products) not by application
- **Integrated:** Data from multiple sources cleaned and standardized
- **Time-variant:** Historical data, not just current state
- **Non-volatile:** Append-only, data is not deleted or updated in place

### 2. OLTP vs OLAP

| Aspect | OLTP (Operational) | OLAP (Analytical) |
|--------|-------------------|-------------------|
| Purpose | Run business operations | Analyze business performance |
| Users | Applications, customers | Analysts, data scientists |
| Queries | Simple, point lookups | Complex, aggregations, scans |
| Data volume | GBs | TBs-PBs |
| Writes | Frequent, small | Rare, bulk loads |
| Reads | Few rows | Millions of rows |
| Normalization | Highly normalized (3NF) | Denormalized (star schema) |
| Schema | Fixed, rigid | Flexible, evolving |
| Examples | PostgreSQL, MySQL | Snowflake, BigQuery, Redshift |

### 3. Data Warehouse Architecture
```
Sources (OLTP, APIs, Files) → 
Staging Area (raw, temporary) → 
Integration Layer (cleaned, conformed) → 
Presentation Layer (star schemas, marts) → 
BI Tools / ML Platforms
```

### 4. Types of Data Warehouses
- **Enterprise Data Warehouse (EDW):** Centralized, all data, all departments
- **Data Mart:** Department-specific subset (sales mart, marketing mart)
- **Virtual Data Warehouse:** Federation across sources without physical centralization
- **Cloud Data Warehouse:** Snowflake, BigQuery, Redshift, Azure Synapse

### 5. ETL in Data Warehousing
- **Extract:** From sources (CDC, full load, incremental)
- **Transform:** Clean, integrate, aggregate (in ETL tool or warehouse)
- **Load:** Into staging, then into presentation layer
- **Modern ELT:** Extract → Load raw → Transform in warehouse (dbt)

### 6. Key Concepts
- **Conformed dimensions:** Same dimension table used across multiple fact tables (e.g., `dim_date` used by sales and inventory)
- **Aggregate tables:** Pre-computed summaries for performance
- **Data marts:** Department-specific views (can be physical tables or logical views)
- **Slowly changing dimensions:** Tracking historical changes (covered in `04-Data-Modeling`)

## Hands-On Exercise

Classify these systems as OLTP or OLAP:
1. Your bank's ATM transaction system
2. Your WDI PostgreSQL database (Silver layer)
3. A Tableau dashboard connected to Snowflake
4. An e-commerce order processing system
5. A marketing analytics platform

## Why This Matters for Your WDI Project

Your WDI pipeline is building a data warehouse:
- **Bronze (Staging):** Raw CSV data
- **Silver (Integration):** Cleaned, conformed star schema in PostgreSQL
- **Gold (Presentation):** Aggregates in Supabase for dashboard
- You're building an OLAP system, not OLTP. Design decisions (denormalization, append-only) reflect this.

## Next File
→ `02-Kimball-vs-Inmon-Approach.md`
