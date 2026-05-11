# Protocol — Stage A Ambiguous Token Policy Decision

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/01_CSV_ambiguous_null_token_decision.md` |
| Stage | Stage A — Ambiguous Token Policy Decision |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Design documentation and policy decision |

---

## 1. Purpose

Document the default policy for ambiguous null-like values such as `unknown` and `missing`.

---

## 2. Decision

The default cleaner preserves ambiguous tokens.

```text
unknown → "unknown"
missing → "missing"
```

They are not added to global `NULL_VALUES`.

---

## 3. Reason

These values may mean missing data in some datasets, but they may also be meaningful categories.

Changing them globally to `None` could cause silent data loss.

---

## 4. Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/design/ambiguous_null_tokens.md` | Created | Documents ambiguous token policy. |
| `log_protocol/01_CSV_ambiguous_null_token_decision/001_ambiguous_token_policy.md` | Created | Records policy decision. |

---

## 5. Architecture Rules Checked

| Rule | Status | Notes |
|---|---|---|
| Adapters only parse formats | Passed | No adapter changes. |
| Cleaning modules are format-independent | Passed | No cleaner change needed. |
| Validators validate only | Not affected | No validator changes. |
| Profilers analyze only | Not affected | No profiler changes. |
| Isolated stage development | Passed | Only policy documentation was added. |

---

## 6. Production Code Decision

No production code change was required.

The current implementation already preserves `unknown` and `missing` by default.

---

## 7. Next Step

Continue with regression confirmation:

```text
Stage B — Regression Test Confirmation
```
