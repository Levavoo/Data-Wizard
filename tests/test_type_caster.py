from datetime import date

from data_processor.cleaners.type_caster import (
    cast_table_by_schema,
    cast_value_by_type,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def test_cast_integer_value() -> None:
    assert cast_value_by_type("1", "integer") == 1


def test_cast_float_value() -> None:
    assert cast_value_by_type("25.50", "float") == 25.5


def test_cast_boolean_value() -> None:
    assert cast_value_by_type("yes", "boolean") is True


def test_cast_date_value() -> None:
    assert cast_value_by_type("2026-01-31", "date") == date(2026, 1, 31)


def test_preserve_string_value() -> None:
    assert cast_value_by_type("Alice", "string") == "Alice"


def test_preserve_unknown_type() -> None:
    assert cast_value_by_type("123", "unknown") == "123"


def test_preserve_none() -> None:
    assert cast_value_by_type(None, "integer") is None


def test_cast_table_by_schema() -> None:
    schema = Schema(
        columns=[
            Column(name="customer_id", inferred_type="integer"),
            Column(name="active", inferred_type="boolean"),
            Column(name="amount", inferred_type="float"),
            Column(name="name", inferred_type="string"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": "1",
                "active": "yes",
                "amount": "25.50",
                "name": "Alice",
            },
            {
                "customer_id": "2",
                "active": "no",
                "amount": "100.75",
                "name": "Bob",
            },
        ],
    )

    cast_table_by_schema(table)

    assert table.rows[0]["customer_id"] == 1
    assert table.rows[0]["active"] is True
    assert table.rows[0]["amount"] == 25.5
    assert table.rows[0]["name"] == "Alice"

    assert table.rows[1]["customer_id"] == 2
    assert table.rows[1]["active"] is False
    assert table.rows[1]["amount"] == 100.75
    assert table.rows[1]["name"] == "Bob"
