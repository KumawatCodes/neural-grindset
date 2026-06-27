# Normalization: 1NF, 2NF, 3NF, BCNF

**Phase:** 2 (Data Core)  
**Prerequisites:** `02-ER-Diagrams-and-Relationships.md`  
**When to Skip:** Only if you can normalize any table to 3NF and explain why BCNF matters  
**Projects This Enables:** Designing OLTP databases, understanding why data warehouses denormalize

## What to Cover

### 1. Why Normalize?
- **Eliminate redundancy:** Store each fact once
- **Prevent anomalies:** Update, insert, delete anomalies
- **Ensure integrity:** Data consistency across the database
- **Trade-off:** More joins, more complex queries

### 2. First Normal Form (1NF)
- **Rule:** Atomic values (no repeating groups, no multi-valued attributes)
- **Example violation:** `phone_numbers: "555-1234, 555-5678"` → Split into separate rows or table
- **Fix:** One value per cell, one row per entity instance

### 3. Second Normal Form (2NF)
- **Rule:** 1NF + no partial dependencies (non-key attributes depend on entire PK, not part of it)
- **Applies to:** Composite primary keys only
- **Example violation:** Order table with (OrderID, ProductID) as PK, but CustomerName depends only on OrderID
- **Fix:** Move CustomerName to Order table, keep only Product-specific attributes in OrderDetail

### 4. Third Normal Form (3NF)
- **Rule:** 2NF + no transitive dependencies (non-key attributes depend only on PK, not on other non-key attributes)
- **Example violation:** Employee table has DepartmentName, but DepartmentName depends on DepartmentID (not EmployeeID)
- **Fix:** Create Department table, reference it with DepartmentID FK

### 5. Boyce-Codd Normal Form (BCNF)
- **Rule:** Every determinant is a candidate key (stricter than 3NF)
- **Example violation:** Student(StudentID, Subject, Professor) where Professor teaches only one Subject
- **Fix:** Split into Student_Professor(StudentID, Professor) and Professor_Subject(Professor, Subject)
- **When it matters:** Complex overlapping candidate keys

### 6. Normalization Summary
```
1NF: No repeating groups, atomic values
2NF: No partial dependencies (full PK dependency)
3NF: No transitive dependencies (only PK dependency)
BCNF: Every determinant is a candidate key
```

### 7. When to STOP Normalizing
- **Data warehouses:** Stop at 3NF or denormalize further (star schema)
- **Read-heavy systems:** Denormalize for query performance
- **Write-heavy OLTP:** Normalize to 3NF/BCNF
- **The rule:** Normalize until it hurts, denormalize until it works

## Hands-On Exercise

Take this unnormalized table and normalize to 3NF:
```
Order(OrderID, CustomerName, CustomerAddress, ProductName, ProductPrice, Quantity, OrderDate)
```

1. Identify repeating groups (1NF violation)
2. Identify partial dependencies (2NF violation)
3. Identify transitive dependencies (3NF violation)
4. Draw the final 3NF schema

## Why This Matters for Data Engineering

OLTP systems (your app database) need normalization. Data warehouses (your analytics database) need denormalization. You must understand both to choose correctly. Your WDI project is analytics → star schema (denormalized).

## Next File
→ `04-Denormalization-for-Analytics.md`
