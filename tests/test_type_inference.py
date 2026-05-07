from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.inference.type_inference import (
    infer_column_type,
    infer_table_types,
)


def test_infer_null_column() -> None:
    values = ["", "null", "None", "n/a"]

    assert infer_column_type(values) == "null"


def test_infer_boolean_column() -> None:
    values = ["true", "FALSE", "yes", "no"]

    assert infer_column_type(values) == "boolean"


def test_infer_integer_column() -> None:
    values = ["1", "2", "300", ""]

    assert infer_column_type(values) == "integer"


def test_infer_float_column() -> None:
    values = ["1.5", "2.0", "300.75", ""]

    assert infer_column_type(values) == "float"


def test_infer_date_column() -> None:
    values = ["2026-01-01", "01.02.2026", "2026/03/01"]

    assert infer_column_type(values) == "date"


def test_infer_datetime_column() -> None:
    values = ["2026-01-01 10:30:00", "2026-01-02T11:45:00"]

    assert infer_column_type(values) == "datetime"


def test_infer_string_column() -> None:
    values = ["Alice", "Bob", "Germany"]

    assert infer_column_type(values) == "string"


def test_infer_table_types_updates_schema_columns() -> None:
    schema = Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="active"),
            Column(name="country"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": "1",
                "active": "true",
                "country": "Germany",
            },
            {
                "customer_id": "2",
                "active": "false",
                "country": "France",
            },
        ],
    )

    infer_table_types(table)

    assert table.schema.get_column("customer_id").inferred_type == "integer"
    assert table.schema.get_column("active").inferred_type == "boolean"
    assert table.schema.get_column("country").inferred_type == "string"
