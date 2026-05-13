# Protocol — Stage E CLI Profile Option

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/12_CSV_cleaning_profiles.md` |
| Stage | Stage E — CLI Profile Option |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | CLI integration, tests, documentation |

---

## Purpose

Add CLI support for selecting a built-in profile.

---

## CLI Options Added

```text
--profile
--no-strict
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `scripts/run_csv_pipeline.py` | Modified | Adds profile resolution and strict override behavior. |
| `scripts/run_csv_pipeline.md` | Modified | Documents profile usage and override behavior. |
| `tests/test_cli_cleaning_profiles.py` | Created | Tests CLI profile behavior. |
| `tests/test_cli_cleaning_profiles.md` | Created | Documents CLI profile tests. |
| `log_protocol/12_CSV_cleaning_profiles/005_cli_profile_option.md` | Created | Records Stage E completion. |

---

## Behavior Added

```text
--profile selects a built-in profile
strict_crm enables strict mode by default
--no-strict disables strict mode from strict profiles
--strict enables strict mode for non-strict profiles
no-profile behavior remains non-strict by default
```

---

## Tests / Checks

Recommended local command:

```bash
python -m pytest tests/test_cli_cleaning_profiles.py
```

Status:

```text
Not executed by assistant in this environment.
```
