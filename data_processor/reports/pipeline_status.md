# pipeline_status.py

## Purpose

`pipeline_status.py` builds automation-friendly status information from a diagnostic bundle.

It belongs to the report/policy layer.

Architecture:

```text
Diagnostic Bundle
→ Pipeline Status
→ Optional CLI Exit Code
```

---

## Main Functions

### `build_pipeline_status(diagnostic_bundle, strict_mode=False)`

Builds a structured status dictionary.

Example:

```python
{
    "status": "failed_policy",
    "has_errors": True,
    "has_warnings": True,
    "error_count": 2,
    "warning_count": 1,
    "strict_mode": True,
    "strict_mode_failed": True,
    "reasons": [...]
}
```

---

### `exit_code_from_pipeline_status(pipeline_status)`

Converts pipeline status into a CLI exit code.

Current mapping:

```text
0 = successful execution
2 = strict policy failure
```

Execution errors are handled by the CLI as exit code `1`.

---

## Status Values

```text
success
completed_with_warnings
failed_policy
```

---

## Strict Mode Policy

Strict mode fails when either condition is true:

```text
validation_report.failed_count > 0
quarantine_candidates.summary.error > 0
```

Strict mode does not fail on warning-only candidates.

---

## Design Rules

This module must not:

- mutate rows
- remove rows
- export files
- parse CLI arguments
- raise policy failures as exceptions

It only builds status data.
