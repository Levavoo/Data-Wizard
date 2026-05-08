# json_report_exporter.py

## Purpose

`json_report_exporter.py` writes report dictionaries to JSON files.

This module belongs to the exporter layer.

Architecture:

```text
Report Dictionary
→ JSON Report Exporter
→ JSON File
```

---

# Why This Module Exists

The project now produces several diagnostic objects:

```text
quality_report
validation_report
column_profiles
row_profiles
```

Terminal output is useful during development, but real migration projects need saved reports.

Saved JSON reports help with:

- audit trails
- debugging
- migration diagnostics
- future UI dashboards
- automated review
- reproducibility

---

# Main Functions

## `export_report_to_json(report, output_path, encoding="utf-8", indent=4)`

Writes a report dictionary to a JSON file.

Example:

```python
from data_processor.exporters.json_report_exporter import export_report_to_json

export_report_to_json(
    report=quality_report,
    output_path="data/processed/quality_report.json",
)
```

---

## `serialize_report_value(value)`

Converts non-JSON-native values into JSON-safe strings.

Currently supports:

| Python Type | JSON Output |
|---|---|
| `date` | ISO date string |
| `datetime` | ISO datetime string |
| `set` | Sorted string representation |

---

# Output Folder Handling

The exporter automatically creates missing output folders.

Example:

```text
data/processed/reports/quality_report.json
```

If `reports/` does not exist, it is created.

---

# Example Input

```python
{
    "table_name": "customers",
    "row_count": 100,
    "generated_at": datetime(2026, 1, 31, 14, 30),
}
```

---

# Example Output

```json
{
    "table_name": "customers",
    "row_count": 100,
    "generated_at": "2026-01-31 14:30:00"
}
```

---

# Important Design Rule

Exporters only serialize data.

They must not:

- clean values
- validate rules
- infer schema
- modify reports
- modify tables

---

# Pipeline Position

Recommended workflow:

```text
Parse
→ Clean
→ Infer Types
→ Type Casting
→ Schema Metadata
→ Analysis
→ Validation
→ Report Generation
→ Report Export
→ Data Export
```

---

# Developer Notes

This exporter uses only the Python standard library:

```python
json
pathlib
datetime
```

No external dependency is needed.

---

# Current Limitations

Current implementation does not yet support:

- Markdown reports
- HTML reports
- CSV issue reports
- compressed reports
- report schemas
- timestamped report naming

---

# Future Improvements

Possible future additions:

- Markdown report exporter
- HTML summary exporter
- validation issue CSV export
- combined report bundle
- report schema validation
- automatic timestamped output names