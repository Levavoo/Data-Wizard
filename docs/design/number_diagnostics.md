# Number Diagnostics

## Purpose

This document drafts future diagnostics for numeric parsing decisions and failures.

---

## Why Diagnostics Are Needed

Number parsing can be ambiguous or fail.

Examples:

```text
1,234
1.234
unknown
100 EUR
```

Users need to know which values were parsed, preserved, or considered ambiguous.

---

## Proposed Diagnostic Shape

```python
{
    "number_diagnostics": {
        "amount": {
            "detected_format": "eu",
            "parsed_count": 10,
            "failed_count": 2,
            "ambiguous_count": 1,
            "invalid_values": [
                {"row_index": 4, "value": "unknown"}
            ]
        }
    }
}
```

---

## Required Concepts

```text
detected_format
parsed_count
failed_count
ambiguous_count
invalid_values
```

---

## Design Rules

Diagnostics should be report-only.

They should not:

```text
mutate values
replace validation reports
hide original values
```

---

## Future Placement

Possible future placement:

```text
diagnostic_bundle["number_diagnostics"]
```

Final placement should be decided during mixed-type and type-diagnostics work.
