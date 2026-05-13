# quarantine_json_exporter.py

## Purpose

`quarantine_json_exporter.py` writes the `quarantine_candidates` report section to a dedicated JSON file.

It belongs to the exporter layer.

Architecture:

```text
quarantine_candidates report data
→ quarantine JSON exporter
→ quarantine_candidates.json
```

---

## Main Function

### `export_quarantine_candidates_to_json(quarantine_candidates, output_path, encoding="utf-8")`

Writes quarantine candidate report data to a UTF-8 JSON file.

---

## Behavior

The exporter:

```text
creates parent directories
writes indented UTF-8 JSON
preserves candidate report structure
serializes date/datetime values safely
```

---

## Design Rules

This module must not:

- mutate candidate data
- select rows
- export CSV
- change diagnostic meaning

Row selection belongs to quarantine row selection utilities.
