Universal Data Cleaning Metamodel
│
├── 01_Physical_Storage_Layer
│   ├── Concern: Where/how bytes physically exist
│   ├── Examples
│   │   ├── local file
│   │   ├── database page
│   │   ├── network stream
│   │   ├── object storage blob
│   │   └── memory buffer
│   └── Cleaning tasks
│       ├── file existence checks
│       ├── permission/access validation
│       ├── corruption detection
│       ├── partial file detection
│       └── checksum validation
│
├── 02_Byte_Layer
│   ├── Concern: Raw bytes before meaning
│   ├── Examples
│   │   ├── 41 42 43
│   │   ├── FF FE 00 61
│   │   └── binary blobs
│   └── Cleaning tasks
│       ├── byte validation
│       ├── byte-order checks
│       ├── magic-number detection
│       ├── binary/text detection
│       └── invalid byte handling
│
├── 03_Container_Compression_Layer
│   ├── Concern: Is data wrapped, compressed, archived, or encrypted?
│   ├── Examples
│   │   ├── .zip
│   │   ├── .gz
│   │   ├── .tar
│   │   ├── .7z
│   │   ├── encrypted files
│   │   └── multipart files
│   └── Cleaning tasks
│       ├── decompression
│       ├── archive extraction
│       ├── password/encryption handling
│       ├── nested file detection
│       └── broken archive recovery
│
├── 04_Encoding_Layer
│   ├── Concern: How bytes become characters or primitive binary values
│   ├── Text encodings
│   │   ├── UTF-8
│   │   ├── UTF-16
│   │   ├── UTF-32
│   │   ├── ASCII
│   │   ├── ISO-8859-1
│   │   └── Windows-1252
│   ├── Binary encodings
│   │   ├── little-endian integers
│   │   ├── big-endian integers
│   │   ├── IEEE-754 floats
│   │   ├── decimal/binary-coded decimal
│   │   └── bit-packed values
│   └── Cleaning tasks
│       ├── encoding detection
│       ├── mojibake repair
│       ├── invalid character repair
│       ├── newline normalization
│       ├── endian correction
│       └── BOM handling
│
├── 05_Format_Syntax_Layer
│   ├── Concern: Which grammar/file format organizes the data?
│   ├── Text formats
│   │   ├── CSV
│   │   ├── TSV
│   │   ├── JSON
│   │   ├── XML
│   │   ├── YAML
│   │   ├── HTML
│   │   └── log files
│   ├── Binary formats
│   │   ├── Parquet
│   │   ├── Avro
│   │   ├── ORC
│   │   ├── Arrow
│   │   ├── Protobuf
│   │   ├── MessagePack
│   │   └── database files
│   └── Cleaning tasks
│       ├── parse validation
│       ├── delimiter detection
│       ├── quote/escape repair
│       ├── bracket/brace repair
│       ├── malformed record handling
│       └── schema extraction
│
├── 06_Structural_Model_Layer
│   ├── Concern: What shape does the data have?
│   ├── Structures
│   │   ├── Scalar
│   │   │   ├── one value
│   │   │   └── example: 25
│   │   ├── Vector/List
│   │   │   ├── ordered values
│   │   │   └── example: [1, 2, 3]
│   │   ├── Tabular
│   │   │   ├── rows and columns
│   │   │   └── examples: CSV, SQL table, Excel sheet
│   │   ├── Hierarchical
│   │   │   ├── nested tree
│   │   │   └── examples: JSON, XML, YAML
│   │   ├── Relational
│   │   │   ├── multiple linked tables
│   │   │   └── examples: PostgreSQL, MySQL, SQLite
│   │   ├── Key_Value
│   │   │   ├── keys mapped to values
│   │   │   └── examples: Redis, configs, dictionaries
│   │   ├── Document
│   │   │   ├── flexible records
│   │   │   └── examples: MongoDB, Elasticsearch
│   │   ├── Graph
│   │   │   ├── nodes and edges
│   │   │   └── examples: Neo4j, network data
│   │   └── Event_Stream
│   │       ├── ordered events over time
│   │       └── examples: logs, Kafka, telemetry
│   └── Cleaning tasks
│       ├── flattening
│       ├── nesting
│       ├── pivoting/unpivoting
│       ├── record alignment
│       ├── column normalization
│       ├── relationship validation
│       └── event ordering
│
├── 07_Schema_Layer
│   ├── Concern: What fields exist and what rules define them?
│   ├── Schema types
│   │   ├── explicit schema
│   │   │   ├── SQL table definition
│   │   │   ├── JSON Schema
│   │   │   ├── Avro schema
│   │   │   └── Parquet schema
│   │   └── inferred schema
│   │       ├── inferred CSV columns
│   │       ├── inferred Excel columns
│   │       └── inferred JSON fields
│   └── Cleaning tasks
│       ├── column name standardization
│       ├── missing field detection
│       ├── extra field detection
│       ├── schema drift detection
│       ├── schema merging
│       └── schema versioning
│
├── 08_Type_Layer
│   ├── Concern: What kind of value is each field?
│   ├── Primitive types
│   │   ├── string
│   │   ├── integer
│   │   ├── float
│   │   ├── decimal
│   │   ├── boolean
│   │   ├── date
│   │   ├── datetime
│   │   ├── time
│   │   ├── binary/blob
│   │   └── null
│   ├── Complex types
│   │   ├── array
│   │   ├── object
│   │   ├── struct
│   │   ├── enum/category
│   │   ├── geometry
│   │   └── vector/embedding
│   └── Cleaning tasks
│       ├── type inference
│       ├── type casting
│       ├── invalid value handling
│       ├── numeric precision repair
│       ├── boolean normalization
│       ├── datetime parsing
│       └── null normalization
│
├── 09_Value_Normalization_Layer
│   ├── Concern: Are values written consistently?
│   ├── Examples
│   │   ├── " Germany " → "Germany"
│   │   ├── "DE", "Germany", "Deutschland" → "Germany"
│   │   ├── "yes", "Y", "true", "1" → true
│   │   ├── "1,000.50" vs "1.000,50"
│   │   └── "2026/05/06" vs "06.05.2026"
│   └── Cleaning tasks
│       ├── trimming whitespace
│       ├── casing normalization
│       ├── locale normalization
│       ├── unit normalization
│       ├── currency normalization
│       ├── category mapping
│       ├── date format normalization
│       └── text cleanup
│
├── 10_Constraint_Validation_Layer
│   ├── Concern: Are values technically valid?
│   ├── Constraint types
│   │   ├── required/not-null
│   │   ├── unique
│   │   ├── min/max
│   │   ├── regex pattern
│   │   ├── allowed values
│   │   ├── foreign key
│   │   └── primary key
│   └── Cleaning tasks
│       ├── duplicate detection
│       ├── range validation
│       ├── pattern validation
│       ├── referential integrity checks
│       ├── invalid record quarantine
│       └── rule-based correction
│
├── 11_Semantic_Layer
│   ├── Concern: Does the data make sense in the real world?
│   ├── Examples
│   │   ├── birth_date cannot be after death_date
│   │   ├── order_date cannot be after delivery_date
│   │   ├── age cannot be negative
│   │   ├── country and postal code should match
│   │   └── total_price should equal quantity × unit_price
│   └── Cleaning tasks
│       ├── business rule validation
│       ├── cross-field validation
│       ├── anomaly detection
│       ├── impossible value detection
│       ├── entity resolution
│       └── consistency checks
│
├── 12_Transformation_Layer
│   ├── Concern: How is clean data reshaped for use?
│   ├── Transformations
│   │   ├── select columns
│   │   ├── rename columns
│   │   ├── filter rows
│   │   ├── join datasets
│   │   ├── aggregate
│   │   ├── group by
│   │   ├── sort
│   │   ├── split fields
│   │   ├── combine fields
│   │   ├── derive new columns
│   │   ├── flatten nested data
│   │   └── convert wide/long format
│   └── Examples
│       ├── full_name → first_name + last_name
│       ├── JSON orders → flat order table
│       ├── daily sales → monthly sales
│       └── raw logs → session table
│
├── 13_Canonical_Model_Layer
│   ├── Concern: What internal standard form does the app use?
│   ├── Recommended internal models
│   │   ├── Table
│   │   ├── Record
│   │   ├── Field
│   │   ├── Type
│   │   ├── Constraint
│   │   ├── Relationship
│   │   ├── Event
│   │   └── Metadata
│   └── Purpose
│       ├── one internal representation
│       ├── many input formats
│       ├── many output formats
│       └── consistent cleaning engine
│
└── 14_Output_Serialization_Layer
    ├── Concern: How is cleaned data written out?
    ├── Output targets
    │   ├── CSV
    │   ├── JSON
    │   ├── Excel
    │   ├── SQL database
    │   ├── Parquet
    │   ├── API response
    │   └── data warehouse table
    └── Cleaning concerns
        ├── output encoding
        ├── schema compatibility
        ├── type preservation
        ├── compression
        ├── partitioning
        └── metadata export


Bytes
→ Encoding
→ Format
→ Structure
→ Schema
→ Type
→ Value
→ Constraint
→ Meaning
→ Transformation
→ Output