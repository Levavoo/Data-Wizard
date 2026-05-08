"""
Column profiling utilities.

This module analyzes columns and generates profile statistics.

Purpose:
- understand dataset quality
- support validation and reporting
- support future UI/reporting systems
- support future automated cleaning decisions
"""

from collections import Counter
from typing import Any

from data_processor.core.column import Column
from data_processor.core.table import Table


def profile_all_columns(
    table: Table,
) -> dict[str, dict[str, Any]]:
    """
    Generate profiles for all table columns.

    Args:
        table:
            Internal dataset table.

    Returns:
        Dictionary of column profiles.
    """
    profiles: dict[str, dict[str, Any]] = {}

    for column in table.schema.columns:
        profiles[column.name] = profile_column(
            table=table,
            column=column,
        )

    return profiles


def profile_column(
    table: Table,
    column: Column,
) -> dict[str, Any]:
    """
    Generate profile statistics for one column.

    Args:
        table:
            Internal dataset table.

        column:
            Target column.

    Returns:
        Column profile dictionary.
    """
    values = [row.get(column.name) for row in table.rows]

    non_null_values = [value for value in values if value is not None]

    total_count = len(values)

    missing_count = total_count - len(non_null_values)

    unique_values = set(non_null_values)

    numeric_values = extract_numeric_values(non_null_values)

    return {
        "column_name": column.name,
        "inferred_type": column.inferred_type,
        "total_count": total_count,
        "missing_count": missing_count,
        "missing_ratio": calculate_ratio(
            missing_count,
            total_count,
        ),
        "unique_count": len(unique_values),
        "unique_ratio": calculate_ratio(
            len(unique_values),
            total_count,
        ),
        "sample_values": sample_values(
            non_null_values,
        ),
        "most_common_values": most_common_values(
            non_null_values,
        ),
        "min_value": min(numeric_values) if numeric_values else None,
        "max_value": max(numeric_values) if numeric_values else None,
    }


def extract_numeric_values(
    values: list[Any],
) -> list[int | float]:
    """
    Extract numeric values only.

    Args:
        values:
            Input values.

    Returns:
        Numeric values.
    """
    numeric_types = (int, float)

    return [
        value
        for value in values
        if isinstance(value, numeric_types) and not isinstance(value, bool)
    ]


def sample_values(
    values: list[Any],
    limit: int = 5,
) -> list[Any]:
    """
    Return sample values.

    Args:
        values:
            Input values.

        limit:
            Maximum sample size.

    Returns:
        Sample values list.
    """
    unique_values = []

    for value in values:
        if value not in unique_values:
            unique_values.append(value)

    return unique_values[:limit]


def most_common_values(
    values: list[Any],
    limit: int = 5,
) -> list[tuple[Any, int]]:
    """
    Return most common values.

    Args:
        values:
            Input values.

        limit:
            Maximum number of results.

    Returns:
        List of value/count tuples.
    """
    counter = Counter(values)

    return counter.most_common(limit)


def calculate_ratio(
    numerator: int,
    denominator: int,
) -> float:
    """
    Safely calculate ratios.

    Args:
        numerator:
            Ratio numerator.

        denominator:
            Ratio denominator.

    Returns:
        Float ratio.
    """
    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator,
        4,
    )
