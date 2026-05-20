# Real-World Messy Customers Expected Report

## Purpose

This document defines the expected outcome for the heavy real-world messy CSV fixture before any test assertions are added.

Fixture:

```text
tests/fixtures/csv/real_world_messy_customers_heavy.csv
```

This file is intentionally dirty.

It is not meant to prove that the pipeline solves every CSV problem.

It is meant to reveal:

```text
what the current program detects correctly
what the current program normalizes safely
what the current program preserves unchanged
what should become a diagnostic or quarantine/review candidate
what weaknesses should be documented for future stages
```

---

## Safety Baseline

The pipeline should remain conservative.

Expected safety behavior:

```text
rows are not deleted automatically
normal cleaned CSV still includes parsed rows
quarantine is report/export only
formula-like text is not executed
HTML-like text is not rendered or interpreted by the cleaner
ambiguous values are not aggressively guessed
lossy transformations should be documented as weaknesses
```

---

## Fixture Overview

The fixture represents a legacy CRM export with:

```text
metadata rows before the header
UTF-8 BOM
semicolon delimiter
duplicate headers
mixed number formats
mixed date formats
mixed boolean formats
invalid emails
missing values
duplicate IDs
duplicate emails
malformed row lengths
multiline quoted fields
escaped quotes
risky text values
summary/footer rows
known unsupported or ambiguous values
```

---

# Expected Parser Diagnostics

## 1. Encoding Detection

The fixture starts with a UTF-8 BOM.

Expected:

```text
selected encoding: utf-8-sig
BOM should not appear in the first header name
parse_diagnostics.encoding should be utf-8-sig
parse_diagnostics.detection.encoding should exist
encoding confidence should indicate high confidence or BOM-based detection
```

Must not happen:

```text
first header contains \ufeff
file fails only because of BOM
```

---

## 2. Delimiter Detection

The fixture uses semicolon delimiter.

Expected:

```text
selected delimiter: ;
columns should split into expected fields
parse_diagnostics.delimiter should be ;
parse_diagnostics.detection.delimiter should exist
```

Must not happen:

```text
whole line treated as one comma-delimited field
semicolon inside quoted text breaks columns
```

---

## 3. Header Row Detection

The file starts with metadata rows before the real header.

Expected:

```text
header_row_index > 0
preamble_row_count > 0
metadata rows are stored as preamble metadata, not normal customer rows
parse diagnostics should warn that header row was not the first source row
```

Expected header row:

```text
Customer ID;Name;Email;Email;Country;Amount;Signup Date;Active;Notes;Phone;Postal Code;Score
```

---

## 4. Header Normalization

Expected normalized column names:

```text
customer_id
name
email
email_2
country
amount
signup_date
active
notes
phone
postal_code
score
```

Reason:

```text
header names are lowercased
spaces become underscores
duplicate Email header becomes email and email_2
```

---

## 5. Duplicate Header Diagnostics

The header has duplicate `Email` columns.

Expected:

```text
parse_diagnostics.duplicate_headers contains email
parse diagnostics warning about duplicated headers exists
schema keeps both columns using unique normalized names
```

---

## 6. Extra Field Diagnostics

Rows with extra fields include examples like:

```text
Rita Extra
Wrong Column Count Many
possibly malformed quote region depending parser behavior
```

Expected:

```text
parse_diagnostics.rows_with_extra_fields is not empty
parse_diagnostics.extra_field_count > 0
rows with extra fields do not crash the pipeline
affected rows are review/quarantine candidates if diagnostics are integrated into quarantine logic
```

Expected limitation:

```text
extra fields beyond known headers may not be preserved in the cleaned table
```

This is acceptable for now if documented.

---

## 7. Missing Field Diagnostics

Rows with missing fields include:

```text
Sam Short
summary/footer rows
possibly malformed quote region depending parser behavior
```

Expected:

```text
parse_diagnostics.rows_with_missing_fields is not empty
parse_diagnostics.missing_field_count > 0
short rows do not crash the pipeline
missing cells become None or empty before null normalization
```

---

## 8. Multiline Quoted Field

Example:

