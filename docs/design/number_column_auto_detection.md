# Number Column Auto Detection

## Purpose

This document drafts future column-level number format detection.

Single-value auto detection is useful, but a full column gives better context.

---

## Problem

Some values are ambiguous alone.

Examples:

```text
1,234
1.234
```

Depending on locale, these may mean:

```text
1234
1.234
```

---

## Proposed Future Approach

For each candidate numeric column:

```text
1. sample non-null string values
2. count US-looking values
3. count EU-looking values
4. count ambiguous values
5. choose dominant format if confidence is high
6. preserve/report ambiguous values if confidence is low
```

---

## Possible Metadata

```python
{
    "column": "amount",
    "detected_number_format": "eu",
    "confidence": 0.92,
    "us_like_count": 1,
    "eu_like_count": 23,
    "ambiguous_count": 3
}
```

---

## Design Rule

Column-level detection should feed cleaner/type-casting policy.

It should not live in the CSV adapter.

---

## Out Of Scope

This document does not implement column-level detection.
