# Object-Oriented Programming Basics

**Phase:** 1 (Foundation) — **Optional Deep Dive**  
**Prerequisites:** `05-Python-Core-for-Data-Engineering.md`  
**When to Skip:** If you already understand classes, inheritance, and can design a simple class hierarchy  
**Projects This Enables:** Building reusable ETL components, understanding Airflow operators

## What to Cover

### 1. OOP Principles
- Encapsulation (private attributes, getters/setters)
- Inheritance (is-a relationships)
- Polymorphism (duck typing in Python)
- Abstraction (abstract base classes with `abc` module)

### 2. Design Patterns (Practical Ones)
- **Factory Pattern:** Creating different database connectors
- **Strategy Pattern:** Swapping ETL strategies (batch vs streaming)
- **Observer Pattern:** Event-driven pipelines
- **Singleton:** Configuration managers (use sparingly)
- **Template Method:** ETL pipeline skeleton with customizable steps

### 3. Python-Specific OOP
- Dataclasses (`@dataclass`) — use these for data models
- `attrs` library (advanced dataclasses)
- NamedTuples for lightweight structures
- Enums for pipeline states

### 4. Data Engineering Application
- Designing a `Pipeline` base class with `extract()`, `transform()`, `load()` methods
- Building a `Connector` hierarchy (PostgresConnector, S3Connector, etc.)
- Creating `DataQualityCheck` classes with different validation strategies

## Hands-On Exercise

Design a class hierarchy for your WDI ETL pipeline:
- `BaseExtractor` with subclasses `CSVExtractor`, `APIExtractor`
- `BaseTransformer` with `CleanTransformer`, `AggregateTransformer`
- `BaseLoader` with `PostgresLoader`, `S3Loader`
- Each has a `.run()` method and `.validate()` method

## Why This Matters for Data Engineering

- Airflow operators are classes (you'll subclass `BaseOperator`)
- Spark transformations are method chains on DataFrame objects
- dbt models are Jinja-templated SQL, but the framework is Python OOP
- Building reusable, testable pipeline components

## Next File
→ `02-Data-Fundamentals/01-What-is-Data-Engineering.md`
