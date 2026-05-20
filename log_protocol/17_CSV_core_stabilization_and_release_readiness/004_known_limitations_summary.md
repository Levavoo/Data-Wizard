# Protocol — Stage D Known Limitations Summary

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md` |
| Stage | Stage D — Known Limitations Summary |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Release readiness documentation |

---

## Purpose

Create one release-facing limitations document.

---

## Document Added

```text
docs/release/csv_core_known_limitations.md
```

---

## Limitations Covered

```text
malformed quote diagnostics
multiline text preservation
leading-zero preservation
currency, percent, and text amounts
date ambiguity and Excel serial dates
locale-specific boolean tokens
spreadsheet injection safety
HTML-like text
extra field preservation
footer/summary row handling
non-streaming pipeline
large diagnostics
local-only performance metrics
unsupported JSON/Excel/GUI scope
```

---

## Release Claim Boundary

The document clearly separates safe claims from unsupported claims.

---

## Important Decision

No production code was changed in this stage.

Reason:

```text
Stage D is a release-facing limitations summary only
```

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/release/csv_core_known_limitations.md` | Created | Summarizes known CSV core limitations before release/merge. |
| `log_protocol/17_CSV_core_stabilization_and_release_readiness/004_known_limitations_summary.md` | Created | Records Stage D completion. |

---

## Next Stage

```text
Stage E — User Workflow Readiness Guide
```
