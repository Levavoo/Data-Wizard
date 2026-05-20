# JSON Pipeline User Guide

## Purpose

This guide explains how to process supported JSON files with Data Wizard.

---

## Supported JSON Shape

First supported shape:

```text
root value is a list
list items are objects
```

Example:

```json
[
  {"customer_id": 1, "name": "Alice", "email": "alice@example.com"},
  {"customer_id": 2, "name": "Bob", "email": "bob@example.com"}
]
```

---

## Column Behavior

```text
object keys become columns
all keys across records are unioned
missing keys become empty/null values
```

---

## Nested Values

Nested objects and arrays are not flattened yet.

Current behavior:

```text
nested objects become compact JSON strings
arrays become compact JSON strings
affected columns appear in parse diagnostics
```

---

## Unsupported JSON Shapes

Not supported yet:

```text
single root object
list of primitive values
mixed list values
JSON Lines / NDJSON
arbitrary deep flattening
root path extraction
multi-table extraction
```

---

## Basic CLI Usage

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\simple_customers.json `
    data\processed\simple_customers_from_json.csv
```

---

## With JSON and HTML Reports

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\nested_values_customers.json `
    data\processed\nested_customers_from_json.csv `
    --report-path data\processed\nested_customers_from_json_report.json `
    --html-report-path data\processed\nested_customers_from_json_report.html
```

---

## With Config File

```powershell
python scripts\run_json_pipeline.py `
    --config examples\json\json_customer_config.json
```

Config must include:

```json
{
  "input_format": "json",
  "input_path": "tests/fixtures/json/simple_customers.json",
  "output_path": "data/processed/json_customers_clean.csv"
}
```

---

## With Quarantine Outputs

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\missing_keys_customers.json `
    data\processed\missing_keys_from_json.csv `
    --quarantine-candidates-path data\processed\missing_keys_quarantine_candidates.json `
    --quarantine-rows-path data\processed\missing_keys_quarantine_rows.csv `
    --accepted-rows-path data\processed\missing_keys_accepted_rows.csv
```

---

## Generated Output Policy

Generated files under `data/processed/` should not be committed by default.

---

## Known Limitations

```text
no JSON Lines / NDJSON
no arbitrary deep flattening
no root_path option yet
no multi-table extraction
nested values are stringified, not normalized into separate columns
```
