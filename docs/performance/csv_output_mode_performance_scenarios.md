# CSV Output Mode Performance Scenarios

## Purpose

This document defines output modes that should be compared for CSV pipeline performance.

---

## Scenario List

Recommended scenarios:

```text
clean_only
json_report
html_report
quarantine_exports
full_outputs
```

---

## Scenario Definitions

### `clean_only`

Outputs:

```text
clean CSV
```

Purpose:

```text
baseline processing and export cost
```

---

### `json_report`

Outputs:

```text
clean CSV
JSON diagnostic report
```

Purpose:

```text
measure diagnostic JSON export cost
```

---

### `html_report`

Outputs:

```text
clean CSV
HTML diagnostic report
```

Purpose:

```text
measure HTML rendering/export cost
```

---

### `quarantine_exports`

Outputs:

```text
clean CSV
quarantine candidate JSON
quarantine rows CSV
accepted rows CSV
```

Purpose:

```text
measure quarantine candidate and row split export cost
```

---

### `full_outputs`

Outputs:

```text
clean CSV
JSON diagnostic report
HTML diagnostic report
quarantine candidate JSON
quarantine rows CSV
accepted rows CSV
```

Purpose:

```text
measure maximum current output cost
```

---

## Interpretation Rule

Compare each scenario with the same:

```text
row count
fixture settings
Python version
machine
branch
```

---

## Artifact Policy

Generated output comparison files should not be committed by default.

Typical generated files:

```text
data/performance/output_modes/*.csv
data/performance/output_modes/*.json
data/performance/output_modes/*.html
```
