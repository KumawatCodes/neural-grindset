# Modern Cloud Warehouses: Snowflake, BigQuery, Redshift

**Phase:** 2 (Data Core) — **Overview Only, Deep Dive in Phase 5**  
**Prerequisites:** `02-Kimball-vs-Inmon-Approach.md`  
**When to Skip:** Skip deep dive now. Return in Phase 5. Read the overview to understand the landscape.  
**Projects This Enables:** Technology selection for your Gold layer and future projects

## What to Cover (Overview)

### 1. Why Cloud Warehouses?
- **Separation of storage and compute:** Scale independently (Snowflake, BigQuery)
- **Pay-per-use:** No upfront hardware costs
- **Auto-scaling:** Handle peak loads without manual intervention
- **Managed service:** No DBA needed for patching, backups, tuning
- **Integration:** Native connectors to cloud storage, BI tools, ML platforms

### 2. Snowflake
- **Architecture:** Multi-cluster shared data (storage on S3/Azure/GCP, compute on virtual warehouses)
- **Key features:**
  - Zero-copy cloning (instant dev/test environments)
  - Time travel (undo changes, query historical data)
  - Data sharing (share data across accounts without copying)
  - Snowpark (run Python/Java/Scala in Snowflake)
  - Native semi-structured support (JSON, Parquet, Avro)
- **Pricing:** Storage + compute (credits per second of warehouse usage)
- **Best for:** Enterprises, data sharing, complex transformations

### 3. BigQuery
- **Architecture:** Serverless, fully managed (no clusters to manage)
- **Key features:**
  - Columnar storage (Capacitor format)
  - Dremel execution engine (massively parallel)
  - Standard SQL (ANSI SQL compliant)
  - BigQuery ML (train ML models with SQL)
  - BI Engine (in-memory caching for dashboards)
  - Streaming inserts (real-time data)
- **Pricing:** Storage + query processing (per TB scanned)
  - **Important:** Can be expensive with unoptimized queries
- **Best for:** Ad-hoc analytics, Google Cloud ecosystems, cost-conscious with optimization

### 4. Amazon Redshift
- **Architecture:** Massively Parallel Processing (MPP) with leader node and compute nodes
- **Key features:**
  - RA3 nodes with managed storage (separate storage and compute)
  - Spectrum (query S3 directly without loading)
  - AQUA (hardware acceleration for queries)
  - Concurrency scaling (auto-add clusters for peak loads)
  - Integration with AWS ecosystem (S3, Glue, Athena, SageMaker)
- **Pricing:** On-demand or reserved instances (per node per hour)
- **Best for:** AWS ecosystems, heavy ETL workloads, predictable usage

### 5. Comparison

| Feature | Snowflake | BigQuery | Redshift |
|---------|-----------|----------|----------|
| Architecture | Multi-cluster | Serverless | MPP clusters |
| Separation S/C | Yes | Yes (sort of) | Yes (RA3) |
| Scaling | Auto (warehouse size) | Automatic | Manual + concurrency scaling |
| Pricing model | Credits | Per query + storage | Per node + storage |
| SQL dialect | Snowflake SQL | Standard SQL | PostgreSQL-ish |
| Semi-structured | Excellent | Good | Fair |
| ML integration | Snowpark | BigQuery ML | SageMaker |
| Data sharing | Excellent | Good | Fair |
| Cost control | Moderate | Needs attention | Predictable |
| Best for | Enterprise, sharing | Ad-hoc, GCP | ETL, AWS |

### 6. Your WDI Project
- **Current:** PostgreSQL (Silver) → Supabase (Gold)
- **Supabase is PostgreSQL-as-a-service:** Not a cloud warehouse, but sufficient for your scale
- **If you scale:** Migrate Gold to Snowflake/BigQuery for better analytics performance
- **For portfolio:** Supabase is fine. Mention in README that you'd migrate to Snowflake for production scale.

## Hands-On Exercise (Preview)

Sign up for free tiers:
1. Snowflake free trial (30 days, $400 credits)
2. BigQuery sandbox (free tier, 1TB query/month)
3. Run the same query on both, compare performance and cost

## Why Defer Deep Dive?

Cloud warehouses are expensive to learn hands-on. Master PostgreSQL first (your Silver layer), then migrate knowledge to cloud warehouses. The SQL is the same; the optimization is different.

## Return Here After
→ `11-Cloud-Platforms/02-AWS-Core-Services-S3-EC2-IAM.md`

## Next File (Continue Phase 2)
→ `04-Columnar-Storage-and-Massively-Parallel-Processing.md`
