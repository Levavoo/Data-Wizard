from data_processor.analysis.column_profile import (
    calculate_ratio,
    extract_numeric_values,
    most_common_values,
    profile_all_columns,
    profile_column,
    sample_values,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def create_test_table() -> Table:
    """
    Create reusable profiling test table.
    """
    schema = Schema(
        columns=[
            Column(
                name="customer_id",
                inferred_type="integer",
            ),
            Column(
                name="country",
                inferred_type="string",
            ),
            Column(
                name="amount",
                inferred_type="float",
            ),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": 1,
                "country": "Germany",
                "amount": 100.5,
            },
            {
                "customer_id": 2,
                "country": "France",
                "amount": 250.0,
            },
            {
                "customer_id": 3,
                "country": "Germany",
                "amount": None,
            },
            {
                "customer_id": 4,
                "country": None,
                "amount": 50.25,
            },
        ],
    )


def test_calculate_ratio() -> None:
    """
    Verify ratios are calculated correctly.
    """
    assert calculate_ratio(1, 4) == 0.25


def test_calculate_ratio_zero_division() -> None:
    """
    Verify zero division protection.
    """
    assert calculate_ratio(1, 0) == 0.0


def test_extract_numeric_values() -> None:
    """
    Verify numeric extraction excludes booleans.
    """
    values = [
        1,
        2.5,
        True,
        False,
        "100",
        None,
    ]

    result = extract_numeric_values(values)

    assert result == [1, 2.5]


def test_sample_values() -> None:
    """
    Verify unique sample extraction.
    """
    values = [
        "Germany",
        "France",
        "Germany",
        "Italy",
    ]

    result = sample_values(values)

    assert result == [
        "Germany",
        "France",
        "Italy",
    ]


def test_most_common_values() -> None:
    """
    Verify most common values are detected.
    """
    values = [
        "Germany",
        "France",
        "Germany",
        "Italy",
        "Germany",
    ]

    result = most_common_values(values)

    assert result[0] == ("Germany", 3)


def test_profile_column() -> None:
    """
    Verify column profiling statistics.
    """
    table = create_test_table()

    column = table.schema.columns[1]

    profile = profile_column(
        table=table,
        column=column,
    )

    assert profile["column_name"] == "country"

    assert profile["inferred_type"] == "string"

    assert profile["total_count"] == 4

    assert profile["missing_count"] == 1

    assert profile["unique_count"] == 2

    assert profile["missing_ratio"] == 0.25

    assert profile["unique_ratio"] == 0.5

    assert "Germany" in profile["sample_values"]


def test_profile_numeric_column() -> None:
    """
    Verify numeric min/max profiling.
    """
    table = create_test_table()

    column = table.schema.columns[2]

    profile = profile_column(
        table=table,
        column=column,
    )

    assert profile["min_value"] == 50.25

    assert profile["max_value"] == 250.0


def test_profile_all_columns() -> None:
    """
    Verify all columns are profiled.
    """
    table = create_test_table()

    profiles = profile_all_columns(table)

    assert "customer_id" in profiles

    assert "country" in profiles

    assert "amount" in profiles

    assert profiles["country"]["missing_count"] == 1
