# CSV GitHub Actions Quality Gate Plan

## Status

```text
Draft — not active until user confirmation.
```

This plan focuses on adding automated GitHub quality checks for the CSV pipeline project.

The first implementation should be a soft gate.

---

## Purpose

Automatically run project checks when code is pushed to `codex` or opened as a pull request into `master`.

Goal:

```text
push to codex
or PR into master
→ GitHub Actions runs checks
→ developer sees pass/fail status
→ manual merge decision stays with user
```

---

## Gate Policy

Initial policy:

```text
soft gate
```

Meaning:

```text
checks run automatically
failures are visible on GitHub
merge is not blocked by branch protection yet
```

Reason:

```text
verify workflow stability before enforcing hard branch protection
```

Future policy:

```text
hard gate
```

Only after the workflow is stable.

---

## Problem

Currently, quality checks depend on manual local execution.

Current risks:

```text
developer forgets to run tests
PR is merged before tests run
format/lint errors are discovered late
local environment differs from GitHub environment
```

Expected result:

```text
GitHub automatically runs pytest/ruff/format checks
PRs clearly show whether checks pass
local commands match CI commands
```

---

## Architectural Layer

This plan belongs mainly to:

```text
Developer Workflow Layer
CI/CD Layer
Quality Assurance Layer
```

Main module areas:

```text
.github/workflows/
docs/development/
log_protocol/
```

Rules:

```text
CI checks should not change code.
CI checks should be deterministic.
CI checks should match local commands.
CI should start soft before becoming required.
Do not enable branch protection automatically in this plan.
```

---

# Stage A — Current Tooling Review

## Goal

Review current project tooling for tests, linting, formatting, and dependencies.

Expected files to inspect:

```text
pyproject.toml
requirements.txt
tests/
scripts/
```

## Expected Files

```text
docs/development/current_quality_tooling.md
log_protocol/07_CSV_github_actions_quality_gate/001_current_tooling_review.md
```

## Acceptance Criteria

- Current test command is documented.
- Current lint command is documented if available.
- Current format command is documented if available.
- Dependency installation command is documented.
- Missing tooling is documented without forcing unrelated setup.

---

# Stage B — GitHub Actions Workflow Design

## Goal

Design the first soft-gate GitHub Actions workflow.

Recommended workflow file:

```text
.github/workflows/codex_checks.yml
```

Recommended triggers:

```yaml
on:
  push:
    branches:
      - codex
  pull_request:
    branches:
      - master
```

Recommended checks:

```text
install dependencies
run pytest
run ruff check if available
run black --check if available
```

## Expected Files

```text
docs/development/github_actions_quality_gate.md
log_protocol/07_CSV_github_actions_quality_gate/002_workflow_design.md
```

## Acceptance Criteria

- Trigger behavior is documented.
- Soft gate behavior is documented.
- Check commands are documented.
- Hard gate is explicitly deferred.

---

# Stage C — Add Soft-Gate Workflow

## Goal

Add the first GitHub Actions workflow file.

Expected files:

```text
.github/workflows/codex_checks.yml
.github/workflows/codex_checks.md
log_protocol/07_CSV_github_actions_quality_gate/003_soft_gate_workflow.md
```

## Acceptance Criteria

- Workflow runs on pushes to `codex`.
- Workflow runs on PRs targeting `master`.
- Workflow installs project dependencies.
- Workflow runs automated checks.
- Workflow does not enforce branch protection.
- Matching `.md` documentation exists.

---

# Stage D — Local Quality Command Guide

## Goal

Document the local equivalent of the CI checks.

Expected file:

```text
docs/development/local_quality_commands.md
```

Suggested commands:

```powershell
python -m pytest
ruff check .
black --check .
```

## Expected Files

```text
docs/development/local_quality_commands.md
log_protocol/07_CSV_github_actions_quality_gate/004_local_quality_command_guide.md
```

## Acceptance Criteria

- PowerShell-friendly commands are documented.
- Commands match GitHub Actions workflow as closely as possible.
- Troubleshooting notes are included.

---

# Stage E — Workflow Result Review Guide

## Goal

Document how to read GitHub Actions results.

Expected file:

```text
docs/development/read_github_actions_results.md
```

Guide should explain:

```text
where to find Actions tab
where to find PR checks
how to open failed jobs
how to read logs
how to rerun failed jobs
```

## Expected Files

```text
docs/development/read_github_actions_results.md
log_protocol/07_CSV_github_actions_quality_gate/005_workflow_result_review_guide.md
```

## Acceptance Criteria

- User can find workflow results on GitHub.
- User can identify failed test/lint/format steps.
- User can rerun workflow if needed.

---

# Stage F — Branch Protection Design Only

## Goal

Document future hard-gate branch protection settings without enabling them yet.

Suggested file:

```text
docs/development/branch_protection_policy.md
```

Recommended future settings:

```text
Require pull request before merging
Require status checks to pass
Require branch up to date before merging
Do not allow direct pushes to master
```

## Expected Files

```text
docs/development/branch_protection_policy.md
log_protocol/07_CSV_github_actions_quality_gate/006_branch_protection_design.md
```

## Acceptance Criteria

- Future hard gate policy is documented.
- It is clear that branch protection is not enabled in this stage.
- Manual merge remains allowed for now.

---

# Stage G — CI Smoke Verification

## Goal

Create a small protocol for verifying the first workflow run after pushing.

Expected files:

```text
log_protocol/07_CSV_github_actions_quality_gate/007_ci_smoke_verification.md
```

## Acceptance Criteria

- User is instructed to check GitHub Actions after push/PR.
- Expected workflow name is documented.
- Expected pass/fail meaning is documented.
- No claim is made that CI passed unless it is actually checked.

---

## Out Of Scope

This plan does not include:

```text
enabling branch protection automatically
auto-merge
auto-deploy
publishing packages
coverage upload
pre-commit hook installation
Docker setup
multi-version Python matrix unless explicitly approved
```

---

## Recommended Implementation Order

```text
Stage A — Current Tooling Review
Stage B — GitHub Actions Workflow Design
Stage C — Add Soft-Gate Workflow
Stage D — Local Quality Command Guide
Stage E — Workflow Result Review Guide
Stage F — Branch Protection Design Only
Stage G — CI Smoke Verification
```

---

## Required Protocol Folder

When active, use:

```text
log_protocol/07_CSV_github_actions_quality_gate/
```

Protocol files:

```text
001_current_tooling_review.md
002_workflow_design.md
003_soft_gate_workflow.md
004_local_quality_command_guide.md
005_workflow_result_review_guide.md
006_branch_protection_design.md
007_ci_smoke_verification.md
999_plan_completion.md
```

---

## Activation Rule

This plan is not active until the user explicitly confirms:

```text
Start 07_CSV_github_actions_quality_gate
```

Until then, continue only with the currently active confirmed plan.
