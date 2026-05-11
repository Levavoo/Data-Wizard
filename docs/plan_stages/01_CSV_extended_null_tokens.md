# CSV Extended Null Tokens Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses only on extending CSV/null-cleaning behavior for additional null-like tokens.

It must not be started automatically.

---

## Purpose

Improve null normalization for common migration-file placeholders that currently may remain as normal strings.

Goal:

```text
raw null-like tokens
→ normalized Python None
→ more reliable type inference
→ cleaner quality reports
→ safer casting and validation
```

---

## Architectural Layer

This plan belongs to:

```text
09_Value_Normalization_Layer
```

Main module area:

```text
data_processor/cleaners/
```

Rules:

```text
Adapters must not normalize nulls.
Null handling belongs in the cleaner layer.
Validators must not change values.
Profilers must not change values.
Exporters must only serialize.
```

---

## Current Behavior

Current null tokens include:

```text
""
null
none
n/a
na
nan
-
```

Current cleaner behavior:

```text
case-insensitive matching
leading/trailing whitespace ignored
non-string values preserved
```

Examples already supported:

```text
" NULL " → None
" n/a "  → None
"   "    → None
```

---

## Problem

Many real CSV migration files use additional placeholders for missing values.

Examples:

```text
#N/A
NIL
--
?
not available
not_applicable
missing
unknown
```

If these stay as strings, they may:

```text
pollute text columns
block numeric type inference
block date type inference
produce misleading quality reports
cause validation false positives
```

---

# Stage A — Conservative Null Token Expansion

## Goal

Add safe, common null tokens that are unlikely to be legitimate business values.

Recommended additions:

```text
#N/A
NIL
--
?
not available
not_applicable
```

## Expected Files

```text
data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md
tests/test_nulls.py
tests/test_nulls.md
log_protocol/01_CSV_extended_null_tokens/001_conservative_null_tokens.md
```

## Acceptance Criteria

- New conservative tokens normalize to `None`.
- Matching remains case-insensitive.
- Leading and trailing whitespace is ignored.
- Existing null token behavior remains unchanged.
- Non-string values remain unchanged.
- No adapter logic changes.

## Example Tests

```python
assert normalize_null("#N/A") is None
assert normalize_null(" NIL ") is None
assert normalize_null("--") is None
assert normalize_null("?") is None
assert normalize_null("not available") is None
assert normalize_null("not_applicable") is None
```

---

# Stage B — Ambiguous Null Token Decision

## Goal

Decide whether ambiguous tokens should be default nulls.

Ambiguous candidates:

```text
missing
unknown
```

## Problem

These tokens often mean missing data, but they can also be real category values.

Examples:

```text
country = unknown
status = unknown
source = missing
```

In some datasets, converting these to `None` is correct.
In other datasets, it destroys meaningful category information.

## Recommended Decision

Do not add `missing` or `unknown` to default global null tokens yet.

Instead, defer them to future configurable cleaning profiles.

Future profile examples:

```text
strict migration profile: unknown → None
survey profile: unknown remains category
CRM profile: missing → None
```

## Expected Files

```text
docs/design/ambiguous_null_tokens.md
log_protocol/01_CSV_extended_null_tokens/002_ambiguous_null_token_decision.md
```

## Acceptance Criteria

- Decision is documented.
- Default cleaner stays conservative.
- Future configurability is planned but not implemented here.

---

# Stage C — Null Token Documentation Cleanup

## Goal

Make null behavior easy to understand for future development.

## Expected Files

```text
data_processor/cleaners/nulls.md
tests/test_nulls.md
```

## Documentation Should Explain

```text
which tokens are normalized
why ambiguous tokens are excluded
case-insensitive matching
whitespace trimming
non-string preservation
where future configurable null profiles belong
```

## Acceptance Criteria

- Documentation matches implemented behavior.
- Examples are included.
- Architectural boundary is clear.

---

# Stage D — Optional Null Token Statistics Design

## Goal

Design future diagnostics for counting which null tokens appeared.

Example future output:

```python
{
    "null_token_stats": {
        "email": {
            "#N/A": 3,
            "NIL": 2,
            "-": 5
        }
    }
}
```

## Expected Files

```text
docs/design/null_token_statistics.md
log_protocol/01_CSV_extended_null_tokens/003_null_token_statistics_design.md
```

## Design Questions

```text
Should stats belong to cleaner metadata?
Should stats appear in quality_report?
Should stats appear in diagnostic_bundle?
Should stats be column-specific?
Should original token casing be preserved?
```

## Acceptance Criteria

- Design location is decided.
- No broad implementation unless separately approved.

---

## Out Of Scope

This plan does not include:

```text
CSV parser diagnostics
locale-aware number parsing
mixed-type diagnostics
cleaning profiles implementation
column-specific null configuration
row quarantine
validation rules
Excel or JSON adapters
```

---

## Recommended Implementation Order

```text
Stage A — Conservative Null Token Expansion
Stage B — Ambiguous Null Token Decision
Stage C — Null Token Documentation Cleanup
Stage D — Optional Null Token Statistics Design
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/01_CSV_extended_null_tokens/
```

Protocol files:

```text
001_conservative_null_tokens.md
002_ambiguous_null_token_decision.md
003_null_token_statistics_design.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 01_CSV_extended_null_tokens
```

Until then, continue only with the currently active confirmed plan.
