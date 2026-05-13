# Quarantine Candidate Sources

## Purpose

This document defines which existing diagnostics can contribute quarantine candidate reasons.

---

## Initial Included Sources

Current included sources:

```text
row_classification.suspicious_rows
validation_report.failed_results
type_diagnostics.mixed_type_columns.invalid_values
```

---

## Row Classification Source

Suspicious row classifications become warning candidates.

Examples:

```text
summary_row
footer_row
comment_row
garbage_row
empty_row
```

Reason:

```text
These rows may not represent normal data records.
```

---

## Validation Report Source

Validation failures become error candidates.

Examples:

```text
required failed
unique failed
regex_pattern failed
allowed_values failed
min_value failed
max_value failed
```

Reason:

```text
These rows violate explicit user-defined constraints.
```

---

## Type Diagnostics Source

Mixed-type invalid values become warning candidates.

Example:

```text
amount column is mostly float, but row 5 contains unknown
```

Reason:

```text
The row may block reliable type handling for migration or analytics.
```

---

## Deferred Sources

Not included yet:

```text
quality_report missing values
quality_report duplicate rows
parse_diagnostics malformed rows
row_profiles high missing count
column_profiles high null columns
```

Reason:

```text
These sources need clearer severity policy before being promoted to quarantine candidates.
```

---

## Design Rule

Candidate source detection must preserve the original source name.

This keeps the report auditable.
