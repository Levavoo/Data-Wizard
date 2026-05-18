# generate_csv_performance_fixture.py

## Purpose

Generates deterministic CSV files for performance testing.

Generated files are artifacts and should not be committed by default.

---

## Default Output

```text
data/performance/csv_performance_fixture.csv
```

---

## Basic Usage

PowerShell:

```powershell
python scripts\performance\generate_csv_performance_fixture.py
```

---

## Generate 10,000 Rows

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --output-path data\performance\csv_performance_10000.csv
```

---

## Generate Semicolon CSV

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --delimiter ";" `
    --output-path data\performance\csv_performance_10000_semicolon.csv
```

---

## Generate UTF-8 BOM CSV

```powershell
python scripts\performance\generate_csv_performance_fixture.py `
    --rows 10000 `
    --bom `
    --output-path data\performance\csv_performance_10000_bom.csv
```

---

## Arguments

| Argument | Purpose | Default |
|---|---|---|
| `--rows` | Number of data rows to generate | `1000` |
| `--output-path` | Output CSV path | `data/performance/csv_performance_fixture.csv` |
| `--delimiter` | CSV delimiter | `,` |
| `--bom` | Write UTF-8 BOM | disabled |
| `--dirty-every` | Inject controlled dirty values every N rows | `25` |

---

## Generated Columns

```text
customer_id
name
email
country
amount
signup_date
active
notes
phone
postal_code
score
```

---

## Dirty Value Injection

Controlled dirty values are injected deterministically.

Examples:

```text
EU amount format
invalid email
invalid boolean token
invalid country
score above 100
```

Disable dirty injection:

```powershell
python scripts\performance\generate_csv_performance_fixture.py --dirty-every 0
```

---

## Artifact Policy

Generated files should not be committed by default.

Recommended generated locations:

```text
data/performance/
data/generated/
```
