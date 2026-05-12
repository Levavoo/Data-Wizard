# GitHub Actions Quality Gate

## Purpose

This document describes the first automated quality gate for the project.

The goal is to make test, lint, and format status visible on GitHub.

---

## Current Policy

```text
soft gate
```

Soft gate means:

```text
checks run automatically
results are visible on GitHub
merge is not blocked by branch protection yet
```

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

The workflow runs on:

```text
push to codex
pull_request targeting master
```

---

## Checks

The workflow runs:

```text
ruff check .
black --check .
python -m pytest
```

---

## Why Soft Gate First

Soft gate is safer during initial CI setup.

It allows the workflow to be tested without blocking development.

After the workflow is stable, branch protection can be enabled separately.

---

## Recommended Merge Rule

Even before hard branch protection is enabled:

```text
do not merge into master if CI fails
```

unless the failure is understood and intentionally accepted.

---

## Future Hard Gate

Future hard gate should require status checks to pass before merging into `master`.

This is intentionally not enabled by this stage.
