CSV file
→ CsvAdapter
→ Table
→ inspect output

New-Item examples\sample_dirty.csv

New-Item tests\test_csv_adapter.py
New-Item tests\test_csv_adapter.md

examples/sample_dirty.csv
 Customer ID , Name , Country , Active 
1,Alice,Germany,YES
2,Bob, France ,no
3,Charlie,,TRUE
4,,Germany,false

Purpose:

whitespace issues
mixed booleans
empty values
inconsistent formatting

# What Happened When Running `pytest`

Command executed:

```powershell
pytest
```

---

# Purpose of Pytest

`pytest` is the automated testing framework used in this project.

It:

- finds test files
- imports project modules
- runs test functions
- checks assertions
- reports failures or success

---

# Initial Failure

First result:

```text
ModuleNotFoundError: No module named 'data_processor'
```

This happened during test collection.

---

# What "Test Collection" Means

Before running tests, pytest first searches for:

```text
tests/
test_*.py
*_test.py
```

In this project:

```text
tests/test_csv_adapter.py
```

was discovered automatically.

Pytest then tried to import:

```python
from data_processor.adapters.csv_adapter import CsvAdapter
```

---

# Why Import Failed

Python could not find:

```text
data_processor
```

because the project root directory was not automatically added to Python's import path.

Python internally uses:

```python
sys.path
```

to determine where modules can be imported from.

The project root was missing from that path.

---

# Fix Applied

Added to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

---

# Meaning of `pythonpath = ["."]`

This tells pytest:

```text
add current project root directory
to Python import search path
```

Now Python can resolve:

```python
data_processor.adapters.csv_adapter
```

correctly.

---

# Meaning of `testpaths = ["tests"]`

This tells pytest:

```text
only search for tests inside:
tests/
```

Benefits:

- cleaner test discovery
- faster test collection
- avoids accidental test detection elsewhere

---

# What Happened After Fix

Pytest successfully:

1. discovered test files
2. imported project modules
3. executed test functions
4. evaluated assertions

Result:

```text
5 passed
```

---

# What Each Test Verified

## `test_csv_adapter_returns_table`

Verified:

```text
CsvAdapter.read()
returns a Table object
```

---

## `test_csv_adapter_row_count`

Verified:

```text
all CSV rows were parsed
```

Expected:

```text
4 rows
```

---

## `test_csv_adapter_column_count`

Verified:

```text
schema columns were created correctly
```

Expected:

```text
4 columns
```

---

## `test_csv_adapter_normalized_headers`

Verified header normalization logic:

```text
trim whitespace
lowercase
spaces → underscores
```

Example:

```text
" Customer ID "
→ "customer_id"
```

---

## `test_csv_adapter_preserves_raw_values`

Verified:

```text
values remain raw strings
```

Important architectural rule:

No cleaning or type inference happens inside adapters.

Example:

```text
"YES"
stays
"YES"

not:
True
```

---

# Architectural Importance

The successful tests confirmed:

```text
CSV File
→ CsvAdapter
→ Schema
→ Table
→ Rows
```

works correctly.

This validates the first complete ingestion slice of the architecture.

---

# Why Testing Early Matters

Testing early prevents:

- hidden architecture problems
- broken imports
- inconsistent interfaces
- silent parsing issues

The earlier problems are detected, the cheaper they are to fix.

---

# Current Verified Components

Verified working:

```text
Column
Schema
Table
BaseAdapter
CsvAdapter
CSV parsing
Header normalization
Internal row storage
Pytest configuration
```

---

# Current Architecture Status

Working flow:

```text
CSV File
→ Adapter Layer
→ Canonical Internal Table Model
```

Next stages will add:

```text
Type inference
→ Cleaning
→ Validation
→ Transformation
→ Export
```