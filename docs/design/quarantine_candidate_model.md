# Quarantine Candidate Model

## Purpose

This document defines the report model for quarantine candidates.

A quarantine candidate is a row that should be reviewed because one or more diagnostics marked it as suspicious or invalid.

---

## Report Shape

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
    "reason_count": 3,
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

## Row Index Semantics

`row_index` is zero-based and refers to the processed table row index.

It does not include the CSV header row.

---

## Severity

Allowed severity values:

```text
info
warning
error
```

A candidate inherits the highest severity from its reasons.

---

## Design Rules

Quarantine candidates are report-only.

They must not:

- remove rows
- mutate values
- block export
- write separate quarantine files

---

## Future Work

Future reports may add:

```text
source_row_number
quarantine_action
review_status
review_notes
```
