# column_profile.py

## Purpose

`column_profile.py` generates detailed statistics for dataset columns.

This module belongs to the analysis layer.

Architecture:

```text
Table
→ Column Profiler
→ Column Statistics
```

---

# Why Column Profiling Matters

Column profiling helps:

- understand data quality
- detect anomalies
- detect missing data
- identify candidate keys
- support validation
- support automated cleaning
- support future UI/reporting systems

---

# Main Responsibilities

This module analyzes:

- missing values
- unique values
- common values
- sample values
- numeric ranges
- inferred types

---

# Main Functions

## `profile_all_columns(table)`

Profiles all schema columns.

Returns:

```python
{
    "column_name": profile_data
}
```

---

## `profile_column(table, column)`

Profiles one column.

Generated statistics:

| Statistic | Meaning |
|---|---|
| `total_count` | Total row count |
| `missing_count` | Missing value count |
| `missing_ratio` | Missing value percentage |
| `unique_count` | Number of unique values |
| `unique_ratio` | Unique value percentage |
| `sample_values` | Example values |
| `most_common_values` | Most frequent values |
| `min_value` | Minimum numeric value |
| `max_value` | Maximum numeric value |
| `inferred_type` | Current inferred logical type |

---

# Example Profile

```python
{
    "column_name": "country",
    "inferred_type": "string",
    "total_count": 100,
    "missing_count": 5,
    "missing_ratio": 0.05,
    "unique_count": 3,
    "unique_ratio": 0.03,
    "sample_values": [
        "Germany",
        "France",
        "Italy"
    ],
    "most_common_values": [
        ("Germany", 80),
        ("France", 15),
    ],
    "min_value": None,
    "max_value": None,
}
```

---

# Numeric Value Handling

Only real numeric values are included in:

```python
min_value
max_value
```

Booleans are excluded intentionally.

Example:

```python
True
False
```

should not become:

```python
1
0
```

during profiling.

---

# Important Design Rule

Profilers only analyze.

They should never:

- modify values
- clean rows
- infer schema
- export data
- validate constraints

This keeps analysis deterministic and side-effect free.

---

# Pipeline Position

Recommended workflow:

```text
Parse
→ Clean
→ Infer Types
→ Type Casting
→ Schema Metadata
→ Column Profiling
→ Quality Reporting
→ Export
```

---

# Why This Helps Future Formats

All future adapters convert data into:

```text
Table
```

Therefore this module works for:

- CSV
- Excel
- JSON
- SQL
- APIs
- Parquet
- Arrow

without modification.

---

# Developer Notes

This module should remain:

- format-independent
- deterministic
- side-effect free
- lightweight
- easy to extend

---

# Current Limitations

Current implementation does not yet support:

- histograms
- quantiles
- standard deviation
- text length analysis
- regex pattern analysis
- outlier scoring
- semantic detection
- cardinality classification

---

# Future Improvements

Possible future additions:

- numeric distributions
- percentile analysis
- category entropy
- text statistics
- outlier detection
- regex profiling
- semantic profiling
- candidate key detection
- relationship profiling
- ML-assisted profiling