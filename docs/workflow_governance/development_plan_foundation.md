# Development Plan — Foundation Architecture

## Goal

Build a format-independent canonical data cleaning and migration engine.

Core principle:

```text
many input formats
→ one canonical model
→ shared processing engine
→ many outputs
```

---

# Current Status

## Completed

### Stage 01 — Canonical Core Models

Completed:

- Table
- Schema
- Column

Files:

```text
data_processor/core/
```

---

### Stage 02 — CSV Adapter

Completed:

- CSV parsing
- UTF-8 handling
- header normalization
- row normalization
- internal Table conversion

Files:

```text
data_processor/adapters/
```

---

### Stage 03 — Cleaning Foundation

Completed:

- null normalization
- text normalization
- boolean normalization
- numeric normalization
- date normalization

Files:

```text
data_processor/cleaners/
```

---

### Stage 04 — Type Inference

Completed:

- column type inference
- schema metadata inference

Files:

```text
data_processor/inference/
```

---

### Stage 05 — Type-Aware Casting

Completed:

- schema-driven casting
- type-aware cleaning
- prevention of incorrect cleaner application

Files:

```text
data_processor/cleaners/type_caster.py
```

---

### Stage 06 — Quality Reporting

Completed:

- duplicate detection
- missing values
- empty columns
- high-null columns

Files:

```text
data_processor/validators/
```

---

### Stage 07 — CSV Export

Completed:

- UTF-8 CSV export
- schema-preserving export
- serialization layer

Files:

```text
data_processor/exporters/
```

---

### Stage 08 — Pipeline Orchestration

Completed:

- full CSV workflow
- CLI execution
- manual execution support

Files:

```text
data_processor/core/pipeline.py
scripts/run_csv_pipeline.py
```

---

### Stage 09 — Analysis Layer

Completed:

- column profiling
- row profiling

Files:

```text
data_processor/analysis/
```

---

# Current Architecture

```text
Input File
↓
Adapter
↓
Canonical Table
↓
Cleaning
↓
Type Inference
↓
Type-Aware Casting
↓
Schema Metadata
↓
Analysis
↓
Validation
↓
Export
```

---

# Next Planned Stages

## Stage 10 — Constraint Engine

Goal:

```text
generic reusable validation rules
```

Planned:

- required constraints
- uniqueness constraints
- min/max validation
- allowed values
- regex validation

Files:

```text
data_processor/validators/constraints.py
```

---

## Stage 11 — Validation Reports

Goal:

```text
structured validation errors
```

Planned:

- row-level violations
- column-level violations
- severity levels
- quarantine candidates

---

## Stage 12 — Transformation Engine

Goal:

```text
controlled dataset reshaping
```

Planned:

- rename columns
- select/drop columns
- filtering
- sorting
- split/combine
- aggregation

---

## Stage 13 — Cleaning Profiles

Goal:

```text
configurable reusable cleaning pipelines
```

Examples:

```text
strict financial profile
CRM migration profile
ERP import profile
```

---

## Stage 14 — Excel Adapter

Goal:

```text
Excel → Table
```

Planned:

- sheet selection
- header detection
- merged-cell handling
- XLSX support

---

## Stage 15 — JSON Adapter

Goal:

```text
JSON → Table
```

Planned:

- flattening
- nested arrays
- object normalization

---

## Stage 16 — Encoding & Robust Parsing

Goal:

```text
handle hostile migration files
```

Planned:

- encoding detection
- delimiter detection
- malformed row handling
- tolerant parsing
- repair strategies

---

## Stage 17 — Report Export

Goal:

```text
machine-readable diagnostics
```

Planned:

- JSON reports
- HTML reports
- CSV issue exports

---

## Stage 18 — Performance Layer

Goal:

```text
large dataset handling
```

Planned:

- streaming
- chunking
- lazy loading
- parallel processing

---

# Architectural Rules

## Rule 01

Adapters only parse formats.

They must not clean data.

---

## Rule 02

Cleaning modules must be format-independent.

---

## Rule 03

All formats convert into:

```text
Table
```

---

## Rule 04

Profilers analyze only.

Never modify data.

---

## Rule 05

Validators validate only.

Never modify data.

---

## Rule 06

Exporters only serialize data.

---

## Rule 07

All new code files require matching `.md` documentation files.

---

## Rule 08

Development proceeds in isolated stages.

Avoid parallel feature expansion.

---

# Long-Term Vision

```text
Enterprise-grade migration & cleaning engine
```

Target capabilities:

- CSV
- Excel
- JSON
- SQL
- APIs
- Parquet
- Arrow
- validation pipelines
- migration diagnostics
- rule engines
- audit reporting
- schema evolution
- canonical transformations
- 