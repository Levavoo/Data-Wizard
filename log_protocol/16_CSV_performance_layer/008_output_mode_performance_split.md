# Protocol — Stage H Report Performance Split

## Metadata

| Field | Value |
|---|---|
| Plan | `docs/plan_stages/16_CSV_performance_layer.md` |
| Stage | Stage H — Report Performance Split |
| Branch | `codex` |
| Status | Implemented |
| Commit Scope | Output mode comparison script and documentation |

---

## Purpose

Measure the cost of different output modes.

---

## Files Added

```text
docs/performance/csv_output_mode_performance_scenarios.md
scripts/performance/run_csv_output_mode_comparison.py
scripts/performance/run_csv_output_mode_comparison.md
```

---

## Scenarios Supported

```text
clean_only
json_report
html_report
quarantine_exports
full_outputs
```

---

## Generated Comparison Output

Default path:

```text
data/performance/output_modes/output_mode_comparison.json
```

Generated files are artifacts and should not be committed by default.

---

## Example Command

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

---

## Important Decision

The script measures output mode costs but does not optimize or change pipeline behavior.

---

## Changed Files

| File | Action | Reason |
|---|---|---|
| `docs/performance/csv_output_mode_performance_scenarios.md` | Created | Defines output scenarios for comparison. |
| `scripts/performance/run_csv_output_mode_comparison.py` | Created | Runs baseline measurements across output modes. |
| `scripts/performance/run_csv_output_mode_comparison.md` | Created | Documents comparison runner usage and artifact policy. |
| `log_protocol/16_CSV_performance_layer/008_output_mode_performance_split.md` | Created | Records Stage H completion. |

---

## Test Execution Status

```text
Not executed by assistant in this environment.
```

---

## Next Stage

```text
Stage I — Initial Bottleneck Review
```
