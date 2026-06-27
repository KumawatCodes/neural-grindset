# Star Schema Design

**Phase:** 2 (Data Core)  
**Prerequisites:** `04-Denormalization-for-Analytics.md`  
**When to Skip:** Only if you can design a star schema from business requirements and explain trade-offs  
**Projects This Enables:** Your WDI project Silver layer, all dimensional modeling

## What to Cover

### 1. What is a Star Schema?
- **Central fact table:** Contains measurements (metrics, quantities)
- **Surrounding dimension tables:** Contains context (who, what, where, when)
- **Visual shape:** Fact table in center, dimensions radiating out (like a star)
- **Relationship:** Fact table has foreign keys to all dimension tables

### 2. Fact Tables
- **Grain:** The level of detail (one row per what?)
- **Measures:** Numeric values (sales_amount, quantity, temperature)
- **Foreign keys:** References to dimension tables
- **Degenerate dimensions:** Dimensions that are just IDs (order_number, transaction_id)
- **Additive measures:** Can be summed across dimensions (sales_amount)
- **Semi-additive measures:** Can be summed across some dimensions (balance)
- **Non-additive measures:** Can't be summed (ratios, percentages)

### 3. Dimension Tables
- **Surrogate key:** Artificial PK (auto-increment integer, UUID), not the natural key
- **Natural key:** Business key (country_code, indicator_code)
- **Attributes:** Descriptive columns (country_name, region, income_group)
- **Hierarchies:** Natural grouping (Year → Quarter → Month → Day)
- **Slowly Changing Dimensions:** How to handle changes over time (covered in `07-SCD`)

### 4. Star Schema Example: Sales
```
                    dim_date
                        |
                        |
dim_customer ---- fact_sales ---- dim_product
                        |
                        |
                    dim_store
```
- `fact_sales`: sale_id, date_key, customer_key, product_key, store_key, quantity, amount
- `dim_date`: date_key, date, day_of_week, month, quarter, year, is_holiday
- `dim_customer`: customer_key, customer_id, name, city, segment
- `dim_product`: product_key, product_id, name, category, brand
- `dim_store`: store_key, store_id, name, region, country

### 5. Advantages of Star Schema
- **Simple queries:** Join fact + dimensions, no complex paths
- **Fast aggregations:** Fact table is narrow, dimensions are small
- **Intuitive for analysts:** Matches business questions ("sales by region and month")
- **BI tool friendly:** Tableau, PowerBI, Looker optimize for star schemas

### 6. Disadvantages
- **Data redundancy:** Dimension attributes repeated (denormalized)
- **Storage:** More than fully normalized
- **Updates:** Changing a dimension attribute requires updating all related facts
- **Not for OLTP:** Write performance is poor

### 7. Design Process
1. **Identify business process:** What are we measuring? (sales, clicks, temperature)
2. **Declare grain:** One row per what? (per transaction, per day per product, per hour per sensor)
3. **Identify dimensions:** Who, what, where, when, why, how
4. **Identify facts:** What are we measuring? (quantity, amount, count, duration)
5. **Validate:** Can you answer the business questions with this schema?

## Hands-On Exercise

Design a star schema for your WDI project:
1. **Business process:** Measuring development indicators over time
2. **Grain:** One row per country per indicator per year per breakdown (sex, age, urbanisation)
3. **Dimensions:** Country, Indicator, Date, Sex, Age, Urbanisation
4. **Facts:** Value, flag (data quality indicator)
5. Draw the schema. Write the CREATE TABLE statements.

## Why This Matters

This is your WDI project's core architecture. Every decision here affects query performance, storage, and maintainability. Get this right, and your dashboard queries will be fast. Get it wrong, and you'll fight the schema forever.

## Next File
→ `06-Snowflake-Schema-Design.md`
