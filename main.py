#!/usr/bin/env python3
"""
Scaffolds a complete DBMS course notes vault (Obsidian-compatible).
Run: python generate_dbms_vault.py [target_dir]
Default target_dir = ./dbms-complete-course
"""

import os
import sys
from datetime import date

ROOT = sys.argv[1] if len(sys.argv) > 1 else "dbms-complete-course"
TODAY = date.today().isoformat()

# folder -> list of files (files ending in "/" are treated as subfolders with their own list)
VAULT = {
    "01_database_theory": [
        "01_introduction_to_dbms.md",
        "02_data_models.md",
        "03_er_model.md",
        "04_relational_model.md",
        "05_relational_algebra.md",
        "06_relational_calculus.md",
        "12_query_processing_optimization.md",
        "13_distributed_databases.md",
        "14_nosql_vs_sql.md",
    ],
    "01_database_theory/07_normalization": [
        "01_functional_dependencies.md",
        "02_normal_forms_1nf_2nf_3nf.md",
        "03_bcnf.md",
        "04_4nf_5nf.md",
        "05_lossless_join_decomposition.md",
    ],
    "01_database_theory/08_transactions": [
        "01_acid_properties.md",
        "02_transaction_states.md",
        "03_concurrent_executions.md",
        "04_schedules_serializability.md",
    ],
    "01_database_theory/09_concurrency_control": [
        "01_lock_based_protocols.md",
        "02_two_phase_locking.md",
        "03_timestamp_ordering.md",
        "04_optimistic_concurrency.md",
        "05_deadlock_handling.md",
    ],
    "01_database_theory/10_recovery_system": [
        "01_failure_classification.md",
        "02_log_based_recovery.md",
        "03_shadow_paging.md",
        "04_aries_algorithm.md",
    ],
    "01_database_theory/11_indexing_and_hashing": [
        "01_indexing_basics.md",
        "02_b_plus_tree.md",
        "03_hash_indexing.md",
        "04_bitmap_index.md",
    ],
    "02_sql_fundamentals": [
        "01_ddl.md",
        "02_dml.md",
        "03_dql_basic.md",
        "04_joins.md",
        "05_subqueries.md",
        "06_set_operations.md",
        "07_aggregation_and_grouping.md",
        "08_views.md",
        "09_window_functions.md",
        "10_ctes.md",
        "11_string_date_functions.md",
        "12_constraints.md",
        "13_indexes_in_sql.md",
    ],
    "03_postgresql_and_plpgsql": [
        "01_postgresql_architecture.md",
        "02_data_types.md",
        "03_plpgsql_basics.md",
        "04_variables_and_control_structures.md",
        "05_cursors.md",
        "06_stored_procedures_vs_functions.md",
        "07_triggers.md",
        "08_exception_handling.md",
        "09_transactions_in_postgresql.md",
        "10_indexes_in_postgresql.md",
        "11_partitioning.md",
        "12_json_jsonb_handling.md",
        "13_extensions_common.md",
        "14_performance_tuning_postgresql.md",
    ],
    "04_oracle_plsql": [
        "01_oracle_architecture.md",
        "02_plsql_basics.md",
        "03_variables_and_control_structures.md",
        "04_cursors_explicit_implicit.md",
        "05_procedures_and_functions.md",
        "06_packages.md",
        "07_triggers.md",
        "08_exception_handling.md",
        "09_collections_varray_nested_table.md",
        "10_bulk_collect_forall.md",
        "11_dynamic_sql.md",
        "12_transactions_in_oracle.md",
    ],
    "05_advanced_rdbms_topics": [
        "01_triggers_and_procedures_comparison.md",
        "02_dynamic_sql_across_platforms.md",
        "03_performance_tuning_and_explain.md",
        "04_database_security.md",
        "05_data_warehousing_intro.md",
        "06_replication_and_sharding.md",
        "07_cap_theorem.md",
    ],
    "06_interview_prep": [
        "01_sql_query_questions.md",
        "02_normalization_questions.md",
        "03_transaction_isolation_levels.md",
        "04_joins_vs_subqueries.md",
        "05_plsql_vs_plpgsql_differences.md",
        "06_common_scenarios.md",
        "07_postgresql_vs_oracle_vs_mysql.md",
        "08_real_world_query_optimization_cases.md",
        "09_behavioral_and_project_questions.md",
    ],
}

TEMPLATE = """---
title: "{title}"
tags: [dbms, {tag}]
status: todo
created: {date}
---

# {title}

## Summary


## Core Concepts


## Syntax / Examples

```sql

```

## Common Pitfalls


## Interview Questions

- 

## Related Notes

- [[]]
"""


def title_from_filename(fname: str) -> str:
    name = os.path.splitext(fname)[0]
    parts = name.split("_")
    if parts and parts[0].isdigit():
        parts = parts[1:]
    return " ".join(p.upper() if p.lower() in {"sql", "acid", "bcnf", "nosql", "cap", "ddl", "dml", "dql", "cte", "ctes", "json", "jsonb"} else p.capitalize() for p in parts)


def build():
    created = 0
    for folder, files in VAULT.items():
        full_folder = os.path.join(ROOT, folder)
        os.makedirs(full_folder, exist_ok=True)
        tag = folder.split("/")[0].split("_", 1)[1] if "_" in folder.split("/")[0] else folder
        for f in files:
            path = os.path.join(full_folder, f)
            if os.path.exists(path):
                continue
            title = title_from_filename(f)
            content = TEMPLATE.format(title=title, tag=tag, date=TODAY)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            created += 1
    return created


if __name__ == "__main__":
    n = build()
    print(f"Created {n} notes under ./{ROOT}")