# CSV Report Interpretation Guide

## Purpose

This guide explains how to interpret the CSV diagnostic report and decide what to fix next.

The report is diagnostic-first. It does not automatically correct every issue.

---

## Recommended Review Order

Review report sections in this order:

```text
1. parse_diagnostics
2. row_classification
3. validation_report
4. type_diagnostics
5. quality_report
6. column_profiles
7. row_profiles
```

---

## 1. Parse Diagnostics

Use this section to check whether the file was read correctly.

Look for:

```text
short rows
extra fields
duplicate headers
empty headers
detected delimiter
detected encoding
```

Action:

```text
Fix structural CSV issues before trusting value-level diagnostics.
```

---

## 2. Row Classification

Use this section to find rows that may not be real data records.

Common classifications:

```text
summary_row
footer_row
comment_row
garbage_row
empty_row
```

Action:

```text
Review suspicious rows manually before importing into another system.
```

Current behavior:

```text
Rows are not removed automatically.
```

---

## 3. Validation Report

Use this section to find failed business or migration rules.

Examples:

```text
duplicate customer ID
invalid email
unsupported country
negative amount
missing required value
```

Action:

```text
Fix values that violate configured constraints.
```

Current behavior:

```text
Validation failures do not block CSV export by default.
```

---

## 4. Type Diagnostics

Use this section to identify columns that mostly look like one type but contain incompatible values.

Example:

```text
amount: 100, 250.75, unknown, 300
```

Action:

```text
Review invalid values in mostly numeric/date/boolean columns.
```

---

## 5. Quality Report

Use this section for general data quality issues.

Examples:

```text
missing values
duplicate rows
empty columns
high-null columns
```

Action:

```text
Decide whether missing or duplicate values are acceptable for your target system.
```

---

## 6. Column Profiles

Use this section to understand each column.

Look for:

```text
missing count
unique count
sample values
```

Action:

```text
Use column profiles to understand whether inferred structure matches your expectations.
```

---

## 7. Row Profiles

Use this section to review row-level quality.

Examples:

```text
rows with many missing values
duplicate candidate rows
```

Action:

```text
Review suspicious row-level patterns manually.
```

---

## Warning vs Serious Problem

### Usually serious

```text
parse errors
extra fields
invalid required IDs
duplicate primary/customer IDs
invalid emails for CRM import
unsupported enum/category values
```

### Usually warning/review

```text
missing optional values
summary/footer rows
mixed-type diagnostics
high-null columns
```

The final decision depends on your target migration system.

---

## Current Limitations

The report does not yet provide:

```text
HTML output
CSV issue export
automatic quarantine
automatic correction
strict fail mode
```

These are future workflow improvements.
