# Current Quarantine Candidate Behavior

## Purpose

This document records current quarantine candidate behavior before dedicated quarantine exports.

---

## Current Behavior

The pipeline builds quarantine candidates inside the diagnostic bundle.

Current section:

```text
quarantine_candidates
```

Current behavior:

```text
rows are flagged for review
candidate reasons are grouped by row index
candidate severity is reported
rows remain in the cleaned CSV
no separate quarantine file is written by default
```

---

## Candidate Sources

Current candidate sources:

```text
validation_report.failed_results
row_classification.suspicious_rows
type_diagnostics.mixed_type_columns.invalid_values
```

---

## Current Export Gap

Users can see quarantine candidates in JSON and HTML reports, but cannot yet easily extract:

```text
quarantine_candidates.json
quarantine_rows.csv
accepted_rows.csv
```

---

## Default Safety Policy

Default behavior must remain unchanged:

```text
normal cleaned CSV includes all rows
quarantine candidates are report-only by default
rows are not removed automatically
strict mode behavior is unchanged
```
