"""
Schema metadata inference utilities.

This module enriches schema columns with statistical and structural metadata.

Purpose:
- detect missing values
- detect uniqueness
- generate sample values
- determine nullable columns
- support validation and reporting
"""

from typing import Any

from data_processor.core.column import Column
from data_processor.core.table import Table

DEFAULT_SAMPLE_SIZE = 5


def infer_schema_metadata(
    table: Table,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> None:
    """
    Infer metadata for all schema columns.

    This function mutates schema columns in place.

    Args:
        table:
            Internal dataset table.

        sample_size:
            Maximum number of sample values per column.
    """
    for column in table.schema.columns:
        metadata = infer_column_metadata(
            table=table,
            column=column,
            sample_size=sample_size,
        )

        for key, value in metadata.items():
            column.add_metadata(key, value)

        column.nullable = metadata["nullable"]


def infer_column_metadata(
    table: Table,
    column: Column,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> dict[str, Any]:
    """
    Infer metadata for one schema column.

    Args:
        table:
            Internal dataset table.

        column:
            Schema column.

        sample_size:
            Maximum number of sample values.

    Returns:
        Dictionary containing inferred metadata.
    """
    values = [row.get(column.name) for row in table.rows]

    total_count = len(values)

    missing_count = sum(1 for value in values if value is None)

    non_null_values = [value for value in values if value is not None]

    unique_count = len(set(non_null_values))

    sample_values = _collect_sample_values(
        values=non_null_values,
        sample_size=sample_size,
    )

    nullable = missing_count > 0

    return {
        "total_count": total_count,
        "missing_count": missing_count,
        "unique_count": unique_count,
        "sample_values": sample_values,
        "nullable": nullable,
    }


def _collect_sample_values(
    values: list[Any],
    sample_size: int,
) -> list[Any]:
    """
    Collect unique sample values.

    Args:
        values:
            Column values.

        sample_size:
            Maximum number of samples.

    Returns:
        List of sample values.
    """
    unique_values: list[Any] = []

    for value in values:
        if value not in unique_values:
            unique_values.append(value)

        if len(unique_values) >= sample_size:
            break

    return unique_values
