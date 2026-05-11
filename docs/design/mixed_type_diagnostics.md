# Mixed-Type Diagnostics

## Purpose

This document defines the diagnostic model for columns that mostly match one type but contain incompatible values.

---

## Problem

Strict type inference can classify a mostly numeric column as `string` when one incompatible value exists.

Example:

```text
100
250.75
unknown
300
400
```

Expected diagnostic interpretation:

```text
dominant_type = float
invalid value = row 2, unknown
```

---

## Diagnostic Shape

```python
{
    "column": "amount",
    "dominant_type": "float",
    "total_values": 5,
    "non_null_count": 5,
    "null_count": 0,
    "valid_count": 4,
    "invalid_count": 1,
    "candidate_counts": {
        "boolean": 0,
        "integer": 3,
        "float": 4,
        "datetime": 0,
        "date": 0
    },
    "invalid_values": [
        {
            "row_index": 2,
            "value": "unknown",
            "expected_type": "float"
        }
    ],
    "is_mixed_type": True
}
```

---

## Row Index Semantics

`row_index` is zero-based and refers to the table row index after parsing.

It does not include the header row.

---

## Dominant Type Threshold

Default threshold:

```text
0.8
```

A type must match at least 80% of non-null values to be considered dominant.

---

## Null Handling

Null values are excluded from dominant type calculation.

They are not invalid mixed-type values.

---

## Design Rule

Mixed-type diagnostics are report-only.

They must not:

- mutate values
- change schema inference
- cast valid values
- quarantine rows
- validate constraints
