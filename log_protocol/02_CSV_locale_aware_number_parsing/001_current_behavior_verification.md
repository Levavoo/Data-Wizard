# Protocol — Stage A Current Behavior Verification

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/02_CSV_locale_aware_number_parsing.md` |
| Stage | Stage A — Current Behavior Verification |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Number tests defining desired US/EU behavior |

---

## Purpose

Verify and define expected behavior for US-style and European-style numeric strings.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_numbers.py` | Modified | Added US/EU number behavior tests. |
| `tests/test_numbers.md` | Modified later | Documents locale-aware test coverage. |

---

## Behavior Defined

```text
1,000.50 → 1000.5
1.000,50 → 1000.5
250,75 → 250.75
5.500,00 → 5500.0
```

---

## Production Code Decision

The verification exposed that production cleaner behavior needed locale-aware parsing support.

Implementation continued in Stage C.

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_numbers.py
```

Status:

```text
Not executed by assistant in this environment.
```
