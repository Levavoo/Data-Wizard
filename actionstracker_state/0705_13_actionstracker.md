Stage 05 — Schema Inference

Table
→ inspect rows and columns
→ enrich schema metadata

New-Item data_processor\inference\schema_inference.py
New-Item data_processor\inference\schema_inference.md

missing_count
unique_count
sample_values
nullable
total_count

infer_schema_metadata()
infer_column_metadata()

New-Item tests\test_schema_inference.py
New-Item tests\test_schema_inference.md

ruff check `
    data_processor\inference\schema_inference.py `
    tests\test_schema_inference.py

black `
    data_processor\inference\schema_inference.py `
    tests\test_schema_inference.py

pytest tests\test_schema_inference.py

pytest

git add .

git commit -m "Implement schema metadata inference"