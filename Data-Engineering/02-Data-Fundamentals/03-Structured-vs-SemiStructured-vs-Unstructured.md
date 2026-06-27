# Structured vs Semi-Structured vs Unstructured Data

**Phase:** 2 (Data Core)  
**Prerequisites:** `02-Data-Types-Formats-CSV-JSON-XML.md`  
**When to Skip:** If you can explain why a JSON API response needs a different storage approach than a relational table  
**Projects This Enables:** Choosing the right storage system for each data type

## What to Cover

### 1. Structured Data
- **Definition:** Fixed schema, tabular, predefined types
- **Examples:** Relational databases, Excel spreadsheets, CSV with known schema
- **Storage:** SQL databases, data warehouses
- **Querying:** SQL (declarative, optimized)
- **Pros:** Easy to query, ACID transactions, strong typing
- **Cons:** Schema evolution is hard, doesn't handle nested data well

### 2. Semi-Structured Data
- **Definition:** Self-describing, no fixed schema, but has some structure
- **Examples:** JSON, XML, NoSQL databases, log files
- **Storage:** Document stores (MongoDB), data lakes, JSON columns in PostgreSQL
- **Querying:** JSONPath, MongoDB query language, Spark SQL with `from_json()`
- **Pros:** Flexible schema, handles nested data, easy to evolve
- **Cons:** No enforced types, harder to optimize queries

### 3. Unstructured Data
- **Definition:** No predefined structure
- **Examples:** Images, videos, audio, PDFs, free text, emails
- **Storage:** Object storage (S3), blob storage, data lakes
- **Processing:** Requires ML/NLP for extraction (OCR, speech-to-text, NLP)
- **In Data Engineering:** Often processed to extract structured metadata

### 4. The Spectrum
```
Structured ←————————————————→ Unstructured
SQL DB      JSON/NoSQL      Text/Images/Videos
|           |                |
Schema      Schema-on-read   No schema
enforced    (flexible)       (extract structure)
```

### 5. Data Engineering Implications
- **ETL for structured:** Schema validation, type casting, constraint checking
- **ETL for semi-structured:** Schema inference, flattening, normalization
- **ETL for unstructured:** Metadata extraction, content tagging, indexing

## Hands-On Exercise

Take your WDI dataset and classify each component:
- Is the raw CSV structured or semi-structured? (Structured, but with categorical dimensions)
- What about the SDMX metadata? (Semi-structured XML/JSON)
- How would you store survey responses with open-ended answers? (Mixed: structured demographics + unstructured text)

## Why This Matters

Your storage choice (SQL vs NoSQL vs Data Lake) depends on data structure. You cannot design a pipeline without knowing what you're storing.

## Next File
→ `04-ETL-vs-ELT-Architecture.md`
