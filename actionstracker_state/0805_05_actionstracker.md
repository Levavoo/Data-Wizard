Stage 14 — CSV Pipeline Diagnostic Report Integration

Goal:

CSV pipeline
→ cleaned CSV
→ diagnostic JSON report

Stage 14 Files To Update
data_processor/core/pipeline.py
data_processor/core/pipeline.md

scripts/run_csv_pipeline.py
scripts/run_csv_pipeline.md

tests/test_pipeline.py
tests/test_pipeline.md

Desired Pipeline Behavior

Current:

input CSV
→ cleaned CSV
→ quality_report returned

New:

input CSV
→ cleaned CSV
→ diagnostic_bundle returned
→ optional diagnostic JSON report exported

We should update:

run_csv_pipeline(
    input_path,
    output_path,
)

to:

run_csv_pipeline(
    input_path,
    output_path,
    report_path=None,
)

Return:

{
    "table": table,
    "quality_report": quality_report,
    "diagnostic_bundle": diagnostic_bundle,
}

If report_path is provided:

write diagnostic JSON report
CLI Goal

Current command:

python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv

New optional command:

python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv `
    --report-path data\processed\sample_clean_report.json
Implementation Order
1. update pipeline.py
2. update pipeline.md
3. update run_csv_pipeline.py
4. update run_csv_pipeline.md
5. update tests/test_pipeline.py
6. run tests
7. manual CLI test
8. commit