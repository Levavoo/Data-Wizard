05 Format Syntax Layer
→ 06 Structural Model Layer
→ 07 Schema Layer
→ 08 Type Layer
→ 09 Value Normalization Layer
→ 10 Constraint Validation Layer
→ 12 Transformation Layer

Input file
→ parse known format
→ convert to internal table
→ infer schema
→ infer/cast types
→ clean values
→ validate constraints
→ export cleaned dataset

1st Fokus 
CSV
Excel
JSON

01 Import
├── CSV parser
├── Excel parser
└── JSON parser

02 Normalize Structure
├── choose table/sheet
├── flatten JSON
├── detect header row
├── standardize column names
└── align rows/columns

03 Infer Schema
├── detect fields
├── detect missing columns
├── infer column types
└── create cleaning profile

04 Clean Values
├── trim whitespace
├── normalize casing
├── normalize nulls
├── parse numbers
├── parse dates
├── normalize booleans
└── standardize categories

05 Validate
├── missing values
├── duplicates
├── invalid types
├── outliers
├── min/max rules
└── allowed values

06 Transform
├── rename columns
├── filter rows
├── select/drop columns
├── split/combine columns
├── sort
├── group/aggregate
└── export

07 Output
├── cleaned CSV
├── cleaned Excel
├── cleaned JSON
└── cleaning report

accept uploaded file
auto-detect UTF-8 / fallback
support .csv, .xlsx, .json
show error if unreadable

Take semi-clean preformatted data
→ parse it
→ understand its structure
→ infer types
→ clean values
→ produce analysis-ready output