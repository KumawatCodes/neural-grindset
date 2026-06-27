# Advanced SQL: Window Functions & CTEs

**Phase:** 2 (Data Core)  
**Prerequisites:** `02-PostgreSQL-Deep-Dive.md`  
**When to Skip:** Only if you can write complex window functions with frames and recursive CTEs without reference  
**Projects This Enables:** Analytics queries on your WDI data, time-series analysis

## What to Cover

### 1. Common Table Expressions (CTEs)
- Syntax: `WITH cte_name AS (SELECT ...)`
- Multiple CTEs in one query
- Recursive CTEs for hierarchical data (org charts, bill of materials)
- CTEs vs subqueries (readability, optimization differences)
- Materialized CTEs (PostgreSQL 12+)

### 2. Window Functions
- Syntax: `function() OVER (PARTITION BY ... ORDER BY ... frame)`
- **Ranking:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`
- **Offset:** `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, `NTH_VALUE()`
- **Aggregate window:** `SUM()`, `AVG()`, `COUNT()` as running totals
- **Frame specification:** `ROWS`, `RANGE`, `GROUPS`, `UNBOUNDED PRECEDING`, `CURRENT ROW`

### 3. Practical Window Function Patterns
- Running totals and moving averages
- Year-over-year growth (`LAG(value, 12)` for monthly data)
- Top-N per group (`ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC)`)
- Gaps and islands (finding consecutive sequences)
- Sessionization (grouping events into sessions)

### 4. CTE + Window Function Combinations
- Complex analytics that would be impossible with simple GROUP BY
- Self-referencing recursive CTEs for pathfinding
- Multi-step transformations with intermediate results

## Hands-On Exercise

Using your WDI data (or sample data):
1. Calculate the running total of GDP per country over time
2. Find the top 3 indicators by value for each country-year
3. Calculate year-over-year GDP growth percentage using `LAG()`
4. Identify countries with declining life expectancy for 3+ consecutive years
5. Rank countries by GDP per capita within each region using `DENSE_RANK()`

## Why This Matters for Data Engineering

Window functions are the most powerful SQL feature for analytics. Your WDI business problem (GDP vs life expectancy over 20 years) requires:
- Time-series analysis (`LAG`/`LEAD`)
- Ranking countries (`RANK`/`DENSE_RANK`)
- Running totals (`SUM() OVER`)
- These are all window functions.

## Next File
→ `04-Indexing-Query-Optimization.md`
