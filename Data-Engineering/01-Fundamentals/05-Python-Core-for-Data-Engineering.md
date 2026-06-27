# Python Core for Data Engineering

**Phase:** 1 (Foundation)  
**Prerequisites:** `02-Linux-Bash-Essentials.md`  
**When to Skip:** Only if you can write decorators, context managers, and generators without reference  
**Projects This Enables:** Every Python-based tool (pandas, Airflow, Spark, dbt)

## What to Cover

### 1. Python Fundamentals (Review Quickly)
- Data types: lists, dicts, sets, tuples, strings
- Comprehensions (list, dict, set)
- `map`, `filter`, `reduce` (but prefer comprehensions)
- `enumerate`, `zip`, `iterators`
- Exception handling (`try/except/finally`, custom exceptions)

### 2. Functions Deep Dive
- `*args`, `**kwargs`
- First-class functions and higher-order functions
- Decorators (timing, logging, retry logic)
- Closures and scope (LEGB rule)

### 3. Object-Oriented Programming
- Classes, inheritance, polymorphism
- `__init__`, `__str__`, `__repr__`, `__len__`
- `@property`, `@staticmethod`, `@classmethod`
- Magic/dunder methods for protocol implementation
- Composition over inheritance

### 4. File I/O and Context Managers
- `with open()` and custom context managers (`__enter__`, `__exit__`)
- `pathlib` (modern path handling, prefer over `os.path`)
- Reading large files (generators, `yield`)
- CSV and JSON parsing (`csv` module, `json` module)

### 5. Modules and Packages
- `import` system, `__init__.py`, `__all__`
- Virtual environments (`venv`, `conda`, `uv` — use `uv`)
- `pip` vs `poetry` vs `uv` (use `uv` for this course)
- Writing `setup.py` / `pyproject.toml`

### 6. Testing Basics
- `pytest` fundamentals
- `assert`, fixtures, parametrization
- Mocking with `unittest.mock`
- Code coverage (`pytest-cov`)

### 7. Python for Data Engineering Specifics
- `logging` module (not `print()` in production)
- `configparser` and `dotenv` for configuration
- `pydantic` for data validation (learn in Phase 3)
- `concurrent.futures` for parallel processing (preview of Spark)
- Type hints (`typing` module, `mypy`)

## Hands-On Exercise

Build a Python module that:
1. Reads a config file (JSON or YAML)
2. Validates it with type hints
3. Downloads a file from a URL
4. Processes it in chunks (generator)
5. Logs progress to a file
6. Has pytest tests for each function

## Why This Matters for Data Engineering

- Airflow is Python
- PySpark is Python
- dbt is Python under the hood
- Your ETL scripts are Python
- Pandas is Python
- boto3 (AWS SDK) is Python

## Next File
→ `02-Data-Fundamentals/01-What-is-Data-Engineering.md`
