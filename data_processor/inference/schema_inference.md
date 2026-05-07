# schema_inference.py

## Purpose

`schema_inference.py` enriches schema columns with metadata inferred from table data.

This module belongs to the inference layer.

Architecture:

```text
Table
→ Schema Inference
→ Enriched Schema Metadata
```

---

# Why Schema Metadata Matters

Basic schema definitions only describe structure.

Example:

```text
column name
column type
```

But real data quality workflows also need:

```text
missing values
uniqueness
sample values
nullable detection
```

This metadata supports:

- validation
- reporting
- profiling
- UI previews
- anomaly detection
- schema comparison

---

# Main Functions

## `infer_schema_metadata(table)`

Infers metadata for all schema columns.

Behavior:

```text
mutates schema columns in place
```

Flow:

```text
Table
→ iterate columns
→ inspect values
→ compute metadata
→ update schema columns
```

---

## `infer_column_metadata(table, column)`

Infers metadata for one column.

Returns metadata dictionary.

---

## `_collect_sample_values(values, sample_size)`

Collects unique sample values.

Purpose:

- schema previews
- reports
- diagnostics
- debugging

---

# Inferred Metadata

Current metadata fields:

| Field | Description |
|---|---|
| `total_count` | Total row count |
| `missing_count` | Number of missing values |
| `unique_count` | Number of unique non-null values |
| `sample_values` | Small representative sample |
| `nullable` | Whether null values exist |

---

# Example

## Input Values

```python
[
    "Germany",
    "France",
    None,
    "Germany"
]
```

---

## Inferred Metadata

```python
{
    "total_count": 4,
    "missing_count": 1,
    "unique_count": 2,
    "sample_values": [
        "Germany",
        "France"
    ],
    "nullable": True
}
```

---

# Sample Values

Sample values are:

- unique
- ordered
- limited in size

Purpose:

```text
preview representative values
without storing entire columns
```

Default sample size:

```python
5
```

---

# Nullability Detection

Rule:

```text
missing_count > 0
→ nullable = True
```

This updates:

```python
column.nullable
```

inside the schema.

---

# Example Usage

```python
from data_processor.inference.schema_inference import (
    infer_schema_metadata,
)

infer_schema_metadata(table)

for column in table.schema.columns:
    print(column.metadata)
```

---

# Pipeline Position

Recommended pipeline order:

```text
Parsing
→ Cleaning
→ Type Inference
→ Schema Inference
→ Validation
→ Transformation
→ Export
```

---

# Important Design Principle

Schema inference enriches metadata.

It should NOT:

- clean values
- validate business rules
- transform rows
- enforce constraints

Those belong to later stages.

---

# Developer Notes

This module should remain:

- deterministic
- explicit
- format-independent
- lightweight
- easy to test

Avoid expensive profiling too early.

---

# Current Limitations

Current implementation does not support:

```text
min/max statistics
frequency distributions
histograms
pattern analysis
cardinality ratios
entropy analysis
anomaly scoring
cross-column analysis
```

---

# Future Improvements

Possible future additions:

- min/max statistics
- frequency analysis
- duplicate ratios
- cardinality metrics
- pattern detection
- value distributions
- schema drift detection
- profiling reports
- confidence scoring
```