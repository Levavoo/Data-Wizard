# Protocol — Stage B Regression Test Confirmation

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/01_CSV_ambiguous_null_token_decision.md` |
| Stage | Stage B — Regression Test Confirmation |
| Branch | `codex` |
| Status | Confirmed |
| Commit Scope | Regression confirmation protocol |

---

## 1. Purpose

Confirm that ambiguous null-like tokens remain preserved by default.

---

## 2. Confirmed Behavior

Current expected behavior:

```text
unknown → "unknown"
missing → "missing"
```

---

## 3. Existing Test Coverage

The behavior is already covered in:

```text
tests/test_nulls.py
```

Relevant test:

```python
def test_preserve_ambiguous_null_like_values() -> None:
    assert normalize_null("unknown") == "unknown"
    assert normalize_null("missing") == "missing"
```

---

## 4. Changed Files

| File | Action | Reason |
|---|---|---|
| `log_protocol/01_CSV_ambiguous_null_token_decision/002_regression_test_confirmation.md` | Created | Records regression confirmation. |

---

## 5. Production Code Decision

No production code change was required.

No test code change was required because regression coverage already exists.

---

## 6. Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_nulls.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```

---

## 7. Next Step

Continue with future configurable policy design only after review:

```text
Stage C — Future Configurable Policy Draft
```
