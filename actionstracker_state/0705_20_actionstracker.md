New-Item data_processor\cleaners\type_caster.py
New-Item data_processor\cleaners\type_caster.md

New-Item tests\test_type_caster.py
New-Item tests\test_type_caster.md

ruff check `
    data_processor\core\pipeline.py `
    data_processor\cleaners\type_caster.py `
    tests\test_pipeline.py `
    tests\test_type_caster.py

black `
    data_processor\core\pipeline.py `
    data_processor\cleaners\type_caster.py `
    tests\test_pipeline.py `
    tests\test_type_caster.py

pytest tests\test_type_caster.py
pytest tests\test_pipeline.py
pytest

python scripts\run_csv_pipeline.py `
    examples\sample_dirty.csv `
    data\processed\sample_clean.csv

Get-Content data\processed\sample_clean.csv