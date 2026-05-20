# CSV Performance Metrics Format

## Purpose

This document defines the JSON metrics format produced by CSV performance tools.

Plan:

```text
docs/plan_stages/16_CSV_performance_layer.md
```

---

## Default Metrics Path

```text
data/performance/csv_performance_baseline.json
```

Generated metrics files are artifacts and should not be committed by default.

---

## Example

```json
{
  "scenario": "rows_10000_clean_json_html",
  "row_count": 10000,
  "column_count": 11,
  "input_file_size_bytes": 1234567,
  "output_file_size_bytes": 1200000,
  "runtime_seconds": 1.23,
  "rows_per_second": 8130.08,
  "pipeline_status": "completed_with_warnings",
  "outputs": {
    "clean_csv": true,
    "json_report": true,
    "html_report": true,
    "quarantine_exports": false
  },
  "artifact_sizes": {
    "json_report_bytes": 12345,
    "html_report_bytes": 45678,
    "quarantine_candidates_bytes": null,
    "quarantine_rows_bytes": null,
    "accepted_rows_bytes": null
  },
  "fixture": {
    "path": "data/performance/csv_performance_10000.csv",
    "requested_rows": 10000,
    "delimiter": ",",
    "bom": false,
    "dirty_every": 25
  }
}
```

---

## Top-Level Fields

| Field | Meaning |
|---|---|
| `scenario` | Human-readable scenario name |
| `row_count` | Parsed output table row count |
| `column_count` | Parsed output table column count |
| `input_file_size_bytes` | Source fixture file size |
| `output_file_size_bytes` | Clean CSV output file size |
| `runtime_seconds` | End-to-end pipeline runtime |
| `rows_per_second` | Parsed rows divided by runtime |
| `pipeline_status` | Pipeline status string |
| `outputs` | Output mode flags |
| `artifact_sizes` | Optional output artifact sizes |
| `fixture` | Fixture generation metadata |

---

## Output Flags

```json
{
  "clean_csv": true,
  "json_report": true,
  "html_report": false,
  "quarantine_exports": false
}
```

---

## Artifact Size Fields

Possible artifact size fields:

```text
json_report_bytes
html_report_bytes
quarantine_candidates_bytes
quarantine_rows_bytes
accepted_rows_bytes
```

Use `null` when the artifact was not generated.

---

## Interpretation Rule

Metrics are machine-dependent.

Compare results carefully using:

```text
same machine
same Python version
same fixture size
same output mode
same branch or commit range
```

---

## Future Extensions

Possible future fields:

```text
python_version
platform
commit_sha
peak_memory_mb
step_timings
constraint_count
quarantine_candidate_count
```

Adding fields should be backward-compatible.
