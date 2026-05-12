# Local Quality Commands

## Purpose

This guide lists the local commands that match the GitHub Actions quality checks.

Run these before pushing to `codex` or opening a pull request.

---

## Install Dependencies

PowerShell:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Run All Tests

```powershell
python -m pytest
```

---

## Run Ruff

```powershell
ruff check .
```

---

## Run Black Check

```powershell
black --check .
```

This checks formatting but does not modify files.

---

## Auto-Format With Black

```powershell
black .
```

Run this if `black --check .` fails.

---

## Recommended Local Check Sequence

```powershell
ruff check .
black --check .
python -m pytest
```

---

## If Ruff Fails

Read the reported file and line number.

Fix the issue manually, then rerun:

```powershell
ruff check .
```

---

## If Black Check Fails

Run:

```powershell
black .
```

Then rerun:

```powershell
black --check .
```

---

## If Pytest Fails

Run a focused test first:

```powershell
python -m pytest tests\test_example_csv_workflow.py
```

Then rerun all tests:

```powershell
python -m pytest
```
