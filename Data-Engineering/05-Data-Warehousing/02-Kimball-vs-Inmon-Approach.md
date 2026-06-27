# Kimball vs Inmon Approach

**Phase:** 2 (Data Core)  
**Prerequisites:** `01-What-is-a-Data-Warehouse.md`  
**When to Skip:** Only if you can articulate the trade-offs and choose between them for any project  
**Projects This Enables:** Architectural decisions for your WDI project and all future warehouses

## What to Cover

### 1. Ralph Kimball Approach (Bottom-Up)
- **Philosophy:** Start with business requirements, build data marts first, integrate later
- **Process:** Identify business processes → Build dimensional models (star schemas) → Integrate via conformed dimensions
- **Data model:** Dimensional (star/snowflake schemas)
- **ETL strategy:** ETL into data marts, then integrate
- **Team:** Business analysts and data modelers lead
- **Speed:** Faster to first deliverable (first data mart in weeks)
- **Flexibility:** Each mart is independent, can evolve separately
- **Integration:** Via conformed dimensions (shared `dim_date`, `dim_customer`)

### 2. Bill Inmon Approach (Top-Down)
- **Philosophy:** Build enterprise-wide normalized data warehouse first, then create data marts
- **Process:** Model all enterprise data in 3NF → Build central warehouse → Derive data marts from warehouse
- **Data model:** Normalized (3NF) in central warehouse, dimensional in marts
- **ETL strategy:** ETL into central warehouse, then ETL to marts
- **Team:** Enterprise architects and data modelers lead
- **Speed:** Slower to first deliverable (months for central warehouse)
- **Integration:** Built-in, single source of truth
- **Consistency:** Strong data governance, no data silos

### 3. Comparison

| Aspect | Kimball (Bottom-Up) | Inmon (Top-Down) |
|--------|---------------------|------------------|
| Starting point | Business requirements | Enterprise data model |
| First deliverable | Data mart (weeks) | Central warehouse (months) |
| Data model | Dimensional | Normalized (3NF) |
| Integration | Conformed dimensions | Central warehouse |
| Flexibility | High (independent marts) | Low (centralized) |
| Governance | Weaker (marts can diverge) | Stronger (single source) |
| Complexity | Lower (per mart) | Higher (enterprise-wide) |
| Best for | Agile teams, specific use cases | Large enterprises, regulatory needs |

### 4. Modern Hybrid Approach
- **Data Vault (Dan Linstedt):** Raw data vault first (agile), then information marts (dimensional)
- ** medallion architecture (Databricks):** Bronze → Silver → Gold (covered in Phase 3)
- **Modern data stack:** Ingest raw (Fivetran) → Transform in warehouse (dbt) → Serve (BI tools)
- **Reality:** Most teams use Kimball for speed, add governance as they grow

### 5. Your WDI Project Analysis
- **Your approach:** Kimball-ish (bottom-up)
- You have one specific use case (GDP vs life expectancy)
- You built a star schema directly (dimensional model)
- You didn't build a normalized central warehouse first
- **Trade-off:** Fast delivery, but if you add more indicators, you might need to refactor
- **Recommendation:** For your portfolio project, Kimball is correct. For a real enterprise, consider the hybrid.

### 6. When to Choose Which

```
Are you building for a specific business need quickly?
├── YES → Kimball (start with star schema)
│         └── Do you have multiple departments with different needs?
│             ├── YES → Build multiple marts with conformed dimensions
│             └── NO  → One star schema is enough
└── NO  → Inmon or Data Vault (enterprise-wide, regulated)
          └── Do you need full audit trail and history?
              ├── YES → Data Vault
              └── NO  → Inmon (normalized warehouse)
```

## Hands-On Exercise

For 3 scenarios, choose Kimball, Inmon, or Data Vault and justify:
1. A startup needing a dashboard in 2 weeks
2. A bank with 50 source systems and regulatory requirements
3. A mid-size e-commerce company with sales, marketing, and inventory data

## Why This Matters

This is the foundational architectural decision. It determines your timeline, your team structure, your data model, and your governance approach. Most "data warehouse failures" are actually "wrong approach for the context" failures.

## Next File
→ `03-Modern-Cloud-Warehouses-Snowflake-BigQuery-Redshift.md`
