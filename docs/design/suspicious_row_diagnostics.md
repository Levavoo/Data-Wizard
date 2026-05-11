# Suspicious Row Diagnostics

## Purpose

This document defines the diagnostic model for suspicious CSV rows.

Suspicious rows are parsed table rows that may not represent normal data records.

---

## Examples

```text
# comment row
TOTAL,,650.50
End of export,
random free text,,
```

---

## Diagnostic Shape

```python
{
    "row_index": 5,
    "classification": "summary_row",
    "reason": "First non-empty value starts with a summary marker.",
    "confidence": 0.9,
    "row": {
        "customer_id": "TOTAL",
        "amount": "650.50"
    }
}
```

---

## Row Index Semantics

`row_index` is zero-based and refers to the table row index after parsing.

It does not include the header row.

---

## Classifications

Current classification values:

```text
normal_row
empty_row
comment_row
summary_row
footer_row
garbage_row
```

---

## Confidence Meaning

Confidence is a heuristic score between `0.0` and `1.0`.

It describes how strongly the classifier believes the row matches the assigned classification.

It is not a probability.

---

## Design Rule

Suspicious row diagnostics are report-only.

They must not:

- remove rows
- quarantine rows
- repair values
- mutate the table
- modify exports

---

## Future Work

Future stages may add:

- quarantine candidates
- configurable classification rules
- issue export files
- source-row index mapping
- confidence tuning