```text
Uma Multiline
```

Expected:

```text
multiline quoted notes field remains one logical cell
row should not split into two customer rows because of newline inside quotes
cleaned CSV export should quote multiline text safely
```

---

## 9. Escaped Quotes

Example:

```text
She said ""hello"" yesterday
```

Expected:

```text
escaped quote syntax parses correctly
resulting text preserves quote meaning
row is not suspicious only because it contains escaped quotes
```

---

## 10. Broken / Unbalanced Quote Area

The fixture intentionally contains a broken quote region around rows 61-62.

Expected at current stage:

```text
pipeline should not crash if Python csv parser can recover
parse diagnostics may show missing/extra fields or merged content
this should be treated as a weakness area
```

Important expected weakness:

```text
current parser may not precisely identify the unbalanced quote source line
current parser may merge rows in a way that is hard to diagnose
```

Do not write brittle assertions for exact behavior here until observed.

---

# Expected Cleaning Behavior

## 1. Whitespace Cleanup

Examples:

```text
 Alice Smith 
email with surrounding spaces
country with trailing spaces
Multiple   Internal   Spaces
```

Expected:

```text
leading/trailing whitespace should be trimmed
repeated internal whitespace should collapse where the text cleaner applies
country value with trailing spaces should normalize to Germany
email with surrounding spaces should trim before validation
```

---

## 2. Null Normalization

Null-like examples:

```text
empty cells
whitespace-only cells
null
NA
N/A
#N/A
```

Expected according to current conservative policy:

```text
known supported null tokens should become None
empty and whitespace-only values should become None
ambiguous tokens should follow the current null-token policy
```

Expected weakness to check:

```text
#N/A may remain unsupported or ambiguous depending current policy
spreadsheet-style null tokens may need future configurable policy
```

---

## 3. Number Normalization

Examples:

```text
1.200,50
250,75
1000.00
2,500.75
2.500,75
1 234,56
1.234.567,89
1,234,567.89
```

Expected:

```text
common EU and US formats should normalize where current number parser supports them
negative amount should remain numeric if parsed, then fail min constraint
zero amount should remain valid numeric value
```

Expected weakness candidates:

```text
space thousand separator may be unsupported
currency symbol values may not parse as numbers
percent values may not parse as amount numbers
text amount values should not be coerced silently
```

---

## 4. Date Handling

Examples:

```text
2024-01-31
31.01.2024
2024/02/15
15-02-2024
03/04/2024
2024-05-13T10:45:00Z
45325
not a date
empty date
```

Expected:

```text
supported date formats should normalize or infer as date where current logic allows
empty date should become missing/null
invalid date strings should be flagged through mixed-type/type diagnostics if dominant type is date
```

Expected weakness candidates:

```text
ambiguous date 03/04/2024 should not be blindly interpreted without policy
Excel serial date 45325 may be unsupported
timestamp with timezone may be unsupported or may remain text
```

---

## 5. Boolean Handling

Examples:

```text
YES
no
TRUE
false
Y
1
0
Yes
No
maybe
ja
nein
```

Expected:

```text
supported boolean tokens should normalize
unsupported tokens should remain visible as invalid/mixed values
maybe should not be coerced to boolean
German ja/nein may be unsupported and should be documented as future improvement if so
```

---

## 6. Text Preservation

Examples:

```text
=SUM(A1:A2)
+CMD|' /C calc'!A0
<b>HTML-like note</b>
Unicode names
emoji
notes containing comma, semicolon, pipe, tab
```

Expected:

```text
formula-like text remains text
HTML-like text remains text
Unicode is preserved
emoji is preserved if encoding/parser supports it
quoted delimiters inside notes do not split columns
```

Expected weakness candidate:

```text
spreadsheet injection hardening is not implemented yet
```

This means values may remain dangerous if opened directly in spreadsheet software. The program should not claim this is solved.

---

# Expected Type Diagnostics

The fixture should produce mixed-type diagnostics for multiple columns.

Expected likely mixed columns:

```text
amount
signup_date
active
score
customer_id
postal_code
email
country
```

Expected diagnostics:

