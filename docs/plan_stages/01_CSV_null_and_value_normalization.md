# CSV Null and Value Normalization Plan

## Status

```text
Draft — not active until user confirmation.
```

This file is a proposed next CSV improvement plan after `00_CSV_improvements.md`.

It must not be started automatically.

---

## Purpose

Strengthen value-level normalization after the parser foundation is stable.

Goal:

```text
CSV input
→ canonical Table
→ reliable null handling
→ reliable text normalization
→ reliable number normalization
→ safer type inference and casting
```

This plan focuses on the value normalization layer, not parsing structure.

---

## Relationship To Previous Plan

Previous active plan:

```text
docs/plan_stages/00_CSV_improvements.md
```

Previous focus:

```text
CSV parsing diagnostics
short row reporting
extra field reporting
header diagnostics
parser metadata
```

This plan should only begin after the previous plan is complete and explicitly approved by the user.

---

## Architectural Layer

This plan mainly belongs to:

```text
09_Value_Normalization_Layer
08_Type_Layer
```

It must respect these rules:

```text
Adapters only parse formats.
Cleaners normalize values.
Type inference detects likely types.
Type-aware casting applies schema-driven conversion.
Validators validate only.
```

---

# Stage A — Whitespace-Only Null Verification

## Goal

Confirm that whitespace-only cells become `None`.

Examples:

```text
"   "  → None
"\t"   → None
"\n"   → None
" \t " → None
```

## Expected Work

Prefer test-only verification unless a failure is found.

Target files:

```text
tests/test_nulls.py
tests/test_nulls.md
log_protocol/01_CSV_null_and_value_normalization/001_whitespace_only_nulls.md
```

Possible production file only if required:

```text
data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md
```

## Acceptance Criteria

- `normalize_null()` handles whitespace-only strings.
- `clean_table_nulls()` handles whitespace-only table cells.
- CSV pipeline preserves the expected behavior.
- No adapter logic is changed.

---

# Stage B — Extended Null Tokens

## Goal

Support more common null-like values.

Suggested additional tokens:

```text
#N/A
NIL
--
?
missing
unknown
not available
not_applicable
```

## Expected Work

Target files:

```text
data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md
tests/test_nulls.py
tests/test_nulls.md
log_protocol/01_CSV_null_and_value_normalization/002_extended_null_tokens.md
```

## Design Decision Needed

Before implementation, decide whether `unknown` should always become `None`.

Reason:

```text
unknown can mean missing value in many migration files
but it can also be a legitimate category value
```

Recommended safe approach:

```text
Add conservative tokens first: #N/A, NIL, --, ?, not available, not_applicable.
Defer unknown/missing configurability to cleaning profiles.
```

## Acceptance Criteria

- New null tokens normalize to `None`.
- Existing null behavior remains unchanged.
- Tests cover case-insensitive matching.
- Documentation explains token policy.

---

# Stage C — Null Token Statistics Draft

## Goal

Prepare reporting for which null tokens were encountered.

Example future report:

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

## Expected Work

This stage should be design-first.

Possible files:

```text
docs/design/null_token_statistics.md
log_protocol/01_CSV_null_and_value_normalization/003_null_token_statistics_design.md
```

Implementation may be deferred until cleaning profiles exist.

## Acceptance Criteria

- Decide whether statistics belong in cleaner metadata, quality reports, or diagnostic bundles.
- No broad implementation unless the design is approved.

---

# Stage D — Locale-Aware Number Parsing

## Goal

Correctly parse US and European decimal formats.

Examples:

```text
US: 1,000.50 → 1000.50
EU: 1.000,50 → 1000.50
EU: 250,75   → 250.75
EU: 5.500,00 → 5500.00
```

## Current Problem

Current number cleaning assumes US-style separators.

Potential incorrect behavior:

```text
"1.000,50" → 1.0005
"250,75"   → 25075.0
"5.500,00" → 5.5
```

## Expected Work

Target files:

```text
data_processor/cleaners/numbers.py
data_processor/cleaners/numbers.md
tests/test_numbers.py
tests/test_numbers.md
log_protocol/01_CSV_null_and_value_normalization/004_locale_aware_numbers.md
```

## Design Requirements

Support policies:

```text
US number format
EU number format
auto-detection
strict fallback behavior
```

Recommended function shape:

```python
normalize_number(value, locale="auto")
```

Possible modes:

```text
auto
us
eu
strict_us
strict_eu
```

## Acceptance Criteria

- US numbers still parse correctly.
- EU decimal numbers parse correctly.
- Ambiguous values are handled deterministically.
- Invalid values remain unchanged or become controlled failures according to existing cleaner design.
- Type inference and type casting do not regress.

---

# Stage E — Numeric Parsing Diagnostics Draft

## Goal

Prepare diagnostics for numeric parsing confidence and failures.

Example:

```python
{
    "number_diagnostics": {
        "amount": {
            "detected_locale": "eu",
            "invalid_values": [
                {"row_index": 4, "value": "unknown"}
            ]
        }
    }
}
```

## Expected Work

Design first.

Possible files:

```text
docs/design/number_diagnostics.md
log_protocol/01_CSV_null_and_value_normalization/005_number_diagnostics_design.md
```

Implementation should be deferred unless needed by Stage D.

---

# Stage F — Mixed-Type Diagnostics Preparation

## Goal

Prepare for dominant type detection and invalid value reporting.

This overlaps with the previous CSV improvement plan item:

```text
Mixed-Type Columns Need Better Diagnostics
```

## Expected Work

Design the boundary between:

```text
type inference
number cleaning
type-aware casting
diagnostic reporting
```

Possible files:

```text
docs/design/mixed_type_diagnostics.md
log_protocol/01_CSV_null_and_value_normalization/006_mixed_type_diagnostics_design.md
```

## Acceptance Criteria

- Decide whether mixed-type diagnostics belong in inference or casting.
- Do not add broad implementation without approval.

---

# Out Of Scope

This plan does not include:

```text
Excel adapter
JSON adapter
constraint engine expansion
row quarantine
footer row removal
large-file streaming
cleaning profiles
```

---

# Recommended Implementation Order

```text
Stage A — Whitespace-Only Null Verification
Stage B — Extended Null Tokens
Stage C — Null Token Statistics Draft
Stage D — Locale-Aware Number Parsing
Stage E — Numeric Parsing Diagnostics Draft
Stage F — Mixed-Type Diagnostics Preparation
```

---

# Required Protocol Folder

When this plan becomes active, create:

```text
log_protocol/01_CSV_null_and_value_normalization/
```

Each completed stage should get one protocol file.

Example:

```text
001_whitespace_only_nulls.md
002_extended_null_tokens.md
003_null_token_statistics_design.md
004_locale_aware_numbers.md
005_number_diagnostics_design.md
006_mixed_type_diagnostics_design.md
999_plan_completion.md
```

---

# Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 01_CSV_null_and_value_normalization
```

Until then, continue only with the current active plan.
