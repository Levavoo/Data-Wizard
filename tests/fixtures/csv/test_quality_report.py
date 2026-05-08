from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table
from data_processor.validators.quality_report import (
    duplicate_row_count,
    empty_columns,
    generate_quality_report,
    high_null_columns,
    missing_values_by_column,
)


def create_test_table() -> Table:
    """
    Create a reusable test table.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
            Column(name="country"),
            Column(name="email"),
            Column(name="unused"),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "name": "Alice",
                "country": "Germany",
                "email": None,
                "unused": None,
            },
            {
                "name": "Bob",
                "country": None,
                "email": "bob@example.com",
                "unused": None,
            },
            {
                "name": "Alice",
                "country": "Germany",
                "email": None,
                "unused": None,
            },
        ],
    )


def test_missing_values_by_column() -> None:
    """
    Verify missing values are counted correctly.
    """
    table = create_test_table()

    result = missing_values_by_column(table)

    assert result["name"] == 0
    assert result["country"] == 1
    assert result["email"] == 2
    assert result["unused"] == 3


def test_duplicate_row_count() -> None:
    """
    Verify duplicate rows are counted correctly.
    """
    table = create_test_table()

    result = duplicate_row_count(table)

    assert result == 1


def test_empty_columns() -> None:
    """
    Verify fully empty columns are detected.
    """
    table = create_test_table()

    result = empty_columns(table)

    assert result == ["unused"]


def test_high_null_columns() -> None:
    """
    Verify high-null columns are detected.
    """
    table = create_test_table()

    result = high_null_columns(
        table=table,
        threshold=0.5,
    )

    assert "email" in result
    assert "unused" in result


def test_high_null_columns_invalid_threshold() -> None:
    """
    Verify invalid thresholds raise ValueError.
    """
    table = create_test_table()

    try:
        high_null_columns(
            table=table,
            threshold=1.5,
        )

    except ValueError:
        assert True
        return

    assert False, "Expected ValueError was not raised."


def test_generate_quality_report() -> None:
    """
    Verify full quality report generation.
    """
    table = create_test_table()

    report = generate_quality_report(table)

    assert report["table_name"] == "customers"
    assert report["row_count"] == 3
    assert report["column_count"] == 4

    assert report["duplicate_row_count"] == 1

    assert report["missing_values_by_column"]["email"] == 2

    assert "unused" in report["empty_columns"]

    assert "email" in report["high_null_columns"]


def test_high_null_columns_empty_table() -> None:
    """
    Verify empty tables return no high-null columns.
    """
    schema = Schema(
        columns=[
            Column(name="name"),
        ]
    )

    table = Table(
        name="empty_table",
        schema=schema,
        rows=[],
    )

    result = high_null_columns(table)

    assert result == []
