# CSV Core Known Limitations

## Purpose

This document summarizes known CSV core limitations before release/merge readiness.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Scope

This document summarizes limitations from:

```text
real-world messy CSV suite
performance layer review
current CSV adapter behavior
current pipeline/report behavior
```

It does not list every possible future feature.

---

## Real-World CSV Limitations

### Malformed Quote Diagnostics

Current limitation:

```text
unbalanced quote source location may not be reported precisely
rows may be merged by Python csv behavior before diagnostics can identify source line clearly
```

Future improvement:

```text
malformed quote pre-scan or parser wrapper
source line tracking
quote-balance diagnostics
```

---

### Multiline Text Preservation

Current behavior:

```text
parser reads multiline quoted fields
text cleaner collapses embedded newlines to spaces
```

Current limitation:

```text
exact multiline text formatting is not preserved after cleaning
```

Future improvement:

```text
profile/config option for preserving multiline text
```

---

### Leading-Zero Preservation

Current limitation:

```text
IDs, postal codes, and phone-like values can be at risk if inferred as numeric
```

Future improvement:

```text
semantic text columns
force_text_columns config option
```

---

### Currency, Percent, and Text Amounts

Current limitation:

```text
currency symbols, percent values, and text-number amounts are not fully normalized
```

Future improvement:

```text
explicit numeric parse diagnostics
currency/percent policy
locale-aware numeric profiles
```

---

### Date Ambiguity and Excel Serial Dates

Current limitation:

```text
ambiguous dates are not fully policy-driven
Excel serial dates may be unsupported
```

Future improvement:

```text
date parsing profiles
Excel serial date option
locale-specific date policies
```

---

### Locale-Specific Boolean Tokens

Current limitation:

```text
German tokens such as ja/nein may be unsupported
```

Future improvement:

```text
locale-aware boolean token profiles
```

---

### Spreadsheet Injection Safety

Current limitation:

```text
formula-like cells remain text but are not escaped for spreadsheet safety
```

Future improvement:

```text
optional spreadsheet injection hardening during CSV export
```

---

### HTML-Like Text

Current limitation:

```text
HTML-like text is preserved as text and not sanitized as a data-cleaning step
```

Current safety expectation:

```text
HTML report rendering must escape displayed values where row previews are added in future
```

---

### Extra Field Preservation

Current limitation:

```text
extra fields are detected in parse diagnostics but may not be preserved in the normalized table
```

Future improvement:

```text
optional raw row / extra fields metadata preservation
```

---

### Footer/Summary Rows

Current behavior:

```text
summary/footer rows can be flagged as suspicious or quarantined
```

Current limitation:

```text
they are not automatically removed from the normal cleaned output
```

Future improvement:

```text
optional exclude_quarantine_candidates_from_clean_output mode
```

---

## Performance Limitations

### Non-Streaming Pipeline

Current limitation:

```text
CSV data is loaded into memory and processed as an in-memory Table
```

Future improvement:

```text
streaming read/write layer
chunked processing
streaming exports
```

---

### Diagnostics Can Grow Large

Current limitation:

```text
row profiles, validation failures, quarantine candidates, JSON reports, and HTML reports can grow with row count
```

Future improvement:

```text
diagnostic depth controls
summary-first report mode
sampled row previews
```

---

### Performance Metrics Are Local

Current limitation:

```text
performance metrics are machine-dependent and not yet used as CI gates
```

Future improvement:

```text
manual benchmark workflow
scheduled performance workflow
advisory threshold reports
```

---

## Format Limitations

Currently supported core format:

```text
CSV
```

Not yet implemented:

```text
JSON adapter
Excel adapter
GUI/web interface
```

Recommended order after stabilization:

```text
JSON adapter
Excel adapter
GUI/local web interface
```

---

## Release Claim Boundary

Safe claim:

```text
The CSV pipeline can clean, profile, validate, report, quarantine, configure, detect common encodings/delimiters, run real-world diagnostic tests, and measure performance baselines.
```

Do not claim:

```text
all dirty CSVs are repaired automatically
all locale formats are supported
spreadsheet injection is solved
HTML sanitization is solved
large-file streaming is solved
Excel/JSON are supported
GUI exists
```

---

## Future Stage Candidates

Recommended candidates:

```text
18_JSON_adapter
19_Excel_adapter
20_GUI_or_local_web_interface
CSV_semantic_text_columns
CSV_malformed_quote_diagnostics
CSV_spreadsheet_injection_export_safety
CSV_locale_profiles_for_dates_booleans_numbers
CSV_diagnostic_depth_controls
CSV_streaming_export_layer
CSV_type_inference_cache
```
