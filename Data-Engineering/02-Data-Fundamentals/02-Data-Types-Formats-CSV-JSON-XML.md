# Data Types & Formats: CSV, JSON, XML

**Phase:** 2 (Data Core)  
**Prerequisites:** `01-What-is-Data-Engineering.md`  
**When to Skip:** Only if you can explain CSV escaping, JSON schema validation, and XML parsing trade-offs  
**Projects This Enables:** Understanding your raw data inputs, parsing any source format

## What to Cover

### 1. CSV (Comma-Separated Values)
- Structure: headers, rows, delimiters (comma, tab, pipe)
- **The escaping problem:** commas in fields, quotes, newlines
- `csv` module in Python vs `pandas.read_csv()`
- Chunked reading for large files (`chunksize` parameter)
- Encoding issues (UTF-8, Latin-1, BOM)
- CSV variants: TSV, PSV (pipe-separated)

### 2. JSON (JavaScript Object Notation)
- Structure: objects `{}`, arrays `[]`, key-value pairs
- JSON Lines (JSONL) for streaming data
- Schema validation with JSON Schema
- Nested data flattening (crucial for data warehouses)
- `json` module, `jsonlines`, `pandas.json_normalize()`
- Streaming parsers (`ijson`) for large files

### 3. XML (eXtensible Markup Language)
- Structure: elements, attributes, namespaces
- When you'll see it: legacy systems, SOAP APIs, configuration files
- Parsing: `xml.etree.ElementTree`, `lxml`
- Converting XML to tabular format (the hard part)
- XPath for data extraction

### 4. Other Formats (Preview)
- **Avro:** Row-based, schema-in-header, good for Kafka
- **Parquet:** Columnar, compressed, the data lake standard (covered in Phase 3)
- **ORC:** Columnar, Hive-optimized (covered in Phase 3)
- **Protocol Buffers:** Binary, schema-evolution (gRPC)

### 5. Format Selection Guide
| Format | When to Use | When NOT to Use |
|--------|-------------|-----------------|
| CSV | Quick exports, human-readable | Nested data, large scale |
| JSON | APIs, semi-structured data | Large batch analytics |
| Parquet | Data lake, analytics | Human-readable needed |
| Avro | Streaming, schema evolution | Ad-hoc querying |

## Hands-On Exercise

1. Download a CSV with embedded commas and quotes — parse it correctly
2. Take a nested JSON API response and flatten it to a CSV
3. Convert a small XML file to a pandas DataFrame
4. Compare file sizes: same data in CSV vs JSON vs Parquet

## Why This Matters for Data Engineering

Every pipeline starts with "what format is my source data?" Your WDI dataset is CSV (SDMX format). Understanding its structure determines how you parse it, chunk it, and model it.

## Next File
→ `03-Structured-vs-SemiStructured-vs-Unstructured.md`
