"""
Row profiling utilities.

This module analyzes row-level quality without modifying data.

Purpose:
- detect incomplete rows
- detect empty rows
- detect duplicate row candidates
- support future quarantine and repair workflows
"""

from typing import Any

from data_processor.core.table import Table


def profile_all_rows(
    table: Table,
) -> list[dict[str, Any]]:
    """
    Generate profiles for all rows in a table.

    Args:
        table:
            Internal dataset table.

    Returns:
        List of row profile dictionaries.
    """
    duplicate_signatures = find_duplicate_signatures(table)

    profiles: list[dict[str, Any]] = []

    for row_index, row in enumerate(table.rows):
        profiles.append(
            profile_row(
                table=table,
                row=row,
                row_index=row_index,
                duplicate_signatures=duplicate_signatures,
            )
        )

    return profiles


def profile_row(
    table: Table,
    row: dict[str, Any],
    row_index: int,
    duplicate_signatures: set[tuple[tuple[str, Any], ...]] | None = None,
) -> dict[str, Any]:
    """
    Generate a profile for one row.

    Args:
        table:
            Internal dataset table.

        row:
            Row dictionary.

        row_index:
            Zero-based row index.

        duplicate_signatures:
            Optional set of duplicate row signatures.

    Returns:
        Row profile dictionary.
    """
    column_names = table.schema.column_names()

    column_count = len(column_names)

    missing_count = count_missing_values(
        row=row,
        column_names=column_names,
    )

    non_null_count = column_count - missing_count

    row_signature = create_row_signature(row)

    is_duplicate_candidate = (
        duplicate_signatures is not None and row_signature in duplicate_signatures
    )

    return {
        "row_index": row_index,
        "column_count": column_count,
        "missing_count": missing_count,
        "missing_ratio": calculate_ratio(
            missing_count,
            column_count,
        ),
        "non_null_count": non_null_count,
        "empty_row": missing_count == column_count,
        "duplicate_candidate": is_duplicate_candidate,
    }


def count_missing_values(
    row: dict[str, Any],
    column_names: list[str],
) -> int:
    """
    Count missing values in a row.

    Args:
        row:
            Row dictionary.

        column_names:
            Expected schema column names.

    Returns:
        Number of missing values.
    """
    return sum(1 for column_name in column_names if row.get(column_name) is None)


def find_duplicate_signatures(
    table: Table,
) -> set[tuple[tuple[str, Any], ...]]:
    """
    Find row signatures that occur more than once.

    Args:
        table:
            Internal dataset table.

    Returns:
        Set of duplicate row signatures.
    """
    seen_signatures: set[tuple[tuple[str, Any], ...]] = set()
    duplicate_signatures: set[tuple[tuple[str, Any], ...]] = set()

    for row in table.rows:
        row_signature = create_row_signature(row)

        if row_signature in seen_signatures:
            duplicate_signatures.add(row_signature)

        else:
            seen_signatures.add(row_signature)

    return duplicate_signatures


def create_row_signature(
    row: dict[str, Any],
) -> tuple[tuple[str, Any], ...]:
    """
    Create a deterministic row signature.

    Args:
        row:
            Row dictionary.

    Returns:
        Sorted tuple representation of the row.
    """
    return tuple(sorted(row.items()))


def calculate_ratio(
    numerator: int,
    denominator: int,
) -> float:
    """
    Safely calculate a rounded ratio.

    Args:
        numerator:
            Ratio numerator.

        denominator:
            Ratio denominator.

    Returns:
        Ratio as float.
    """
    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator,
        4,
    )
