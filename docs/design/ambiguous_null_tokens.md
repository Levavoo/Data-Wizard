# Ambiguous Null Tokens

## Purpose

This document defines the default policy for ambiguous null-like tokens.

Ambiguous tokens are values that may mean missing data in some migration files but may also be valid category values in others.

Examples:

```text
unknown
missing
```

---

## Decision

The default cleaner preserves ambiguous tokens.

Default behavior:

```text
unknown → "unknown"
missing → "missing"
```

They are not included in the global `NULL_VALUES` set.

---

## Reason

Converting ambiguous tokens globally can cause silent data loss.

Example:

```csv
customer_id,status
1,unknown
2,missing
```

In this dataset, `unknown` and `missing` may be meaningful categories.

If the default cleaner converted them to `None`, downstream users would lose information that may be important for analysis, reporting, or migration review.

---

## Conservative Default Policy

The default null cleaner should include tokens that are very likely to mean missing data.

Examples:

```text
""
null
none
n/a
na
nan
-
#n/a
nil
--
?
not available
not_applicable
```

The default null cleaner should exclude ambiguous tokens.

Examples:

```text
unknown
missing
```

---

## Future Configurable Profiles

Future cleaning profiles may allow project-specific behavior.

Examples:

```text
strict migration profile: unknown → None, missing → None
survey profile: unknown remains category
CRM profile: missing → None, unknown remains category
```

Possible future configuration shape:

```python
{
    "global_null_tokens": ["", "null", "n/a", "#N/A"],
    "ambiguous_null_tokens": ["unknown", "missing"],
    "columns": {
        "email": {
            "extra_null_tokens": ["unknown", "missing"]
        },
        "status": {
            "preserve_tokens": ["unknown"]
        }
    }
}
```

---

## Architecture Rules

- Adapters must not normalize ambiguous tokens.
- Default cleaners should remain conservative.
- Column-specific behavior belongs to future cleaning profiles.
- Validators should not mutate ambiguous values.
- Profilers should report observed values but not change them.

---

## Current Regression Test

The behavior is protected by:

```text
tests/test_nulls.py
```

Relevant test:

```python
def test_preserve_ambiguous_null_like_values() -> None:
    assert normalize_null("unknown") == "unknown"
    assert normalize_null("missing") == "missing"
```

---

## Future Work

Possible future stages:

- configurable null token profiles
- column-specific null policy rules
- null token statistics
- profile-driven migration modes
