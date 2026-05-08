Stage 07 — CSV Exporter

Table
→ write cleaned rows
→ CSV file

New-Item data_processor\exporters\csv_exporter.py
New-Item data_processor\exporters\csv_exporter.md

- create output folder if missing
- write UTF-8 CSV
- write headers from schema column order
- write rows from Table.rows
- preserve cleaned Python values as CSV-safe text

New-Item tests\test_csv_exporter.py
New-Item tests\test_csv_exporter.md

CSV input
→ Table
→ clean/analyze
→ CSV output

ruff check `
    data_processor\exporters\csv_exporter.py `
    tests\test_csv_exporter.py

black `
    data_processor\exporters\csv_exporter.py `
    tests\test_csv_exporter.py

pytest tests\test_csv_exporter.py

pytest

git add .

git commit -m "Implement CSV exporter"