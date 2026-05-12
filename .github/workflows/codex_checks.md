# codex_checks.yml

## Purpose

This workflow runs automatic quality checks for the `codex` branch and pull requests into `master`.

It is a soft gate.

That means checks are visible on GitHub, but branch protection is not enforced by this workflow alone.

---

## Workflow File

```text
.github/workflows/codex_checks.yml
```

---

## Workflow Name

```text
Codex Checks
```

---

## Triggers

Runs on pushes to:

```text
codex
```

Runs on pull requests targeting:

```text
master
```

---

## Checks

The workflow runs:

```text
pip install -r requirements.txt
ruff check .
black --check .
python -m pytest
```

---

## Python Version

```text
3.12
```

---

## Soft Gate Meaning

Soft gate means:

```text
checks run automatically
failures are visible
merge is still manually controlled
branch protection is not enabled automatically
```

---

## When To Use Results

Before merging a PR into `master`, review the workflow result.

Recommended rule:

```text
Do not merge if checks fail, unless the failure is understood and intentionally accepted.
```

---

## Local Equivalent

Run locally:

```powershell
ruff check .
black --check .
python -m pytest
```
