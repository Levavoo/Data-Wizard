# Protocol — Stage A Parse Diagnostics

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/00_CSV_improvements.md` |
| Stage | Stage A — Parse Diagnostics |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Parser diagnostics model, CSV integration, diagnostic bundle integration, tests, docs |

---

## 1. Purpose

Add structured parser diagnostics for CSV ingestion so parsing issues are reported without changing adapter responsibilities.

This stage addresses silent or unclear parser issues such as extra fields, short rows, empty headers, duplicate headers, shifted header rows, detected delimiter, and detected encoding.

---

## 2. Scope

### Included

- Added `ParseDiagnostics` model.
- Attached parser diagnostics to `Table.metadata["parse_diagnostics"]`.
- Added CSV row-width diagnostics for extra and missing fields.
- Added header diagnostics for empty and duplicated headers.
- Added parser warnings for shifted headers, empty headers, duplicate headers, extra fields, and missing fields.
- Exposed parser diagnostics as a top-level diagnostic bundle section.
- Added focused parser diagnostics tests.
- Added matching `.md` documentation for new test and code files.

### Not Included

- Suspicious row classification.
- Footer or summary row classification.
- Row quarantine.
- Header detection confidence scoring.
- Manual header row override.
- Data cleaning or value normalization.

---

## 3. Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/adapters/parse_diagnostics.py` | Created | Defines structured parser diagnostics. |
| `data_processor/adapters/parse_diagnostics.md` | Created | Documents parser diagnostics model. |
| `data_processor/adapters/csv_adapter.py` | Modified | Builds and attaches parser diagnostics. |
| `data_processor/adapters/csv_adapter.md` | Modified | Documents CSV parser diagnostics behavior. |
| `data_processor/reports/diagnostic_bundle.py` | Modified | Exposes parser diagnostics in report bundle. |
| `data_processor/reports/diagnostic_bundle.md` | Modified | Documents parser diagnostics report section. |
| `tests/test_parse_diagnostics.py` | Created | Adds parser diagnostics coverage. |
| `tests/test_parse_diagnostics.md` | Created | Documents parser diagnostics tests. |
| `log_protocol/00_CSV_improvements/001_parse_diagnostics.md` | Created | Records this stage implementation. |

---

## 4. Architecture Rules Checked

| Rule | Status | Notes |
|---|---|---|
| Adapters only parse formats | Passed | Diagnostics describe parser structure only. |
| Cleaning modules are format-independent | Passed | No cleaning logic added. |
| All formats convert into `Table` | Passed | CSV still outputs `Table`. |
| Profilers analyze only | Not affected | No profiler changes. |
| Validators validate only | Passed | No validator behavior added. |
| Exporters only serialize | Not affected | No exporter changes. |
| New code files require `.md` docs | Passed | `parse_diagnostics.md` added. |
| Isolated stage development | Passed | Only Stage A was implemented. |

---

## 5. Behavior Before

```text
Extra fields beyond headers were ignored silently.
Short rows became missing values but source row-width issues were not explicitly reported.
Duplicate and empty headers were normalized but not reported as parser diagnostics.
Diagnostic bundle had no top-level parse_diagnostics section.
```

---

## 6. Behavior After

```text
Table metadata includes parse_diagnostics.
Diagnostic bundle includes top-level parse_diagnostics.
Rows with extra fields are reported by source row index.
Rows with missing fields are reported by source row index.
Empty headers and duplicate headers are reported.
Parser warnings summarize important structural issues.
```

Example:

```python
{
    "rows_with_extra_fields": [3],
    "extra_field_count": 1,
    "rows_with_missing_fields": [2],
    "missing_field_count": 1,
    "duplicate_headers": ["name"],
    "empty_headers": [3]
}
```

---

## 7. Tests / Checks

Added tests in:

```text
tests/test_parse_diagnostics.py
```

Recommended local command:

```bash
python -m pytest tests/test_parse_diagnostics.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```

---

## 8. Risks / Notes

- Source row indexes in diagnostics are zero-based and refer to original source rows, including header and preamble rows.
- Extra fields are still ignored in canonical row data, but now reported.
- This stage does not classify garbage rows or footer rows; those remain future stages.

---

## 9. Next Step

Continue with the next active-plan stage only after review:

```text
Stage B — Whitespace-Only Null Handling
```
