# Project Dependencies

This document explains the Python packages installed in the virtual environment.

---

# Direct Development Dependencies

These are tools intentionally installed for development.

---

## black==26.3.1

`black` is a Python code formatter.

Purpose:

- Automatically formats Python code
- Keeps code style consistent
- Reduces manual formatting decisions

Common command:

```powershell
black .
```

---

## isort==8.0.1

`isort` sorts Python imports.

Purpose:

- Groups imports cleanly
- Sorts imports alphabetically
- Keeps import sections readable

Common command:

```powershell
isort .
```

---

## pytest==9.0.3

`pytest` is the testing framework.

Purpose:

- Runs automated tests
- Helps verify that cleaning logic works correctly
- Prevents old functionality from breaking

Common command:

```powershell
pytest
```

---

## ruff==0.15.12

`ruff` is a fast Python linter.

Purpose:

- Finds style problems
- Finds common bugs
- Can replace many older linting tools

Common command:

```powershell
ruff check .
```

---

# Indirect Dependencies

These were installed because the main tools need them.

---

## click==8.3.3

Command-line utility library.

Used by tools like `black`.

---

## colorama==0.4.6

Adds colored terminal output support on Windows.

Used by command-line tools.

---

## iniconfig==2.3.0

Reads `.ini` configuration files.

Used by `pytest`.

---

## mypy_extensions==1.1.0

Typing support package.

Used by tools that handle advanced Python type hints.

---

## packaging==26.2

Helps tools understand package versions and Python package metadata.

Used by many Python tools.

---

## pathspec==1.1.1

Handles file ignore patterns.

Used by tools like `black` to respect ignored files.

---

## platformdirs==4.9.6

Finds correct system-specific folders.

Used by tools for cache/config locations.

---

## pluggy==1.6.0

Plugin system used by `pytest`.

Allows pytest plugins and extensions.

---

## Pygments==2.20.0

Syntax highlighting library.

Used by pytest and other tools for readable terminal output.

---

## pytokens==0.4.1

Token parsing support for Python tooling.

Used internally by formatting/linting tools.

---

# Important Rule

Do not manually edit `requirements.txt` unless necessary.

Preferred workflow:

```powershell
pip install package-name
pip freeze > requirements.txt
```

---

# Current Development Commands

Run all checks before committing:

```powershell
ruff check .
black .
isort .
pytest
```

---

# Dependency Policy

Because this project may process sensitive data:

- Keep dependencies minimal
- Prefer Python standard library when reasonable
- Avoid cloud-based services
- Avoid packages that upload telemetry or data
- Review every new dependency before installing