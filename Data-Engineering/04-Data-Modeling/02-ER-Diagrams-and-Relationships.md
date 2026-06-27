# ER Diagrams and Relationships

**Phase:** 2 (Data Core)  
**Prerequisites:** `01-Data-Modeling-Introduction.md`  
**When to Skip:** Only if you can draw ER diagrams and identify all relationship types instinctively  
**Projects This Enables:** Visualizing your WDI schema, communicating with stakeholders

## What to Cover

### 1. Entity-Relationship Diagrams (ERDs)
- **Entities:** Rectangles (tables)
- **Attributes:** Ovals or listed inside rectangles
- **Relationships:** Diamonds or lines connecting entities
- **Cardinality notation:** Crow's foot, Chen notation, UML

### 2. Relationship Types
- **One-to-One (1:1):** One employee has one desk, one desk has one employee
- **One-to-Many (1:N):** One customer has many orders, one order has one customer
- **Many-to-Many (M:N):** One student takes many courses, one course has many students (requires junction table)

### 3. Cardinality Notation
```
Crow's Foot:
|o-----||  (One-to-One, optional on left)
||-----|<  (One-to-Many, mandatory on both)
|>-----|<  (Many-to-Many)

UML:
1..1  (exactly one)
0..*  (zero or many)
1..*  (one or many)
```

### 4. Identifying vs Non-Identifying Relationships
- **Identifying:** Child table's primary key includes parent's PK (strong dependency)
- **Non-Identifying:** Child has its own PK, parent's PK is just a FK (weaker dependency)
- In data warehousing: mostly non-identifying (surrogate keys)

### 5. Weak Entities
- Entities that can't exist without another entity (Order Line without Order)
- Identified by partial key + parent's key
- In data warehousing: often merged into fact tables

### 6. Tools for ER Diagrams
- dbdiagram.io (text-based, free)
- draw.io / diagrams.net (visual, free)
- Lucidchart (paid, collaborative)
- pgAdmin (for PostgreSQL, auto-generates from schema)
- dbt docs (auto-generates from SQL models)

## Hands-On Exercise

Draw an ER diagram for your WDI star schema:
- Entities: Country, Indicator, Date, Sex, Age, Urbanisation, WDI_Data
- Relationships: Which are 1:N? Which are M:N?
- Identify primary keys and foreign keys
- Use dbdiagram.io to create it with code

## Why This Matters

You can't build what you can't visualize. ER diagrams are the contract between business requirements and implementation. Your WDI schema needs a diagram to communicate with your teammate.

## Next File
→ `03-Normalization-1NF-2NF-3NF-BCNF.md`
