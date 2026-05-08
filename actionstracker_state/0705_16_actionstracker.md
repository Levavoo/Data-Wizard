Stage 08 — Pipeline Orchestrator

input file
→ parse
→ clean
→ infer
→ validate
→ export

New-Item data_processor\core\pipeline.py
New-Item data_processor\core\pipeline.md

New-Item tests\test_pipeline.py
New-Item tests\test_pipeline.md

Initial Pipeline Scope

Pipeline should:

1. load CSV
2. normalize nulls
3. normalize text
4. normalize booleans
5. normalize numbers
6. normalize dates
7. infer column types
8. infer schema metadata
9. generate quality report
10. export cleaned CSV


Recommended Main Function
run_csv_pipeline(
    input_path,
    output_path,
)

Return:

{
    "table": table,
    "quality_report": report,
}

Important Architectural Goal

This module should NOT contain cleaning logic itself.

Pipeline responsibilities:

orchestration only

Meaning:

call modules
coordinate stages
return results

NOT:

parse dates directly
clean strings directly
infer types directly
Architecture Achieved After This Stage
CSV File
↓
CsvAdapter
↓
Table
↓
Cleaning Modules
↓
Inference Modules
↓
Validation Modules
↓
CSV Exporter
↓
Clean CSV
After Pipeline

Recommended next stages:

09 CLI runner
10 Excel adapter
11 JSON adapter
12 Transformation engine
13 Rule-based validation
14 Cleaning profiles
15 Config-driven pipelines