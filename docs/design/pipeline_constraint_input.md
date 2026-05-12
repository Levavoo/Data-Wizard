# Pipeline Constraint Input

## Purpose

This document defines how constraint validation is passed into the CSV pipeline.

---

## Decision

`run_csv_pipeline()` accepts optional `Constraint` objects.

Function shape:

```python
run_csv_pipeline(
    input_path=input_path,
    output_path=output_path,
    report_path=report_path,
    constraints=constraints,
)
```

---

## Backward Compatibility

`constraints` defaults to `None`.

Existing calls continue to work:

```python
run_csv_pipeline(input_path, output_path)
```

If no constraints are provided, validation results are empty.

---

## Execution Point

Constraints run after:

```text
cleaning
type inference
type-aware casting
schema metadata inference
```

This means validators see cleaned and cast values.

---

## Design Rule

The pipeline orchestrates validation but does not contain validation logic.

Actual validation remains in:

```text
data_processor/validators/constraints.py
```
