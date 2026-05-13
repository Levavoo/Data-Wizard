# customer_migration_sample.csv

## Purpose

This file is a small demonstration CSV for the cleaning and diagnostics pipeline.

It is intentionally messy so users can see how diagnostics behave.

---

## File

```text
examples/csv/customer_migration_sample.csv
```

---

## Included Issues

### Normal rows

Rows for Alice and Bob are mostly valid customer records.

---

### Duplicate customer ID

Customer ID `2` appears twice.

Expected diagnostic area:

```text
validation_report
```

---

### Unsupported country

`Mars` is not part of the example allowed country list.

Expected diagnostic area:

```text
validation_report
```

---

### Invalid email

`invalid-email` does not match the example email regex.

Expected diagnostic area:

```text
validation_report
```

---

### Negative amount

`-5` violates the example minimum amount rule.

Expected diagnostic area:

```text
validation_report
```

---

### Null-like values

Examples:

```text
#N/A
not available
```

Expected behavior:

```text
normalized to None
```

---

### US and EU number formats

Examples:

```text
1,000.50
250,75
5.500,00
```

Expected behavior:

```text
converted to numeric values
```

---

### Suspicious rows

Rows:

```text
TOTAL
End of export
```

Expected diagnostic area:

```text
row_classification
```

---

## Intended Use

Run this file through the CLI with:

```text
examples/csv/customer_constraints.json
```

and inspect the generated diagnostic JSON report.
