CSV / Excel / JSON input
        ↓
Format-specific parser/adapter
        ↓
Canonical internal model
        ↓
Shared cleaning functions
        ↓
Format-specific exporter

data_processor/
│
├── adapters/
│   ├── csv_adapter.py
│   ├── excel_adapter.py
│   └── json_adapter.py
│
├── core/
│   ├── dataset.py
│   ├── schema.py
│   ├── column.py
│   ├── type_inference.py
│   └── cleaning_pipeline.py
│
├── cleaners/
│   ├── text_cleaner.py
│   ├── number_cleaner.py
│   ├── date_cleaner.py
│   ├── boolean_cleaner.py
│   ├── null_cleaner.py
│   └── duplicate_cleaner.py
│
├── validators/
│   ├── schema_validator.py
│   ├── constraint_validator.py
│   └── quality_report.py
│
└── exporters/
    ├── csv_exporter.py
    ├── excel_exporter.py
    └── json_exporter.py

Format-specific code should only answer:
"How do I read/write this format?"

Shared cleaning code should answer:
"How do I clean this data?"

CSV
→ parse rows/columns
→ convert to internal Table

Excel
→ parse sheets/cells
→ convert to internal Table

JSON
→ flatten objects/arrays
→ convert to internal Table

many inputs → one internal model → many outputs

CSV file       → Table
Excel sheet    → Table
JSON array     → Table
JSON object    → flattened Table

Dedicated parsers/adapters: yes
Dedicated cleaners per format: no
Shared cleaning engine: yes