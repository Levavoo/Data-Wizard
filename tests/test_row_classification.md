# test_row_classification.py

## Purpose

Tests suspicious row classification behavior.

These tests verify that row classification detects suspicious rows without mutating or removing data.

---

## Tested File

```text
data_processor/analysis/row_classification.py
```

---

## Covered Behavior

- empty row classification
- comment row classification
- summary row classification
- footer row classification
- garbage row classification
- normal row preservation
- table-level suspicious row summary

---

## Example

Input rows:

```text
1,100
TOTAL,100
End of export,
```

Expected summary:

```text
normal_row: 1
summary_row: 1
footer_row: 1
```

---

## Run Tests

```bash
python -m pytest tests/test_row_classification.py
```

---

## Design Rule

Row classification is diagnostic-only.

It must not remove rows, quarantine rows, modify values, or change exports.
