# test_schema_inference.py

## Purpose

Tests the schema inference module.

This verifies that schema metadata is inferred correctly from table values.

Architecture:

```text
Table
→ Schema Inference
→ Enriched Schema Metadata
```

---

# Tested File

```text
data_processor/inference/schema_inference.py
```

---

# Current Test Coverage

## `test_infer_column_metadata_counts`

Verifies:

- total row count
- missing value count

Example:

```text
4 rows
1 missing value
```

---

## `test_infer_column_metadata_unique_count`

Verifies unique non-null values are counted correctly.

Example:

```text
Germany
France
Germany
None
```

Expected unique count:

```text
2
```

---

## `test_infer_column_metadata_nullable`

Verifies nullable detection.

Rule:

```text
missing_count > 0
→ nullable = True
```

---

## `test_infer_column_metadata_sample_values`

Verifies representative sample values are collected.

Rules:

- unique
- ordered
- size-limited

---

## `test_infer_schema_metadata_updates_columns`

Verifies schema columns are enriched with metadata.

Checks:

```text
metadata updates
nullable updates
```

---

## `test_sample_values_are_unique`

Verifies duplicate sample values are not repeated.

Example:

```text
Germany
Germany
France
```

Expected samples:

```text
Germany
France
```

---

# Important Design Rule

Schema inference enriches metadata only.

It does NOT:

- clean values
- validate business rules
- transform data
- enforce constraints

---

# Why Schema Metadata Matters

Schema metadata supports:

- validation
- profiling
- reporting
- UI previews
- anomaly detection
- diagnostics

Without metadata, schemas only describe structure.

---

# Run Tests

```powershell
pytest tests\test_schema_inference.py
```

Expected result:

```text
6 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\inference\schema_inference.py `
    tests\test_schema_inference.py

black `
    data_processor\inference\schema_inference.py `
    tests\test_schema_inference.py

pytest tests\test_schema_inference.py
```

---

# Developer Notes

Schema inference should stay:

- deterministic
- lightweight
- explicit
- format-independent

Avoid expensive profiling too early.

---

# Future Improvements

Possible future additions:

- min/max statistics
- frequency distributions
- pattern detection
- cardinality metrics
- anomaly scoring
- schema drift detection
- profiling reports