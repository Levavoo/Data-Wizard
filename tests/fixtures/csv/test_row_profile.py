from data_processor.analysis.row_profile import (
    calculate_ratio,
    count_missing_values,
    create_row_signature,
    find_duplicate_signatures,
    profile_all_rows,
    profile_row,
)
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


def create_test_table() -> Table:
    """
    Create reusable test table.
    """
    schema = Schema(
        columns=[
            Column(name="customer_id"),
            Column(name="name"),
            Column(name="country"),
        ]
    )

    return Table(
        name="customers",
        schema=schema,
        rows=[
            {
                "customer_id": 1,
                "name": "Alice",
                "country": "Germany",
            },
            {
                "customer_id": 2,
                "name": None,
                "country": "France",
            },
            {
                "customer_id": None,
                "name": None,
                "country": None,
            },
            {
                "customer_id": 1,
                "name": "Alice",
                "country": "Germany",
            },
        ],
    )


def test_calculate_ratio() -> None:
    """
    Verify ratio calculation.
    """
    assert calculate_ratio(1, 4) == 0.25


def test_calculate_ratio_zero_division() -> None:
    """
    Verify zero division handling.
    """
    assert calculate_ratio(1, 0) == 0.0


def test_count_missing_values() -> None:
    """
    Verify missing values are counted.
    """
    row = {
        "customer_id": 1,
        "name": None,
        "country": None,
    }

    column_names = [
        "customer_id",
        "name",
        "country",
    ]

    result = count_missing_values(
        row=row,
        column_names=column_names,
    )

    assert result == 2


def test_create_row_signature() -> None:
    """
    Verify deterministic row signatures.
    """
    row = {
        "name": "Alice",
        "country": "Germany",
    }

    result = create_row_signature(row)

    assert isinstance(result, tuple)

    assert ("country", "Germany") in result


def test_find_duplicate_signatures() -> None:
    """
    Verify duplicate rows are detected.
    """
    table = create_test_table()

    duplicates = find_duplicate_signatures(table)

    assert len(duplicates) == 1


def test_profile_row_complete() -> None:
    """
    Verify complete row profiling.
    """
    table = create_test_table()

    duplicate_signatures = find_duplicate_signatures(table)

    row = table.rows[0]

    profile = profile_row(
        table=table,
        row=row,
        row_index=0,
        duplicate_signatures=duplicate_signatures,
    )

    assert profile["row_index"] == 0

    assert profile["column_count"] == 3

    assert profile["missing_count"] == 0

    assert profile["non_null_count"] == 3

    assert profile["empty_row"] is False

    assert profile["duplicate_candidate"] is True


def test_profile_empty_row() -> None:
    """
    Verify fully empty rows are detected.
    """
    table = create_test_table()

    duplicate_signatures = find_duplicate_signatures(table)

    row = table.rows[2]

    profile = profile_row(
        table=table,
        row=row,
        row_index=2,
        duplicate_signatures=duplicate_signatures,
    )

    assert profile["missing_count"] == 3

    assert profile["missing_ratio"] == 1.0

    assert profile["empty_row"] is True


def test_profile_all_rows() -> None:
    """
    Verify full-table row profiling.
    """
    table = create_test_table()

    profiles = profile_all_rows(table)

    assert len(profiles) == 4

    assert profiles[0]["row_index"] == 0

    assert profiles[2]["empty_row"] is True
