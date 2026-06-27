# Snowflake Schema Design

**Phase:** 2 (Data Core)  
**Prerequisites:** `05-Star-Schema-Design.md`  
**When to Skip:** Only if you understand the trade-off between star and snowflake and can choose appropriately  
**Projects This Enables:** Normalized warehouse design, storage optimization

## What to Cover

### 1. What is a Snowflake Schema?
- **Extension of star schema:** Dimensions are normalized into sub-dimensions
- **Visual shape:** Like a snowflake (more branches than a star)
- **Relationship:** Dimension tables have their own dimension tables

### 2. Snowflake Example: Sales
```
                    dim_date
                        |
                        |
dim_customer ---- fact_sales ---- dim_product
      |                             |
      |                             |
dim_city                      dim_category
      |                             |
dim_country                   dim_brand
```
- `dim_customer` references `dim_city`, which references `dim_country`
- `dim_product` references `dim_category`, which references `dim_brand`

### 3. Star vs Snowflake Comparison

| Aspect | Star Schema | Snowflake Schema |
|--------|-------------|------------------|
| Normalization | Denormalized dimensions | Normalized dimensions |
| Storage | More (redundancy) | Less (no redundancy) |
| Query complexity | Simple (fewer joins) | Complex (more joins) |
| Query performance | Faster reads | Slower reads (more joins) |
| Maintenance | Easier (fewer tables) | Harder (more tables) |
| Data integrity | Lower (redundancy risk) | Higher (normalized) |
| BI tool support | Excellent | Good |

### 4. When to Choose Snowflake
- **Storage is expensive:** Reducing redundancy matters
- **Dimensions are large:** Normalization saves significant space
- **Dimensions change frequently:** Normalized updates affect fewer rows
- **Query patterns are predictable:** You can optimize the specific joins
- **Data integrity is critical:** Financial data, regulatory compliance

### 5. When to Choose Star
- **Query performance is priority:** Most analytics workloads
- **Storage is cheap:** Cloud warehouses (Snowflake, BigQuery)
- **Analysts need simple SQL:** Fewer joins = fewer mistakes
- **Dimensions are small:** Redundancy overhead is minimal
- **Rapid iteration:** Easier to modify, faster to develop

### 6. Hybrid Approach (Galaxy Schema / Fact Constellation)
- Multiple fact tables sharing dimension tables
- Example: `fact_sales` and `fact_inventory` both use `dim_product` and `dim_date`
- Common in enterprise data warehouses
- More complex but avoids duplicate dimensions

### 7. Modern Data Warehouse Reality
- **Snowflake (the company):** Optimized for star schemas, storage is cheap
- **BigQuery:** Columnar storage, denormalization is fine
- **Recommendation:** Start with star schema, normalize to snowflake only if storage or integrity demands it

## Hands-On Exercise

Take your WDI star schema and snowflake it:
1. Which dimensions could be normalized further?
2. What are the trade-offs for your specific dataset?
3. Given that your dataset is 8.9M rows and dimensions are small, which is better?
4. Write the CREATE TABLE statements for both and compare

## Why This Matters

Your WDI project uses a star schema (6 dimension tables + 1 fact table). Understanding snowflake helps you defend that choice and know when to deviate. Most modern warehouses prefer star for simplicity.

## Next File
→ `07-Slowly-Changing-Dimensions-SCD-Type-1-2-3.md`
