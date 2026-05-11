# Protocol — Stage A Conservative Null Token Expansion

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/01_CSV_extended_null_tokens.md` |
| Stage | Stage A — Conservative Null Token Expansion |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Null cleaner update, tests, documentation, protocol |

---

## 1. Purpose

Extend default null normalization with conservative null-like tokens commonly found in CSV migration files.

This reduces false string values in cleaned datasets and improves later type inference, casting, reporting, and validation.

---

## 2. Scope

### Included

- Added conservative null tokens to `NULL_VALUES`.
- Added unit tests for extended tokens.
- Added table-level tests for extended token cleanup.
- Added tests proving ambiguous tokens remain unchanged.
- Updated null cleaner documentation.
- Updated null test documentation.

### Not Included

- Did not add `unknown` as a default null token.
- Did not add `missing` as a default null token.
- Did not implement configurable null profiles.
- Did not implement null token statistics.
- Did not modify adapters, validators, profilers, or exporters.

---

## 3. Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/cleaners/nulls.py` | Modified | Added conservative null tokens. |
| `data_processor/cleaners/nulls.md` | Modified | Documented extended null tokens and ambiguous-token policy. |
| `tests/test_nulls.py` | Modified | Added extended token tests and ambiguity preservation tests. |
| `tests/test_nulls.md` | Modified | Documented extended null token tests. |
| `log_protocol/01_CSV_extended_null_tokens/001_conservative_null_tokens.md` | Created | Records Stage A completion. |

---

## 4. Architecture Rules Checked

| Rule | Status | Notes |
|---|---|---|
| Adapters only parse formats | Passed | No adapter changes. |
| Cleaning modules are format-independent | Passed | Null token handling remains in cleaner layer. |
| All formats convert into `Table` | Not affected | No model change. |
| Profilers analyze only | Not affected | No profiler change. |
| Validators validate only | Not affected | No validator change. |
| Exporters only serialize | Not affected | No exporter change. |
| Documentation updated | Passed | Cleaner and test docs updated. |
| Isolated stage development | Passed | Only Stage A was implemented. |

---

## 5. Behavior Before

```text
#N/A          remained a string
NIL           remained a string
--            remained a string
?             remained a string
not available remained a string
not_applicable remained a string
```

---

## 6. Behavior After

```text
#N/A           → None
NIL            → None
--             → None
?              → None
not available  → None
not_applicable → None
```

Matching remains:

```text
case-insensitive
whitespace-trimmed
```

---

## 7. Ambiguous Token Decision

The following tokens remain unchanged by default:

```text
unknown
missing
```

Reason:

```text
They may be missing-value placeholders in some datasets, but legitimate category values in others.
```

They should be handled later through configurable cleaning profiles or column-specific null rules.

---

## 8. Tests / Checks

Recommended local commands:

```bash
python -m pytest tests/test_nulls.py
python -m pytest
```

Status:

```text
Not executed by assistant in this environment.
```

---

## 9. Risks / Notes

- The added tokens are conservative but still affect cleaned output if users expected these exact strings to remain as values.
- `?` is now treated as null globally.
- Ambiguous tokens are intentionally deferred.

---

## 10. Next Step

Continue with the next active-plan stage only after review:

```text
Stage B — Ambiguous Null Token Decision
```
