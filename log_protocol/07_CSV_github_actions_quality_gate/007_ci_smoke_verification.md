# Protocol — Stage G CI Smoke Verification

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/07_CSV_github_actions_quality_gate.md` |
| Stage | Stage G — CI Smoke Verification |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Protocol documentation |

---

## Purpose

Document how to verify the first GitHub Actions workflow run after pushing or opening a pull request.

---

## Workflow To Check

```text
Codex Checks
```

---

## Expected Job

```text
Python quality checks
```

---

## Expected Steps

```text
Checkout repository
Set up Python
Install dependencies
Run Ruff
Run Black check
Run tests
```

---

## Verification Instructions

After this branch is pushed or a pull request is opened:

```text
1. Open the repository on GitHub.
2. Go to the Actions tab.
3. Select Codex Checks.
4. Open the latest run.
5. Confirm all steps pass.
```

For pull requests:

```text
1. Open the pull request.
2. Review the checks section.
3. Confirm Codex Checks is successful before merging.
```

---

## Status

GitHub Actions result is not verified by the assistant in this environment.

The user should verify the first workflow run on GitHub.
