# CSV Diagnostic Report Guide

## Purpose

The CSV diagnostic report explains what happened during CSV processing.

It is designed to help users answer:

```text
Was the file parsed correctly?
What data quality issues exist?
Which rows or columns need review?
Which validation rules failed?
```

---

## Report Location

When running the CLI with `--report-path`, the report is written as JSON.

Example:

```powershell
python scripts\run_csv_pipeline.py `
    examples\csv\customer_migration_sample.csv `
    data\processed\customer_migration_clean.csv `
    --constraints-path examples\csv\customer_constraints.json `
    --report-path data\processed\customer_migration_report.json
```

---

## Top-Level Structure

Current top-level report sections:

```text
table_name
row_count
column_count
metadata
parse_diagnostics
quality_report
column_profiles
row_profiles
row_classification
type_diagnostics
validation_report
```

---

## `table_name`

Name of the processed table.

Usually derived from the input file name.

---

## `row_count`

Number of rows in the internal table after parsing.

Important:

```text
Suspicious rows are still counted because they are not removed automatically.
```

---

## `column_count`

Number of columns in the internal table after header normalization.

---

## `metadata`

General metadata attached to the table.

May include:

```text
source format
encoding
delimiter
parse diagnostics
```

---

## `parse_diagnostics`

Explains problems or observations during CSV parsing.

Examples:

```text
short rows
extra fields
duplicate headers
empty headers
detected delimiter
detected encoding
```

Use this section first when the file structure looks wrong.

---

## `quality_report`

Reports general data quality issues.

Examples:

```text
missing values
duplicate rows
empty columns
high-null columns
```

Use this section to understand general cleanliness.

---

## `column_profiles`

Provides per-column summaries.

Common information:

```text
missing count
unique count
sample values
```

Use this section to understand each column individually.

---

## `row_profiles`

Provides row-level quality details.

Examples:

```text
missing value count per row
duplicate candidate flag
```

Use this section to find rows that may require manual review.

---

## `row_classification`

Reports rows that look suspicious or non-data-like.

Possible classifications:

```text
normal_row
empty_row
comment_row
summary_row
footer_row
garbage_row
```

Example:

```json
{
  "row_index": 5,
  "classification": "summary_row",
  "reason": "First non-empty value starts with a summary marker.",
  "confidence": 0.9
}
```

Important:

```text
Rows are reported only. They are not removed automatically.
```

---

## `type_diagnostics`

Reports columns that mostly look like one type but contain incompatible values.

Example:

```text
amount values: 100, 250.75, unknown, 300
```

Possible diagnostic:

```text
dominant_type = float
invalid value = row 2, unknown
```

Use this section to find values that block reliable type handling.

---

## `validation_report`

Reports constraint validation results when constraints are provided.

Examples:

```text
required value missing
duplicate ID
invalid email
unsupported country
amount below minimum
```

Important:

```text
Validation reports issues only. It does not block export by default.
```

---

## Recommended Review Order

Review the report in this order:

```text
1. parse_diagnostics
2. row_classification
3. validation_report
4. type_diagnostics
5. quality_report
6. column_profiles
7. row_profiles
```

Reason:

```text
Structural issues should be understood before value-level issues.
```

---

## Current Limitation

The report is currently JSON only.

Future stages may add:

```text
HTML reports
CSV issue exports
pretty CLI summaries
quarantine candidate reports
```
