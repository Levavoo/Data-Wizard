# CSV Core Merge Readiness Report

## Purpose

This report summarizes CSV core readiness before merging/releasing the current `codex` branch.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Current Status

The CSV core is ready for local verification before merge.

This stage produced release-readiness documentation and checklists, but did not run local tests in this environment.

Required local verification remains:

```text
full pytest
real-world CSV suite
performance smoke tests
CLI/config/report/quarantine commands
```

---

## What Is Ready

The current CSV core includes:

```text
CSV parsing
encoding detection
delimiter detection
metadata-before-header handling
null/text/number/date/boolean cleaning foundation
type inference and diagnostics
constraint validation
quality reports
diagnostic bundle
JSON report export
HTML report export
quarantine candidate export
quarantine row export
accepted row export
strict mode
cleaning profiles
pipeline config files
CLI config/profile/override workflow
real-world messy CSV test suite
performance measurement layer
optional pipeline timing hooks
```

---

## Required Local Verification Commands

Run:

```powershell
git checkout codex
git pull Levavoo codex
python -m pytest
```

Then targeted checks:

```powershell
python -m pytest tests/test_real_world_messy_csv_observation.py
python -m pytest tests/test_real_world_parser_diagnostics.py
python -m pytest tests/test_real_world_cleaning_preservation.py
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
python -m pytest tests/performance/test_csv_performance_smoke.py
python -m pytest tests/test_pipeline_performance_metrics.py
```

---

## Required Manual CLI Verification

Basic CLI:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\simple_customers.csv `
    data\processed\release_simple_customers_clean.csv
```

Config workflow:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\customer_migration_config.json
```

Full real-world workflow:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\real_world_messy_customers_heavy.csv `
    data\processed\release_real_world_clean.csv `
    --constraints-path tests\fixtures\csv\real_world_messy_customers_constraints.json `
    --report-path data\processed\release_real_world_report.json `
    --html-report-path data\processed\release_real_world_report.html `
    --quarantine-candidates-path data\processed\release_real_world_quarantine_candidates.json `
    --quarantine-rows-path data\processed\release_real_world_quarantine_rows.csv `
    --accepted-rows-path data\processed\release_real_world_accepted_rows.csv
```

---

## Optional Performance Verification

Baseline:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

Output mode comparison:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

---

## Generated Artifact Check

After running verification:

```powershell
git status
```

Generated outputs under these folders should normally remain uncommitted:

```text
data/processed/
data/performance/
```

See:

```text
docs/release/generated_artifact_policy.md
```

---

## Known Limitations

Known limitations are documented in:

```text
docs/release/csv_core_known_limitations.md
```

Important release boundaries:

```text
not a full malformed CSV repair engine
not streaming/chunked processing
not spreadsheet injection hardened yet
not full locale-aware date/boolean/number handling yet
not JSON adapter
not Excel adapter
not GUI
```

---

## Merge Readiness Decision

Merge is recommended only after local verification passes.

If tests fail:

```text
fix failing code or tests
update known limitations if failure exposes expected limitation
rerun full pytest
rerun targeted Stage 15/16 checks
```

If tests pass:

```text
create PR from codex to master
review large branch scope carefully
merge after review
```

---

## Suggested PR Title

```text
CSV core stabilization: profiles, config, reports, quarantine, detection, real-world tests, performance tooling
```

---

## Suggested PR Body

```text
## Summary

Adds CSV core improvements including quarantine exports, cleaning profiles, config-file execution, encoding/delimiter detection, real-world dirty CSV tests, and performance measurement tooling.

## Verification

- [ ] python -m pytest
- [ ] python -m pytest tests/test_real_world_messy_csv_observation.py
- [ ] python -m pytest tests/test_real_world_parser_diagnostics.py
- [ ] python -m pytest tests/test_real_world_cleaning_preservation.py
- [ ] python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
- [ ] python -m pytest tests/performance/test_csv_performance_smoke.py
- [ ] python -m pytest tests/test_pipeline_performance_metrics.py

## Notes

Generated artifacts under data/processed and data/performance are not committed by default.
Known limitations are documented in docs/release/csv_core_known_limitations.md.
```

---

## Recommended Next Stages

After merge/release checkpoint:

```text
18_JSON_adapter
19_Excel_adapter
20_GUI_or_local_web_interface
```

Alternative improvement stages before adapters:

```text
CSV_semantic_text_columns
CSV_malformed_quote_diagnostics
CSV_spreadsheet_injection_export_safety
CSV_locale_profiles_for_dates_booleans_numbers
CSV_diagnostic_depth_controls
CSV_streaming_export_layer
```
