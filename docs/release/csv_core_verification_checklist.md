# CSV Core Verification Checklist

## Purpose

This checklist defines local verification commands before merging or releasing the CSV core.

Plan:

```text
docs/plan_stages/17_CSV_core_stabilization_and_release_readiness.md
```

---

## Required Checks

### 1. Full Test Suite

PowerShell:

```powershell
python -m pytest
```

Expected:

```text
all tests pass
```

---

### 2. Real-World CSV Suite

PowerShell:

```powershell
python -m pytest tests/test_real_world_messy_csv_observation.py
python -m pytest tests/test_real_world_parser_diagnostics.py
python -m pytest tests/test_real_world_cleaning_preservation.py
python -m pytest tests/test_real_world_quarantine_and_diagnostics.py
```

Expected:

```text
all Stage 15 real-world tests pass
```

---

### 3. Performance Smoke Tests

PowerShell:

```powershell
python -m pytest tests/performance/test_csv_performance_smoke.py
python -m pytest tests/test_pipeline_performance_metrics.py
```

Expected:

```text
performance tooling smoke tests pass
pipeline timing metrics test passes
```

---

### 4. CLI Basic Workflow

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    tests\fixtures\csv\simple_customers.csv `
    data\processed\release_simple_customers_clean.csv
```

Expected output:

```text
CSV pipeline completed.
clean CSV written to data/processed/
```

---

### 5. CLI Config Workflow

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\customer_migration_config.json
```

Expected output:

```text
config workflow completes
configured outputs are written
```

---

### 6. CLI Full Report and Quarantine Workflow

PowerShell:

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

Expected output:

```text
clean CSV generated
JSON report generated
HTML report generated
quarantine candidate JSON generated
quarantine rows CSV generated
accepted rows CSV generated
```

---

## Optional Checks

### 1. Performance Baseline

PowerShell:

```powershell
python scripts\performance\run_csv_performance_baseline.py `
    --rows 10000 `
    --json-report `
    --html-report
```

Expected:

```text
baseline metrics JSON is generated under data/performance/
```

---

### 2. Output Mode Comparison

PowerShell:

```powershell
python scripts\performance\run_csv_output_mode_comparison.py `
    --rows 10000 `
    --output-dir data\performance\output_modes_10000
```

Expected:

```text
comparison metrics generated under data/performance/output_modes_10000/
```

---

### 3. Semicolon Detection Example

PowerShell:

```powershell
python scripts\run_csv_pipeline.py `
    --config examples\csv\semicolon_customers_config.json
```

Expected:

```text
semicolon-delimited CSV is processed
```

---

## Generated Artifacts

The commands above may create files under:

```text
data/processed/
data/performance/
```

These are generated artifacts and should usually not be committed.

---

## Git Cleanliness Check

After running verification:

```powershell
git status
```

Expected:

```text
no unexpected tracked file changes
only ignored/untracked generated artifacts if any
```

If generated artifacts appear as untracked files, review `.gitignore` and remove or ignore them before commit.

---

## Recommended Final Sequence

PowerShell:

```powershell
git checkout codex
git pull Levavoo codex
python -m pytest
python -m pytest tests/performance/test_csv_performance_smoke.py
python -m pytest tests/test_pipeline_performance_metrics.py
git status
```

Then optionally run manual CLI and performance commands.
