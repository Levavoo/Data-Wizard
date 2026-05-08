accept CSV, Excel, and JSON files
parse them with format-specific adapters
convert them into one internal Table model
infer schema and column types
clean values consistently
validate data quality and constraints
transform the dataset
export clean CSV, Excel, JSON, and a report

Recommended structure
data-cleaner/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── data_processor/
│   ├── __init__.py
│   │
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── csv_adapter.py
│   │   ├── excel_adapter.py
│   │   └── json_adapter.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── table.py
│   │   ├── column.py
│   │   ├── schema.py
│   │   ├── types.py
│   │   └── pipeline.py
│   │
│   ├── inference/
│   │   ├── __init__.py
│   │   ├── schema_inference.py
│   │   └── type_inference.py
│   │
│   ├── cleaners/
│   │   ├── __init__.py
│   │   ├── nulls.py
│   │   ├── text.py
│   │   ├── numbers.py
│   │   ├── dates.py
│   │   ├── booleans.py
│   │   └── duplicates.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── schema_validator.py
│   │   ├── constraint_validator.py
│   │   └── quality_report.py
│   │
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── columns.py
│   │   ├── rows.py
│   │   └── aggregation.py
│   │
│   └── exporters/
│       ├── __init__.py
│       ├── csv_exporter.py
│       ├── excel_exporter.py
│       └── json_exporter.py
│
├── tests/
│   ├── test_csv_adapter.py
│   ├── test_type_inference.py
│   └── test_cleaners.py
│
├── examples/
│   └── sample_dirty.csv
│
└── scripts/
    └── run_pipeline.py