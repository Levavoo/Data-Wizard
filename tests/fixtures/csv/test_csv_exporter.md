# test_csv_exporter.py

## Purpose

Tests the CSV exporter module.

This verifies that the internal `Table` model can be exported into valid CSV output.

Architecture:

```text
Table
→ CSV Exporter
→ CSV File
```

---

# Tested File

```text
data_processor/exporters/csv_exporter.py
```

---

# Current Test Coverage

## `test_serialize_none`

Verifies:

```python
None
```

becomes:

```text
""
```

during CSV export.

---

## `test_serialize_boolean_values`

Verifies booleans become lowercase strings.

Examples:

```python
True
→ "true"

False
→ "false"
```

---

## `test_serialize_date`

Verifies Python `date` objects become ISO date strings.

Example:

```python
date(2026, 1, 31)
→ "2026-01-31"
```

---

## `test_serialize_datetime`

Verifies Python `datetime` objects become ISO datetime strings.

Example:

```python
datetime(...)
→ "2026-01-31 14:30:00"
```

---

## `test_serialize_regular_values`

Verifies normal values are stringified correctly.

Examples:

```python
100
25.5
"Alice"
```

---

## `test_export_table_to_csv`

Verifies complete CSV export.

Checks:

- file creation
- header output
- row output
- UTF-8 writing
- serialized values

---

## `test_export_creates_directories`

Verifies missing output directories are created automatically.

Example:

```text
nested/folder/customers.csv
```

---

# Important Design Rule

Exporters only write data.

They should not:

- clean values
- infer schema
- validate rules
- transform rows

Those belong to earlier pipeline stages.

---

# Why CSV Export Matters

CSV export completes the first end-to-end workflow:

```text
CSV Input
→ Parse
→ Internal Table
→ Cleaning
→ Validation
→ CSV Output
```

This is the first fully usable migration pipeline.

---

# Run Tests

```powershell
pytest tests\test_csv_exporter.py
```

Expected result:

```text
7 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\exporters\csv_exporter.py `
    tests\test_csv_exporter.py

black `
    data_processor\exporters\csv_exporter.py `
    tests\test_csv_exporter.py

pytest tests\test_csv_exporter.py
```

---

# Developer Notes

This exporter intentionally avoids pandas.

The project architecture uses:

```text
many formats
→ one canonical model
→ many exporters
```

Therefore exporters should remain:

- explicit
- deterministic
- lightweight
- format-independent

---

# Future Improvements

Possible future additions:

- configurable delimiters
- compressed CSV export
- append mode
- metadata sidecar files
- chunked streaming export
- quote handling configuration
- large-file optimization