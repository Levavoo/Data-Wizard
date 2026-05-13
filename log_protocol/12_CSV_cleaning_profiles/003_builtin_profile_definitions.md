# Protocol — Stage C Built-In Profile Definitions

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/12_CSV_cleaning_profiles.md` |
| Stage | Stage C — Built-In Profile Definitions |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Config module, tests, documentation |

---

## Purpose

Define initial built-in profiles as plain data.

---

## Profiles Added

```text
default
light_touch
migration_audit
strict_crm
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `data_processor/config/cleaning_profiles.py` | Created | Adds built-in cleaning profiles. |
| `data_processor/config/cleaning_profiles.md` | Created | Documents profile definitions. |
| `tests/test_cleaning_profiles.py` | Created | Tests profile definitions. |
| `tests/test_cleaning_profiles.md` | Created | Documents profile tests. |
| `log_protocol/12_CSV_cleaning_profiles/003_builtin_profile_definitions.md` | Created | Records Stage C completion. |

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cleaning_profiles.py
```

Status:

```text
Not executed by assistant in this environment.
```
