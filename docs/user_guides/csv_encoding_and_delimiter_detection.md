# CSV Encoding and Delimiter Detection Guide

## Purpose

The CSV pipeline can detect common text encodings and delimiters before parsing a CSV file.

This helps with real-world exports from different systems.

---

## Default Behavior

By default, the pipeline attempts to detect:

```text
encoding
delimiter
```

Default encoding candidates:

```text
utf-8-sig
utf-8
cp1252
latin-1
```

Default delimiter candidates:

```text
,
;
\t
|
```

---

## Explicit Encoding

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --encoding cp1252
```

---

## Explicit Delimiter

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --delimiter ";"
```

---

## Disable Auto-Detection

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv `
    --no-auto-detect-csv
```

When disabled, the defaults are:

```text
encoding = utf-8
delimiter = comma
```

---

## Config File Fields

Config files may include:

```json
{
  "encoding": "cp1252",
  "delimiter": ";",
  "auto_detect_csv": true
}
```

---

## Override Policy

Explicit CLI values override config values.

Example:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\semicolon_customers_config.json `
    --delimiter ";"
```

---

## Detection Diagnostics

Detection information is stored in:

```text
parse_diagnostics.detection
```

Typical fields:

```text
selected_encoding
selected_delimiter
confidence
reason
candidate_results
candidate_scores
```

---

## Ambiguous Delimiter Behavior

If delimiter detection is ambiguous, the pipeline falls back to comma.

This fallback is visible in diagnostics.

---

## Safety Rule

Detection does not repair data, remove rows, or change cleaning behavior.

It only decides how to read the file and records diagnostics.
