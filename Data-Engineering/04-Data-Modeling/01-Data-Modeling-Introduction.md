# Data Modeling Introduction

**Phase:** 2 (Data Core)  
**Prerequisites:** `03-Databases-and-SQL/06-When-SQL-vs-NoSQL.md`  
**When to Skip:** Never — this is the foundation of all database design  
**Projects This Enables:** Your WDI star schema, all future warehouse design

## What to Cover

### 1. What is Data Modeling?
- The process of defining how data is stored, structured, and related
- Three levels: Conceptual → Logical → Physical
- **Conceptual:** Entities and relationships (business view)
- **Logical:** Attributes, keys, normalization (analyst view)
- **Physical:** Tables, indexes, data types, partitions (engineer view)

### 2. Why Data Modeling Matters
- **Performance:** Bad models = slow queries, expensive joins
- **Scalability:** Bad models = can't partition, can't shard
- **Maintainability:** Bad models = schema changes break everything
- **Accuracy:** Bad models = wrong aggregations, double counting

### 3. Data Modeling Approaches
- **Bottom-up:** Start from existing data sources, normalize
- **Top-down:** Start from business requirements, design schema
- **Hybrid:** Most real-world projects (requirements + source analysis)

### 4. Key Concepts
- **Entities:** Real-world objects (Customer, Order, Product)
- **Attributes:** Properties of entities (name, price, date)
- **Relationships:** One-to-one, one-to-many, many-to-many
- **Keys:** Primary key (unique identifier), foreign key (relationship), natural key vs surrogate key
- **Cardinality:** How many instances relate to how many

### 5. The Data Modeling Process
1. Gather requirements (what questions need answers?)
2. Identify entities and relationships
3. Define attributes and keys
4. Normalize (for OLTP) or denormalize (for OLAP)
5. Validate with sample queries
6. Iterate

## Hands-On Exercise

Model a simple library system:
- Entities: Book, Author, Member, Loan
- Relationships: Author writes Book, Member borrows Book
- Identify keys, cardinality, attributes
- Draw an ER diagram

## Why This Matters for Your WDI Project

Your WDI dataset has implicit entities:
- **Country** (entity) → `dim_country` (dimension table)
- **Indicator** (entity) → `dim_indicator` (dimension table)
- **Observation** (event) → `fact_wdi_data` (fact table)
- Without modeling, you dump everything in one flat table and can't analyze efficiently.

## Next File
→ `02-ER-Diagrams-and-Relationships.md`
