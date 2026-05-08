# test_json_report_exporter.py

## Purpose

Tests the JSON report exporter.

This verifies that report dictionaries can be saved as JSON files.

Architecture:

```text
Report Dictionary
→ JSON Report Exporter
→ JSON File
```

---

# Tested File

```text
data_processor/exporters/json_report_exporter.py
```

---

# Current Test Coverage

## `test_serialize_date`

Verifies Python `date` objects become ISO strings.

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

## `test_serialize_set`

Verifies sets are serialized deterministically.

---

## `test_serialize_unsupported_value`

Verifies unsupported objects raise:

```python
TypeError
```

---

## `test_export_report_to_json`

Verifies JSON report file creation.

Checks:

- file exists
- JSON can be read back
- date/datetime values are serialized correctly
- normal report fields are preserved

---

## `test_export_report_creates_directories`

Verifies missing output folders are created automatically.

---

# Important Design Rule

Report exporters only serialize reports.

They must never:

- clean data
- validate constraints
- infer schema
- modify tables
- modify reports semantically

---

# Run Tests

```powershell
pytest tests\test_json_report_exporter.py
```

Expected:

```text
6 passed
```

---

# Recommended Validation Workflow

```powershell
ruff check `
    data_processor\exporters\json_report_exporter.py `
    tests\test_json_report_exporter.py

black `
    data_processor\exporters\json_report_exporter.py `
    tests\test_json_report_exporter.py

pytest tests\test_json_report_exporter.py
pytest
```

---

# Developer Notes

This exporter will later support:

- quality report export
- validation report export
- column profile export
- row profile export
- full diagnostic bundles