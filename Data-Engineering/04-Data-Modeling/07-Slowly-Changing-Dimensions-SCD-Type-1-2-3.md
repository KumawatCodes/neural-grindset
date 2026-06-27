# Slowly Changing Dimensions (SCD): Type 1, 2, 3

**Phase:** 2 (Data Core)  
**Prerequisites:** `06-Snowflake-Schema-Design.md`  
**When to Skip:** Only if you can implement SCD Type 2 with effective dates and explain when to use each type  
**Projects This Enables:** Tracking historical changes in your WDI dimensions (country renames, indicator redefinitions)

## What to Cover

### 1. What are Slowly Changing Dimensions?
- **Definition:** Dimension attributes that change over time, but not frequently
- **Examples:** Customer address, product category, employee department, country name
- **Problem:** If a customer moves, do we update their old orders to show the new address?
- **Answer:** It depends on the business requirement — that's what SCD types solve

### 2. SCD Type 0: Fixed (Rare)
- **Rule:** Never change dimension attributes
- **Use case:** Date dimensions (January 1st 2020 will always be January 1st 2020)
- **Implementation:** Standard table, no special handling

### 3. SCD Type 1: Overwrite
- **Rule:** Update the dimension row in place, lose history
- **Use case:** Correcting errors, when history doesn't matter
- **Example:** Fixing a typo in a customer name
- **Implementation:** Simple `UPDATE` statement
- **Pros:** Simple, no extra storage
- **Cons:** No history, can't answer "what was the value before?"

### 4. SCD Type 2: Add New Row (Most Common)
- **Rule:** Add a new row with new values, keep old row with effective dates
- **Use case:** When history matters (tracking customer address changes, product price history)
- **Implementation:**
  - Add `effective_date` and `expiration_date` columns
  - Add `is_current` flag (or check `expiration_date IS NULL`)
  - Surrogate key auto-increments, natural key stays the same
- **Example:**
  ```
  customer_key | customer_id | address     | effective_date | expiration_date | is_current
  1            | C001        | 123 Main St | 2020-01-01     | 2022-06-15      | N
  2            | C001        | 456 Oak Ave | 2022-06-16     | NULL            | Y
  ```
- **Pros:** Full history, can answer "what was the address on date X?"
- **Cons:** More storage, more complex queries (filter by date), more complex ETL

### 5. SCD Type 3: Add New Column
- **Rule:** Add a "previous value" column to track one previous state
- **Use case:** When you only need the current and one previous value
- **Example:** `current_address` and `previous_address` columns
- **Pros:** Simple queries, less storage than Type 2
- **Cons:** Only one level of history, not scalable

### 6. SCD Type 4: History Table (Mini-Dimension)
- **Rule:** Keep current dimension small, move history to separate table
- **Use case:** Very large dimensions with frequent changes (e.g., customer with 100 attributes)
- **Implementation:** Current dimension table + history table with all versions
- **Pros:** Fast queries on current data, history available when needed
- **Cons:** More complex, two tables to maintain

### 7. SCD Type 6: Hybrid (1 + 2 + 3)
- **Rule:** Type 1 for some attributes, Type 2 for others, Type 3 for others
- **Use case:** Different attributes have different history requirements
- **Example:** Customer name (Type 1, overwrite), address (Type 2, track history), email (Type 3, current + previous)
- **Implementation:** Most complex, but most flexible

### 8. Implementation in ETL
- **Type 1:** Simple `UPDATE`
- **Type 2:**
  1. Detect changed rows (hash comparison or column-by-column)
  2. Update `expiration_date` and `is_current` on old row
  3. Insert new row with `effective_date` = today, `expiration_date` = NULL, `is_current` = Y
- **Tools:** dbt has SCD Type 2 macros, Airflow can orchestrate

## Hands-On Exercise

Implement SCD Type 2 for `dim_country` in your WDI project:
1. What country attributes might change? (name, region, income_group)
2. Add `effective_date`, `expiration_date`, `is_current` columns
3. Write the ETL logic to handle a country changing its income_group
4. Write a query that retrieves the income_group as of a specific date

## Why This Matters for Your WDI Project

Countries change names (e.g., Swaziland → Eswatini), regions get redefined, indicators get renamed. If you overwrite in place (Type 1), historical analysis becomes wrong. If you track history (Type 2), you can analyze "GDP growth in what was then called Swaziland."

## Next File
→ `08-Data-Vault-Modeling-Overview.md`
