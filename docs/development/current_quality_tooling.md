# Current Quality Tooling

## Purpose

This document summarizes the current quality tools used by the project.

---

## Tool Configuration

Main configuration file:

```text
pyproject.toml
```

Configured tools:

```text
pytest
black
isort
ruff
```

---

## Dependencies

Main dependency file:

```text
requirements.txt
```

Install command:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Test Command

```powershell
python -m pytest
```

Runs tests from:

```text
tests/
```

---

## Ruff Command

```powershell
ruff check .
```

Checks Python linting rules.

---

## Black Check Command

```powershell
black --check .
```

Checks formatting without changing files.

---

## Format Command

To format files locally:

```powershell
black .
```

---

## Current CI Decision

The first GitHub Actions quality gate uses:

```text
ruff check .
black --check .
python -m pytest
```

It does not run `isort` yet.

Reason:

```text
start with the simplest stable soft gate first
```
