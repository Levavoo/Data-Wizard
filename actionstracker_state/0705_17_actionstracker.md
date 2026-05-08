New-Item data_processor\core\pipeline.py
New-Item data_processor\core\pipeline.md

New-Item tests\test_pipeline.py
New-Item tests\test_pipeline.md

ruff check `
    data_processor\core\pipeline.py `
    tests\test_pipeline.py

black `
    data_processor\core\pipeline.py `
    tests\test_pipeline.py

pytest tests\test_pipeline.py
pytest