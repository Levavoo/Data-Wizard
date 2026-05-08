# row_profile.py

## Purpose

`row_profile.py` generates row-level quality statistics.

This module belongs to the analysis layer.

Architecture:

```text
Table
→ Row Profiler
→ Row Quality Profiles
```

---

# Why Row Profiling Matters

Column profiling shows problems by field.

Row profiling shows problems by record.

This is important for:

- invalid-row quarantine
- migration diagnostics
- repair workflows
- anomaly detection
- row quality scoring
- audit reports

---

# Main Responsibilities

This module analyzes:

- missing values per row
- missing ratio per row
- empty rows
- duplicate row candidates
- non-null value count
- expected column count

---

# Main Functions

## `profile_all_rows(table)`

Profiles every row in a table.

Returns:

```python
[
    row_profile,
    row_profile,
    row_profile,
]
```

---

## `profile_row(table, row, row_index, duplicate_signatures=None)`

Profiles one row.

Returned fields:

| Field | Meaning |
|---|---|
| `row_index` | Zero-based row position |
| `column_count` | Expected number of columns |
| `missing_count` | Number of missing values |
| `missing_ratio` | Ratio of missing values |
| `non_null_count` | Number of non-null values |
| `empty_row` | Whether all expected values are missing |
| `duplicate_candidate` | Whether row appears duplicated |

---

## `count_missing_values(row, column_names)`

Counts values that are missing according to schema columns.

A value is considered missing when:

```python
value is None
```

This assumes null cleaning has already run.

---

## `find_duplicate_signatures(table)`

Finds row signatures that appear more than once.

Used to mark duplicate candidates.

---

## `create_row_signature(row)`

Creates a deterministic signature for a row.

Current signature format:

```python
tuple(sorted(row.items()))
```

This allows rows with the same key/value pairs to be detected as duplicates.

---

## `calculate_ratio(numerator, denominator)`

Safely calculates ratios.

If denominator is zero:

```python
0.0
```

is returned.

---

# Example Profile

```python
{
    "row_index": 3,
    "column_count": 5,
    "missing_count": 2,
    "missing_ratio": 0.4,
    "non_null_count": 3,
    "empty_row": False,
    "duplicate_candidate": False,
}
```

---

# Important Design Rule

Row profilers only analyze.

They must never:

- modify row values
- delete rows
- quarantine rows directly
- clean values
- validate business rules
- export data

Later modules may use row profiles to decide what action to take.

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
→ Row Profiling
→ Quality Reporting
→ Export
```

---

# Why This Helps Future Formats

All future formats become:

```text
Table
```

Therefore row profiling automatically works for:

- CSV
- Excel
- JSON
- SQL
- APIs
- Parquet
- Arrow

without format-specific logic.

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

- severity scoring
- row anomaly detection
- row repair suggestions
- invalid type diagnostics
- constraint violation summaries
- foreign key validation
- semantic validation

---

# Future Improvements

Possible future additions:

- row quality score
- quarantine candidate detection
- duplicate group IDs
- anomaly detection
- repair suggestions
- row-level validation errors
- row-level lineage
- audit logs