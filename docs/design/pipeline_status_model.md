# Pipeline Status Model

## Purpose

This document defines the structured pipeline status returned by CSV pipeline execution.

---

## Status Shape

```python
{
    "status": "completed_with_warnings",
    "has_errors": True,
    "has_warnings": True,
    "error_count": 2,
    "warning_count": 1,
    "strict_mode": False,
    "strict_mode_failed": False,
    "reasons": [...]
}
```

---

## Status Values

```text
success
completed_with_warnings
failed_policy
```

---

## `success`

Used when no error or warning signals are present.

---

## `completed_with_warnings`

Used when processing succeeds but diagnostics contain warnings or errors in non-strict mode.

---

## `failed_policy`

Used when strict mode is enabled and serious policy failures are present.

This is not an execution failure.

---

## Reason Shape

```python
{
    "source": "validation_report",
    "severity": "error",
    "code": "validation_failures",
    "count": 2,
    "message": "Validation failures were reported."
}
```

---

## Design Rule

Pipeline status must not mutate data, remove rows, or block report generation.
