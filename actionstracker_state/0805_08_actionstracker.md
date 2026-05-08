Improve type_inference.py so it recognizes existing Python int, float, bool, date, and datetime values.

The report shows the full diagnostic bundle was created:

quality_report       ✓
column_profiles      ✓
row_profiles         ✓
validation_report    ✓
JSON report export   ✓

One issue is visible and should be fixed next:

customer_id inferred_type = "string"
active inferred_type = "string"

But the values were cast correctly:

customer_id sample values: 1, 2, 3, 4
active sample values: true, false

So after type-aware casting, infer_table_types() is not recognizing non-string Python values. Our current type inference mostly checks strings.

Then the report should show:

customer_id inferred_type = integer
active inferred_type = boolean

data_processor/inference/type_inference.py
data_processor/inference/type_inference.md
tests/test_type_inference.py
tests/test_type_inference.md

ruff check `
    data_processor\inference\type_inference.py `
    tests\test_type_inference.py

black `
    data_processor\inference\type_inference.py `
    tests\test_type_inference.py

pytest tests\test_type_inference.py
pytest