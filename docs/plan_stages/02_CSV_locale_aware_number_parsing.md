# CSV Locale-Aware Number Parsing Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on making numeric normalization reliable for CSV data that uses different decimal and thousands separator conventions.

It must not be started automatically.

---

## Purpose

Improve numeric parsing so CSV files with US-style and European-style numbers are handled correctly.

Goal:

```text
raw CSV numeric strings
→ locale-aware normalization
→ reliable type inference
→ reliable type-aware casting
→ cleaner exports and diagnostics
```

---

## Problem

Current number cleaning assumes US-style formatting.

US examples:

```text
1,000.50 → 1000.50
250.75   → 250.75
5,500.00 → 5500.00
```

European examples:

```text
1.000,50 → 1000.50
250,75   → 250.75
5.500,00 → 5500.00
```

Known risk:

```text
"1.000,50" may be parsed incorrectly
"250,75" may be parsed incorrectly
"5.500,00" may be parsed incorrectly
```

This can break:

```text
type inference
numeric casting
quality reporting
exports
analytics
migration validation
```

---

## Architectural Layer

This plan belongs mainly to:

```text
08_Type_Layer
09_Value_Normalization_Layer
```

Main module area:

```text
data_processor/cleaners/numbers.py
```

Rules:

```text
Adapters must not parse numeric locale semantics.
Number normalization belongs in cleaner/type layers.
Type inference should benefit from normalized numbers.
Diagnostics should explain ambiguous or failed parsing.
Exporters should only serialize final values.
```

---

# Stage A — Current Behavior Verification

## Goal

Add regression tests that prove the current behavior for US and EU number strings.

This stage should first expose the current bug clearly.

## Expected Files

```text
tests/test_numbers.py
tests/test_numbers.md
log_protocol/02_CSV_locale_aware_number_parsing/001_current_behavior_verification.md
```

## Acceptance Criteria

- Tests cover US-style numbers.
- Tests cover EU-style numbers.
- Current failures are documented if EU parsing fails.
- No production code change is required in this stage unless test-only verification is impossible.

---

# Stage B — Number Format Policy Design

## Goal

Define supported numeric locale policies.

Recommended policies:

```text
auto
us
eu
strict_us
strict_eu
```

## Policy Meaning

### `auto`

Detect likely format from the string or column context.

### `us`

Parse values as US-style numbers.

Example:

```text
1,000.50 → 1000.50
```

### `eu`

Parse values as European-style numbers.

Example:

```text
1.000,50 → 1000.50
```

### `strict_us`

Only parse valid US-style numbers.

Invalid or ambiguous values should remain unchanged or be reported.

### `strict_eu`

Only parse valid EU-style numbers.

Invalid or ambiguous values should remain unchanged or be reported.

## Expected Files

```text
docs/design/number_format_policy.md
log_protocol/02_CSV_locale_aware_number_parsing/002_number_format_policy.md
```

## Acceptance Criteria

- Supported policies are documented.
- Ambiguous values are considered.
- Default behavior is defined.

---

# Stage C — Locale-Aware Number Normalization

## Goal

Implement locale-aware number normalization.

Possible function shape:

```python
normalize_number(value, locale="auto")
```

or:

```python
normalize_number(value, number_format="auto")
```

## Expected Files

```text
data_processor/cleaners/numbers.py
data_processor/cleaners/numbers.md
tests/test_numbers.py
tests/test_numbers.md
log_protocol/02_CSV_locale_aware_number_parsing/003_locale_aware_number_normalization.md
```

## Acceptance Criteria

- Existing US-style numeric parsing still works.
- EU-style decimal numbers parse correctly.
- Thousands separators are handled correctly.
- Invalid strings remain unchanged according to existing cleaner behavior.
- Non-string values remain unchanged unless existing behavior already converts them.
- Tests cover positive, negative, integer, float, US, EU, and invalid values.

---

# Stage D — Column-Level Auto Detection Draft

## Goal

Design how column-level numeric format detection should work later.

Reason:

A single value can be ambiguous.

Examples:

```text
1,234
1.234
```

These may mean different things depending on locale.

## Expected Files

```text
docs/design/number_column_auto_detection.md
log_protocol/02_CSV_locale_aware_number_parsing/004_column_auto_detection_draft.md
```

## Acceptance Criteria

- Ambiguous values are documented.
- Column-level majority detection is proposed.
- Single-value auto-detection limitations are documented.
- No broad implementation unless separately approved.

---

# Stage E — Numeric Diagnostics Draft

## Goal

Design future diagnostics for numeric parsing decisions and failures.

Possible future diagnostic shape:

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

## Expected Files

```text
docs/design/number_diagnostics.md
log_protocol/02_CSV_locale_aware_number_parsing/005_number_diagnostics_draft.md
```

## Acceptance Criteria

- Diagnostic requirements are documented.
- Invalid values are reportable.
- Ambiguous values are reportable.
- Diagnostics remain report-only and do not mutate values.

---

# Stage F — Pipeline Integration Check

## Goal

Verify locale-aware number parsing works through the normal CSV pipeline.

Target fixture:

```text
tests/fixtures/csv/european_decimals.csv
```

Expected files:

```text
tests/test_pipeline.py
tests/test_pipeline.md
log_protocol/02_CSV_locale_aware_number_parsing/006_pipeline_integration_check.md
```

## Acceptance Criteria

- Pipeline handles EU decimal CSV values correctly.
- Cleaned output contains correct numeric values.
- Existing US pipeline behavior does not regress.
- Diagnostic bundle remains valid.

---

## Out Of Scope

This plan does not include:

```text
Excel adapter
JSON adapter
full cleaning profiles
currency parsing
unit parsing
percentage parsing
mixed-type diagnostics implementation
constraint validation expansion
```

---

## Recommended Implementation Order

```text
Stage A — Current Behavior Verification
Stage B — Number Format Policy Design
Stage C — Locale-Aware Number Normalization
Stage D — Column-Level Auto Detection Draft
Stage E — Numeric Diagnostics Draft
Stage F — Pipeline Integration Check
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/02_CSV_locale_aware_number_parsing/
```

Protocol files:

```text
001_current_behavior_verification.md
002_number_format_policy.md
003_locale_aware_number_normalization.md
004_column_auto_detection_draft.md
005_number_diagnostics_draft.md
006_pipeline_integration_check.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 02_CSV_locale_aware_number_parsing
```

Until then, continue only with the currently active confirmed plan.
