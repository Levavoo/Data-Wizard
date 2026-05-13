# HTML Report Structure

## Purpose

This document defines the first static HTML diagnostic report structure.

---

## Report Title

```text
CSV Diagnostic Report — <table_name>
```

---

## Section Order

The first HTML report uses this section order:

```text
Summary
Pipeline Status
Quality Report
Validation Report
Quarantine Candidates
Row Classification
Type Diagnostics
Parse Diagnostics
Metadata
```

---

## Summary Section

Includes:

```text
table name
row count
column count
```

---

## Pipeline Status Section

Includes:

```text
status
strict mode
strict mode failed
error count
warning count
reasons
```

---

## Quality Report Section

Includes summary values from the existing quality report.

---

## Validation Report Section

Includes:

```text
total results
passed count
failed count
failures by column
failures by constraint
failed results
```

---

## Quarantine Candidates Section

Includes:

```text
candidate count
severity summary
candidate details
```

---

## Large/Nested Data Handling

Nested values are rendered inside `<pre>` blocks.

Long sections use `<details>` blocks where appropriate.

---

## Design Rule

The HTML report displays existing diagnostics only.

It must not change diagnostic meaning or shape.
