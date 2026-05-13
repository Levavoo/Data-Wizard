# Read GitHub Actions Results

## Purpose

This guide explains how to check GitHub Actions results after pushing to `codex` or opening a pull request.

---

## Where To Find Results

Open the repository on GitHub.

Use either:

```text
Actions tab
```

or the checks section inside a pull request.

---

## Workflow Name

Look for:

```text
Codex Checks
```

---

## When It Runs

The workflow runs when:

```text
code is pushed to codex
a pull request targets master
```

---

## How To Read A Successful Run

A successful run means:

```text
Ruff passed
Black check passed
pytest passed
```

---

## How To Read A Failed Run

Open the failed workflow run.

Then open the failed job:

```text
Python quality checks
```

Look for the failed step:

```text
Run Ruff
Run Black check
Run tests
```

---

## Common Failures

### Ruff failure

Usually a linting problem.

Fix the reported file and line number.

---

### Black failure

Usually formatting.

Run locally:

```powershell
black .
```

---

### Pytest failure

A test failed.

Run locally:

```powershell
python -m pytest
```

For focused debugging, run the failing test file only.

---

## Rerun Failed Jobs

On GitHub, open the failed workflow run and choose:

```text
Re-run jobs
```

Use this after pushing a fix or when the failure was temporary.

---

## Soft Gate Reminder

This workflow is currently a soft gate.

That means GitHub shows pass/fail results, but branch protection does not block merge yet.

Recommended manual policy:

```text
Do not merge into master when checks fail.
```
