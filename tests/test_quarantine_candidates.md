# test_quarantine_candidates.py

## Purpose

Tests quarantine candidate report building.

These tests verify that existing diagnostics can be grouped into row-level review candidates.

---

## Tested File

```text
data_processor/reports/quarantine_candidates.py
```

---

## Covered Behavior

- validation failures create error candidates
- suspicious rows create warning candidates
- mixed-type invalid values create warning candidates
- multiple reasons are grouped by row index
- empty reports are returned when there are no reasons
- table rows are not mutated

---

## Run Tests

```bash
python -m pytest tests/test_quarantine_candidates.py
```

---

## Design Rule

Quarantine candidates are report-only.

They must not remove rows, mutate rows, block export, or write quarantine files.
