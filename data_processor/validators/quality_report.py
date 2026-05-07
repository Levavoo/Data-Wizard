"""
Data quality reporting utilities.

This module generates basic quality reports from the internal Table model.

Purpose:
- summarize dataset quality
- detect missing values
- detect duplicate rows
- detect empty columns
- detect high-null columns
"""

from typing import Any

from data_processor.core.table import Table

DEFAULT_HIGH_NULL_THRESHOLD = 0.5


def generate_quality_report(
    table: Table,
    high_null_threshold: float = DEFAULT_HIGH_NULL_THRESHOLD,
) -> dict[str, Any]:
    """
    Generate a basic quality report for a table.

    Args:
        table:
            Internal dataset table.

        high_null_threshold:
            Ratio from 0.0 to 1.0 used to flag high-null columns.

    Returns:
        Dictionary containing quality report results.
    """
    return {
        "table_name": table.name,
        "row_count": table.row_count(),
        "column_count": table.column_count(),
        "missing_values_by_column": missing_values_by_column(table),
        "duplicate_row_count": duplicate_row_count(table),
        "empty_columns": empty_columns(table),
        "high_null_columns": high_null_columns(
            table=table,
            threshold=high_null_threshold,
        ),
    }


def missing_values_by_column(table: Table) -> dict[str, int]:
    """
    Count missing values per column.

    Args:
        table:
            Internal dataset table.

    Returns:
        Dictionary mapping column names to missing counts.
    """
    missing_counts: dict[str, int] = {}

    for column in table.schema.columns:
        count = 0

        for row in table.rows:
            if row.get(column.name) is None:
                count += 1

        missing_counts[column.name] = count

    return missing_counts


def duplicate_row_count(table: Table) -> int:
    """
    Count duplicate rows.

    Args:
        table:
            Internal dataset table.

    Returns:
        Number of duplicate rows.
    """
    seen_rows: set[tuple[tuple[str, Any], ...]] = set()
    duplicate_count = 0

    for row in table.rows:
        row_signature = tuple(sorted(row.items()))

        if row_signature in seen_rows:
            duplicate_count += 1

        else:
            seen_rows.add(row_signature)

    return duplicate_count


def empty_columns(table: Table) -> list[str]:
    """
    Detect columns where all values are missing.

    Args:
        table:
            Internal dataset table.

    Returns:
        List of empty column names.
    """
    result: list[str] = []

    for column in table.schema.columns:
        values = [row.get(column.name) for row in table.rows]

        if values and all(value is None for value in values):
            result.append(column.name)

    return result


def high_null_columns(
    table: Table,
    threshold: float = DEFAULT_HIGH_NULL_THRESHOLD,
) -> list[str]:
    """
    Detect columns with a high ratio of missing values.

    Args:
        table:
            Internal dataset table.

        threshold:
            Ratio from 0.0 to 1.0.

    Returns:
        List of column names exceeding or matching the threshold.
    """
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0.0 and 1.0.")

    if table.row_count() == 0:
        return []

    result: list[str] = []

    missing_counts = missing_values_by_column(table)

    for column_name, missing_count in missing_counts.items():
        null_ratio = missing_count / table.row_count()

        if null_ratio >= threshold:
            result.append(column_name)

    return result
