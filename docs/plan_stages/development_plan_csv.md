# CSV-Focused Development Plan

## Development Rule

Every code file must have a matching documentation file.

Example:

```text
data_processor/core/table.py
data_processor/core/table.md
```

Each `.md` file should explain:

- purpose of the file
- main classes/functions
- input/output behavior
- developer notes
- future improvements

---

# Stage 01 — Core Internal Model

Goal:

Create the canonical table structure used by all formats.

Files:

```text
data_processor/core/table.py
data_processor/core/table.md

data_processor/core/column.py
data_processor/core/column.md

data_processor/core/schema.py
data_processor/core/schema.md
```

Purpose:

- represent rows and columns
- store metadata
- prepare for schema/type inference

---

# Stage 02 — CSV Adapter

Goal:

Read CSV files and convert them into the internal `Table`.

Files:

```text
data_processor/adapters/csv_adapter.py
data_processor/adapters/csv_adapter.md
```

Responsibilities:

- check file exists
- detect encoding fallback
- read CSV safely
- detect delimiter
- parse rows
- return `Table`

Not responsible for:

- cleaning values
- validating business rules
- exporting data

---

# Stage 03 — Basic Type Inference

Goal:

Detect simple column types.

Files:

```text
data_processor/inference/type_inference.py
data_processor/inference/type_inference.md
```

Initial supported types:

```text
string
integer
float
boolean
date
datetime
null
```

---

# Stage 04 — Basic Value Cleaners

Goal:

Clean common dirty CSV values.

Files:

```text
data_processor/cleaners/nulls.py
data_processor/cleaners/nulls.md

data_processor/cleaners/text.py
data_processor/cleaners/text.md

data_processor/cleaners/numbers.py
data_processor/cleaners/numbers.md

data_processor/cleaners/booleans.py
data_processor/cleaners/booleans.md

data_processor/cleaners/dates.py
data_processor/cleaners/dates.md
```

Initial cleaning tasks:

- trim whitespace
- normalize empty/null values
- normalize booleans
- parse simple numbers
- parse common date formats
- standardize text casing later

---

# Stage 05 — Schema Inference

Goal:

Create a simple inferred schema from the table.

Files:

```text
data_processor/inference/schema_inference.py
data_processor/inference/schema_inference.md
```

Schema should include:

- column name
- inferred type
- nullable true/false
- sample values
- missing count
- unique count

---

# Stage 06 — Validation

Goal:

Generate basic quality checks.

Files:

```text
data_processor/validators/quality_report.py
data_processor/validators/quality_report.md

data_processor/validators/constraint_validator.py
data_processor/validators/constraint_validator.md
```

Initial checks:

- missing values
- duplicate rows
- invalid type values
- empty columns
- high-null columns

---

# Stage 07 — CSV Exporter

Goal:

Write cleaned internal `Table` back to CSV.

Files:

```text
data_processor/exporters/csv_exporter.py
data_processor/exporters/csv_exporter.md
```

Responsibilities:

- write headers
- write rows
- use UTF-8
- preserve cleaned values

---

# Stage 08 — Cleaning Pipeline

Goal:

Connect everything into one simple flow.

Files:

```text
data_processor/core/pipeline.py
data_processor/core/pipeline.md
```

Pipeline:

```text
CSV file
→ csv_adapter
→ Table
→ clean values
→ infer schema
→ validate
→ export cleaned CSV
→ create report
```

---

# Stage 09 — First CLI Script

Goal:

Run the pipeline from PowerShell.

Files:

```text
scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md
```

Example command:

```powershell
python scripts\run_csv_pipeline.py data\raw\sample.csv data\processed\cleaned.csv
```

---

# Stage 10 — Tests

Goal:

Add tests for each module.

Files:

```text
tests/test_table.py
tests/test_table.md

tests/test_csv_adapter.py
tests/test_csv_adapter.md

tests/test_type_inference.py
tests/test_type_inference.md

tests/test_cleaners.py
tests/test_cleaners.md
```

Testing rule:

Every important module should have at least one test file.

---

# Recommended First Implementation Order

Do not build everything at once.

Recommended order:

```text
1. table.py + table.md
2. column.py + column.md
3. csv_adapter.py + csv_adapter.md
4. sample_dirty.csv
5. test_csv_adapter.py + test_csv_adapter.md
6. nulls.py + nulls.md
7. text.py + text.md
8. type_inference.py + type_inference.md
9. csv_exporter.py + csv_exporter.md
10. pipeline.py + pipeline.md
11. run_csv_pipeline.py + run_csv_pipeline.md
```

---

# Development Principle

Build one small working slice first:

```text
Read CSV → Table → Export CSV
```

Then expand:

```text
Read CSV → Table → Clean → Infer Schema → Validate → Export
```

This keeps the project stable, testable, and understandable.