# Constraint Validation Policy

## Purpose

This document defines what constraint validation should and should not do inside the CSV pipeline.

---

## Decision

Constraint validation is report-only for now.

Current policy:

```text
constraints report violations only
constraints do not clean values
constraints do not cast values
constraints do not quarantine rows
constraints do not block export by default
```

---

## Reason

Validation should make issues visible without changing data unexpectedly.

Blocking export or quarantining rows requires explicit policy and user-facing controls.

---

## Current Behavior

When constraints are provided:

```text
pipeline validates after cleaning and casting
validation results are returned
validation report is included in diagnostic bundle
clean CSV export still runs
```

---

## Future Options

Possible future policy modes:

```text
warn_only
fail_on_validation_error
quarantine_invalid_rows
exclude_invalid_rows_from_export
```

These are not implemented yet.

---

## Architecture Rule

Validators validate only.

They must not mutate rows, clean values, cast values, export files, or quarantine records.
