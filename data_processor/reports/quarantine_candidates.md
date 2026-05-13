# quarantine_candidates.py

## Purpose

`quarantine_candidates.py` builds row-level quarantine candidate diagnostics from existing report sections.

It belongs to the report layer.

Architecture:

```text
row classification
+ type diagnostics
+ validation report
→ quarantine candidate report
```

---

## Main Function

### `build_quarantine_candidates(table_rows, row_classification, type_diagnostics, validation_report)`

Builds a report with rows that should be reviewed as quarantine candidates.

Returned shape:

```python
{
    "candidate_count": 2,
    "summary": {
        "error": 1,
        "warning": 1,
        "info": 0
    },
    "candidates": [...]
}
```

---

## Candidate Shape

```python
{
    "row_index": 2,
    "severity": "error",
    "reason_count": 2,
    "reasons": [...],
    "row": {...}
}
```

---

## Reason Shape

```python
{
    "source": "validation_report",
    "code": "regex_pattern_failed",
    "severity": "error",
    "column": "email",
    "message": "Value does not match pattern.",
    "value": "invalid-email"
}
```

---

## Supported Sources

Current sources:

```text
row_classification.suspicious_rows
type_diagnostics.mixed_type_columns.invalid_values
validation_report.failed_results
```

---

## Severity Levels

Current severity levels:

```text
info
warning
error
```

Initial mapping:

```text
validation failure → error
mixed-type invalid value → warning
suspicious row classification → warning
```

---

## Design Rules

This module must not:

- mutate rows
- remove rows
- quarantine rows physically
- block export
- write files

It only produces report data.

---

## Future Work

Possible future additions:

- quarantine CSV export
- quarantine JSON export
- parse diagnostics as candidate source
- quality report missing-value candidate source
- strict/fail mode integration
