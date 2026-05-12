# Branch Protection Policy

## Purpose

This document describes the future hard-gate policy for protecting `master`.

This stage does not enable branch protection automatically.

---

## Current Policy

Current policy:

```text
soft gate
```

Meaning:

```text
GitHub Actions checks run
results are visible
manual merge is still possible
```

---

## Future Hard Gate

After the workflow is stable, protect `master` with these settings:

```text
Require a pull request before merging
Require status checks to pass before merging
Require branches to be up to date before merging
Do not allow direct pushes to master
```

---

## Required Check

Recommended required check:

```text
Codex Checks / Python quality checks
```

Exact check name may need to be confirmed in GitHub after the first workflow run.

---

## Why Not Enable Hard Gate Immediately

The workflow should first prove it runs reliably on GitHub.

Reasons:

```text
dependency installation may fail
formatting expectations may need adjustment
workflow permissions may need adjustment
check names must be confirmed
```

---

## Recommended Manual Policy Now

Until branch protection is enabled:

```text
Only merge PRs into master after checks pass.
```

---

## Future Setup Location

GitHub UI path:

```text
Repository Settings
→ Branches
→ Branch protection rules
→ Add rule
```

Branch name pattern:

```text
master
```
