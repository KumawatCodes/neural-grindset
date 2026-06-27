# Data Vault Modeling Overview

**Phase:** 2 (Data Core) — **Preview Only, Deep Dive in Phase 6**  
**Prerequisites:** `07-Slowly-Changing-Dimensions-SCD-Type-1-2-3.md`  
**When to Skip:** Skip the deep dive now. Read the overview and return in Phase 6.  
**Projects This Enables:** Enterprise-scale data warehouse design, agile data modeling

## What to Cover (Overview Only)

### 1. What is Data Vault?
- **Invented by:** Dan Linstedt (1990s)
- **Goal:** Agile, scalable, auditable enterprise data warehouse
- **Philosophy:** Store all data, all history, all sources — model later
- **Target audience:** Large enterprises with hundreds of source systems

### 2. Core Components
- **Hubs:** Business keys (unique list of entities, e.g., all customers)
- **Links:** Relationships between hubs (e.g., customer-order relationship)
- **Satellites:** Descriptive attributes and history (e.g., customer name, address over time)
- **Hash keys:** Surrogate keys generated from business keys (deterministic, source-independent)

### 3. Data Vault vs Star Schema

| Aspect | Star Schema | Data Vault |
|--------|-------------|------------|
| Design approach | Business requirements first | Store everything first |
| Agility | Less agile (requires redesign) | More agile (add new sources easily) |
| Complexity | Simpler queries | More complex queries |
| Storage | Less | More (stores all history) |
| Auditability | Lower | Higher (full history, source tracking) |
| Team size | Small-Medium | Large Enterprise |
| Implementation time | Faster | Slower initial setup |

### 4. When to Use Data Vault
- **Enterprise with 50+ source systems:** Need to integrate everything
- **Regulatory requirements:** Full audit trail, data lineage
- **Frequent source changes:** New sources added monthly
- **Data science needs:** Raw data access for ML feature engineering
- **Large team:** Dedicated data vault modelers

### 5. When to Use Star Schema (Your WDI Case)
- **Single source:** One dataset, one format
- **Known requirements:** Specific analytics questions
- **Small team:** You and one teammate
- **Fast delivery:** Need dashboard in weeks, not months
- **Limited storage:** Can't afford to store everything raw

### 6. The Modern Stack: Raw Vault + Business Vault + Information Mart
```
Sources → Raw Vault (Hubs, Links, Satellites) → 
Business Vault (calculated links, derived satellites) → 
Information Mart (star schemas for BI tools)
```
- **Raw Vault:** Store everything as-is from sources
- **Business Vault:** Apply business rules, calculations
- **Information Mart:** Star schemas for specific use cases (this is what analysts query)

### 7. Tools
- dbt (with Data Vault packages)
- WhereScape, VaultSpeed (commercial)
- Custom SQL + Airflow

## Hands-On Exercise (Preview)

Read one case study of a Data Vault implementation (e.g., a bank with 100+ systems). Compare to your WDI project. Why is Data Vault overkill for your use case? When would you need it?

## Why Defer Deep Dive?

Data Vault is powerful but complex. For your WDI project (single source, small team, known requirements), it's massive over-engineering. Learn star schema first. Return to Data Vault when you join an enterprise with 50 source systems and regulatory requirements.

## Return Here After
→ `15-System-Design-and-Architecture/06-Data-Mesh-Principles-and-Implementation.md`

## Next File (Continue Phase 2)
→ `05-Data-Warehousing/01-What-is-a-Data-Warehouse.md`
