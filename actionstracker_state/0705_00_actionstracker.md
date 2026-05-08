New-Item data_processor\core\table.py
New-Item data_processor\core\table.md

New-Item data_processor\core\column.py
New-Item data_processor\core\column.md

New-Item data_processor\core\schema.py
New-Item data_processor\core\schema.md

Implementation order:

1. column.py
2. schema.py
3. table.py

Reason:

Column → Schema → Table
Stage 01 Goal

Create the internal data model that every parser, cleaner, validator, and exporter will use.

The internal model should be simple:

Table
├── name
├── columns
├── rows
└── metadata

Column
├── name
├── original_name
├── inferred_type
├── nullable
└── metadata

Schema
├── columns
└── metadata

Stage 01 Rules
No CSV logic here
No Excel logic here
No JSON logic here
No cleaning logic here
Only reusable internal structures
Keep code small and clear
Use Python standard library only


New-Item data_processor\core\column.py
New-Item data_processor\core\column.md


add_metadata(key: str, value: Any)
Adds extra metadata to the column.
Example:
column.add_metadata("missing_count", 4)

to_dict()
Converts the column object into a dictionary.
Useful for:


schema reports


debugging


tests


JSON export later



Example
from data_processor.core.column import Columncolumn = Column(    name="customer_id",    original_name=" Customer ID ",)column.set_type("integer")column.add_metadata("missing_count", 0)print(column.to_dict())

Developer Notes
This file should not contain:


CSV parsing logic


Excel parsing logic


JSON parsing logic


cleaning logic


validation logic


export logic


It should only describe what a column is inside the internal model.

Future Improvements
Possible later additions:


allowed type enum


column constraints


column statistics


source position tracking


display formatting rules


lineage information


After saving:```powershellruff check data_processor\core\column.pyblack data_processor\core\column.py