```text
invalid numeric-like values should appear in type diagnostics
invalid date-like values should appear in type diagnostics
invalid boolean-like values should appear in type diagnostics
columns with dominant types plus outliers should be reported
```

Important:

```text
exact counts should not be asserted until baseline observation is recorded
```

---

# Expected Constraint Validation Behavior

A dedicated constraint config should be created before validation tests.

Expected file:

```text
tests/fixtures/csv/real_world_messy_customers_constraints.json
```

Expected realistic constraints:

```text
customer_id required
customer_id unique
email regex
email required if policy decides primary email is required
country allowed values
amount min_value 0
score min_value 0
score max_value 100
```

Expected validation failures:

```text
duplicate customer_id 16
invalid email formats
missing email values
unknown country Atlantis
missing country
negative amount
negative score
score above 100
possibly text score values
```

Potential future constraints not required yet:

```text
postal code format by country
phone format
date range
signup_date required
email unique
```

---

# Expected Row Classification and Quarantine Behavior

Expected suspicious/review candidate rows include:

```text
summary/footer rows: TOTAL, Grand Total, End of export, Rows exported
rows with extra fields
rows with missing fields
rows with validation failures
rows with invalid/mixed type values
rows with duplicate IDs
rows with invalid emails
rows with unknown countries
rows with risky formula-like text may be future candidate if such rule exists
```

Expected quarantine behavior:

```text
quarantine candidates should be reported
quarantine rows CSV should be exportable
accepted rows CSV should be exportable
normal cleaned CSV should still include parsed rows by default
```

Do not expect:

```text
automatic deletion of footer rows
automatic deletion of invalid rows
automatic repair of malformed rows
```

---

# Expected Preserved Values

The following should be preserved unless the current cleaner has an explicit safe normalization:

```text
formula-like text
HTML-like text
Unicode names
emoji
multiline note text
escaped quote meaning
quoted delimiters inside notes
phone numbers as text-like values if not configured otherwise
```

Special concern:

```text
postal codes and customer IDs with leading zeros should ideally be preserved,
but current type inference may convert them if inferred as numeric.
```

If leading zeros are lost, document it as a weakness rather than changing expectations silently.

---

# Expected Weaknesses To Watch

This fixture is designed to reveal weaknesses.

Expected possible weaknesses:

```text
unbalanced quote source location may not be diagnosed precisely
leading zeros in IDs/postal codes may be lost
postal codes may be inferred as numbers instead of semantic text
currency values may not parse cleanly
percent values may not parse cleanly
Excel serial dates may not be supported
German boolean tokens ja/nein may not be supported
spreadsheet formula injection is not escaped
HTML-like text is not sanitized
extra fields are detected but not preserved
summary/footer rows are flagged but not removed
country normalization may be exact-match only
phone number validation is not implemented
```

These should feed future improvement stages.

---

# Expected Report Sections For Baseline Observation

When the first observation test/script is created, capture or verify these report sections:

```text
parse_diagnostics
quality_report
column_profiles
row_profiles
row_classification
type_diagnostics
validation_report
quarantine_candidates
pipeline_status
```

---

# Initial Testing Strategy

Do not start with exact-count tests.

Start with broad assertions:

```text
pipeline completes or failure is documented
parse diagnostics exist
encoding is detected
semicolon delimiter is detected
header row is not first row
duplicate header is detected
extra/missing fields are reported
validation report has failures
quarantine candidates exist
expected report files can be exported
```

Only after baseline observation should stable exact counts be added.

---

# Out Of Scope For This Stage

This expected report does not require fixing:

```text
all malformed CSV quote behavior
all date formats
all currency formats
all locale formats
all semantic types
spreadsheet injection escaping
HTML sanitization
phone/country/postal databases
row deletion
interactive review UI
streaming large-file processing
```

---

## Final Rule

If observed behavior differs from this expected report, do one of two things:

```text
1. fix the code if the expectation reflects already-supported intended behavior
2. update observed weakness documentation if the expectation reveals a real current limitation
```

Do not hide weaknesses by weakening the test without documenting the reason.
