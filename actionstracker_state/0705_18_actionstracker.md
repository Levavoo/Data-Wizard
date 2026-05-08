Stage 09 — CLI Runner

Goal:

run pipeline from PowerShell
→ input CSV
→ cleaned output CSV
→ printed quality report

Create:

New-Item scripts\run_csv_pipeline.py
New-Item scripts\run_csv_pipeline.md

Example future command:

python scripts\run_csv_pipeline.py `
    data\raw\customers.csv `
    data\processed\customers_clean.csv

ruff check scripts\run_csv_pipeline.py
black scripts\run_csv_pipeline.py
python scripts\run_csv_pipeline.py examples\sample_dirty.csv data\processed\sample_clean.csv

pytest
git add .
git commit -m "Add CSV pipeline CLI runner"