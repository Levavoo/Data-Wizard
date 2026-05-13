# Strict Mode Policy

## Purpose

This document defines opt-in strict-mode behavior for CSV pipeline runs.

---

## Default Mode

Default mode is non-strict.

Behavior:

```text
issues are reported
CSV export still runs
pipeline status may be completed_with_warnings
CLI exits 0 when execution succeeds
```

---

## Strict Mode

Strict mode is enabled explicitly with:

```text
--strict
```

or through:

```python
run_csv_pipeline(..., strict_mode=True)
```

---

## Initial Failure Conditions

Strict mode fails policy when either condition is true:

```text
validation_report.failed_count > 0
quarantine_candidates.summary.error > 0
```

---

## Warning-Only Behavior

Warning-only quarantine candidates do not fail strict mode currently.

Reason:

```text
warnings require review but may not represent hard migration failure
```

---

## Strict Policy Failure

Strict policy failure means:

```text
processing completed
reports were generated
CSV export still ran
serious diagnostics were found
CLI exits 2
```

---

## Design Rule

Strict mode must not remove rows or mutate values.

Strict mode reports policy failure only.

---

## Future Policy Modes

Possible future modes:

```text
validation_errors
quarantine_error_candidates
any_quarantine_candidate
any_warning_or_error
custom policy config
```
