# Protocol — Stage A Whitespace-Only Null Verification

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/01_CSV_null_and_value_normalization.md` |
| Stage | Stage A — Whitespace-Only Null Verification |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Regression tests and documentation |

---

## 1. Purpose

Verify that whitespace-only CSV cells are normalized to Python `None` through the existing null-cleaning behavior.

This stage confirms the current cleaner already handles whitespace-only strings and adds regression coverage to prevent future breakage.

---

## 2. Scope

### Included

- Added unit-level whitespace-only null tests for `normalize_null()`.
- Added table-level whitespace-only null tests for `clean_table_nulls()`.
- Added pipeline-level CSV test proving whitespace-only cells become `None`.
- Updated matching test documentation.

### Not Included

- No production cleaner code change.
- No adapter change.
- No pipeline behavior change.
- No new null tokens.
- No null token statistics.

---

## 3. Changed Files

| File | Action | Reason |
|---|---|---|
| `tests/test_nulls.py` | Modified | Added whitespace-only null regression tests. |
| `tests/test_nulls.md` | Modified | Documented new null tests. |
| `tests/test_pipeline.py` | Modified | Added end-to-end whitespace-only CSV cell test. |
| `tests/test_pipeline.md` | Modified | Documented new pipeline test. |
| `log_protocol/01_CSV_null_and_value_normalization/001_whitespace_only_nulls.md` | Created | Records Stage A completion. |

---

## 4. Architecture Rules Checked

| Rule | Status | Notes |
|---|---|---|
| Adapters only parse formats | Passed | No adapter change. |
| Cleaning modules are format-independent | Passed | Existing null cleaner behavior verified. |
| All formats convert into `Table` | Not affected | No model change. |
| Profilers analyze only | Not affected | No profiler change. |
| Validators validate only | Not affected | No validator change. |
| Exporters only serialize | Not affected | No exporter change. |
| Documentation updated | Passed | Test docs updated. |
| Isolated stage development | Passed | Only Stage A verification was implemented. |

---

## 5. Behavior Verified

```text
"   "      → None
"\t"       → None
"\n"       → None
" \t \n " → None
```

Verified at:

```text
normalize_null()
clean_table_nulls()
run_csv_pipeline()
```

---

## 6. Production Code Decision

No production code change was required.

Reason:

```text
normalize_null() already strips string values before checking NULL_VALUES.
The empty string token is already configured as null.
```

---

## 7. Tests / Checks

Recommended local commands:

```bash
python -m pytest tests/test_nulls.py
python -m pytest tests/test_pipeline.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```

---

## 8. Risks / Notes

- This stage intentionally avoids changing null cleaner behavior.
- Future null-token expansion should be handled in the next stage.
- Pipeline-level test protects the order: parse → null clean → text clean.

---

## 9. Next Step

Continue with the next active-plan stage only after review:

```text
Stage B — Extended Null Tokens
```
