# Protocol — Stage C Locale-Aware Number Normalization

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_locale_aware_number_parsing.md` |
| Stage | Stage C — Locale-Aware Number Normalization |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Cleaner, inference, tests, documentation |

---

## Purpose

Implement locale-aware number parsing for US-style and European-style numeric strings.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/cleaners/numbers.py` | Modified | Added `auto`, `us`, and `eu` parsing support. |
| `data_processor/cleaners/numbers.md` | Modified | Documented locale-aware number parsing. |
| `data_processor/inference/type_inference.py` | Modified | Reused locale-aware numeric preparation for inference. |
| `data_processor/inference/type_inference.md` | Modified | Documented locale-aware numeric inference. |
| `tests/test_numbers.py` | Modified | Added locale-aware number normalization tests. |
| `tests/test_type_inference.py` | Modified | Added EU-style float inference test. |
| `tests/test_numbers.md` | Modified | Documented number tests. |
| `tests/test_type_inference.md` | Modified | Documented inference tests. |

---

## Behavior After

```text
1,000.50 → 1000.5
1.000,50 → 1000.5
250,75 → 250.75
5.500,00 → 5500.0
```

---

## Architecture Rules Checked

| Rule | Status | Notes |
|---|---|---|
| Adapters only parse formats | Passed | No adapter changes. |
| Cleaning modules normalize values | Passed | Number parsing lives in cleaner. |
| Inference detects only | Passed | Inference uses cleaned representation only for detection. |
| Exporters only serialize | Not affected | No exporter changes. |

---

## Tests / Checks

Recommended local commands:

```bash
python -m pytest tests/test_numbers.py
python -m pytest tests/test_type_inference.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```
