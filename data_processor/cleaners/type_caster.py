"""
Type-aware value casting utilities.

This module casts table values based on each column's inferred type.

Purpose:
- avoid applying every cleaner to every value
- prevent incorrect conversions such as "1" becoming True
- keep casting controlled by schema metadata
"""

from typing import Any

from data_processor.cleaners.booleans import normalize_boolean
from data_processor.cleaners.dates import normalize_date_or_datetime
from data_processor.cleaners.numbers import normalize_float
from data_processor.cleaners.numbers import normalize_integer
from data_processor.core.column import Column
from data_processor.core.table import Table


def cast_table_by_schema(table: Table) -> None:
    """
    Cast table values based on schema column inferred types.

    This function mutates table rows in place.

    Args:
        table:
            Internal dataset table with inferred column types.
    """
    for column in table.schema.columns:
        cast_column_values(
            table=table,
            column=column,
        )


def cast_column_values(
    table: Table,
    column: Column,
) -> None:
    """
    Cast values for one column based on its inferred type.

    Args:
        table:
            Internal dataset table.

        column:
            Column definition containing inferred type.
    """
    for row in table.rows:
        row[column.name] = cast_value_by_type(
            value=row.get(column.name),
            inferred_type=column.inferred_type,
        )


def cast_value_by_type(
    value: Any,
    inferred_type: str,
) -> Any:
    """
    Cast one value according to an inferred logical type.

    Args:
        value:
            Raw or lightly cleaned value.

        inferred_type:
            Logical type from schema inference.

    Returns:
        Cast value or original value.
    """
    if value is None:
        return None

    normalized_type = inferred_type.strip().lower()

    if normalized_type == "integer":
        return normalize_integer(value)

    if normalized_type == "float":
        return normalize_float(value)

    if normalized_type == "boolean":
        return normalize_boolean(value)

    if normalized_type in {"date", "datetime"}:
        return normalize_date_or_datetime(value)

    return value
