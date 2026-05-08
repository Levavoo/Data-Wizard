New-Item data_processor\adapters\base_adapter.py
New-Item data_processor\adapters\base_adapter.md

ruff check data_processor\adapters\base_adapter.py
black data_processor\adapters\base_adapter.py

New-Item data_processor\adapters\csv_adapter.py
New-Item data_processor\adapters\csv_adapter.md

ruff check data_processor\adapters\csv_adapter.py
black data_processor\adapters\csv_adapter.py

git add .
git commit -m "Implement CSV adapter"