# Current CSV Pipeline Performance Surface

## Purpose

This document records the current CSV pipeline stages and likely performance hotspots before adding measurement tooling.

Plan:

```text
docs/plan_stages/16_CSV_performance_layer.md
```

---

## Current Pipeline Flow

Current CSV pipeline flow:

```text
CsvAdapter.read()
→ clean_table_nulls()
→ clean_table_text()
→ infer_table_types()
→ cast_table_by_schema()
→ infer_table_types()
→ infer_schema_metadata()
→ validate_table_constraints()
→ generate_quality_report()
→ build_diagnostic_bundle()
→ build_pipeline_status()
→ export_table_to_csv()
→ optional JSON report export
→ optional HTML report export
→ optional quarantine candidate JSON export
→ optional quarantine rows CSV export
→ optional accepted rows CSV export
```

---

## Likely Runtime Hotspots

Potential runtime-heavy areas:

```text
CSV parsing and row list creation
row-by-row cleaning
number normalization
type inference over every value
type casting over every value
quality report calculation
row profile generation
row classification
mixed-type diagnostics
constraint validation
quarantine candidate generation
CSV export
large JSON report export
large HTML report rendering
```

---

## Likely Memory Hotspots

Potential memory-heavy areas:

```text
loading all CSV rows into memory
storing full Table rows in memory
building column profiles
building row profiles
building diagnostic bundle
building quarantine candidate list
rendering HTML report as one large string
exporting quarantine/accepted row split tables
```

---

## Output Modes Affect Performance

Different output modes should be measured separately:

```text
clean CSV only
clean CSV + JSON report
clean CSV + HTML report
clean CSV + quarantine exports
full output mode
```

Reason:

```text
reports and quarantine exports can be more expensive than basic cleaning
```

---

## Current Limitations

Current pipeline is not streaming.

Expected current behavior:

```text
input is read into memory
cleaned table is held in memory
reports are built in memory
exports are written after processing
```

This is acceptable for the current architecture but must be measured before optimization decisions.

---

## Performance Risk From Diagnostics

Diagnostics are valuable but can grow with row count.

Potential risks:

```text
row profiles for every row
validation failure details for many rows
quarantine candidates for many rows
HTML report rendering very large diagnostic sections
```

---

## Design Rule

Performance work should not reduce diagnostics silently.

If a future optimization limits diagnostics, it must be explicit and configurable.
