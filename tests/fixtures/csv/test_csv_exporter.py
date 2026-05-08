from datetime import date
from datetime import datetime
from pathlib import Path

from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.exporters.csv_exporter import (
    export_table_to_csv,
    serialize_csv_value,
)


def test_serialize_none() -> None:
    """
    Verify None becomes empty string.
    """
    assert serialize_csv_value(None) == ""


def test_serialize_boolean_values() -> None:
    """
    Verify booleans are serialized correctly.
    """
    assert serialize_csv_value(True) == "true"
    assert serialize_csv_value(False) == "false"


def test_serialize_date() -> None:
    """
    Verify dates become ISO date strings.
    """
    result = serialize_csv_value(date(2026, 1, 31))

    assert result == "2026-01-31"


def test_serialize_datetime() -> None:
    """
    Verify datetimes become ISO datetime strings.
    """
    result = serialize_csv_value(datetime(2026, 1, 31, 14, 30, 0))

    assert result == "2026-01-31 14:30:00"


def test_serialize_regular_values() -> None:
    """
    Verify regular values become strings.
    """
    assert serialize_csv_value(100) == "100"
    assert serialize_csv_value(25.5) == "25.5"
    assert serialize_csv_value("Alice") == "Alice"


def test_export_table_to_csv(tmp_path: Path) -> None:
    """
    Verify table export creates a valid CSV file.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
            Column(name="active"),
            Column(name="birth_date"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "name": "Alice",
                "active": True,
                "birth_date": date(2026, 1, 31),
            },
            {
                "name": "Bob",
                "active": False,
                "birth_date": None,
            },
        ],
    )

    output_path = tmp_path / "customers_clean.csv"

    export_table_to_csv(
        table=table,
        output_path=output_path,
    )

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "name,active,birth_date" in content

    assert "Alice,true,2026-01-31" in content

    assert "Bob,false," in content


def test_export_creates_directories(
    tmp_path: Path,
) -> None:
    """
    Verify exporter creates missing directories.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
        ]
    )

    table = Table(
        name="customers",
        schema=schema,
        rows=[
            {"name": "Alice"},
        ],
    )

    output_path = tmp_path / "nested" / "folder" / "customers.csv"

    export_table_to_csv(
        table=table,
        output_path=output_path,
    )

    assert output_path.exists()
