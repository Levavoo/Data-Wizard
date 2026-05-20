# JSON Pipeline CLI

## Purpose

Runs supported JSON input through the Data Wizard pipeline.

---

## Basic Usage

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\simple_customers.json `
    data\processed\simple_customers_from_json.csv
```

---

## With Reports

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\missing_keys_customers.json `
    data\processed\missing_keys_from_json.csv `
    --report-path data\processed\missing_keys_from_json_report.json `
    --html-report-path data\processed\missing_keys_from_json_report.html
```

---

## With Quarantine Exports

```powershell
python scripts\run_json_pipeline.py `
    tests\fixtures\json\missing_keys_customers.json `
    data\processed\missing_keys_from_json.csv `
    --quarantine-candidates-path data\processed\missing_keys_quarantine_candidates.json `
    --quarantine-rows-path data\processed\missing_keys_quarantine_rows.csv `
    --accepted-rows-path data\processed\missing_keys_accepted_rows.csv
```
