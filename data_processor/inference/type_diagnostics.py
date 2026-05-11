"""
Type diagnostic utilities.

This module analyzes type evidence without mutating values or changing inferred
schema types.
"""

from typing import Any

from data_processor.core.table import Table
from data_processor.inference.type_inference import is_boolean
from data_processor.inference.type_inference import is_date
from data_processor.inference.type_inference import is_datetime
from data_processor.inference.type_inference import is_float
from data_processor.inference.type_inference import is_integer
from data_processor.inference.type_inference import is_null

DOMINANT_TYPE_THRESHOLD = 0.8
TYPE_CANDIDATES = (
    "boolean",
    "integer",
    "float",
    "datetime",
    "date",
)


def analyze_column_type_evidence(
    values: list[Any],
    column_name: str,
    threshold: float = DOMINANT_TYPE_THRESHOLD,
) -> dict[str, Any]:
    """
    Analyze type evidence for one column.

    Args:
        values:
            Column values.

        column_name:
            Column name.

        threshold:
            Minimum valid ratio needed for dominant type detection.

    Returns:
        Type diagnostic dictionary.
    """
    non_null_entries = [
        (row_index, value)
        for row_index, value in enumerate(values)
        if not is_null(value)
    ]

    total_values = len(values)
    non_null_count = len(non_null_entries)
    null_count = total_values - non_null_count

    candidate_counts = {
        candidate: _count_candidate_matches(non_null_entries, candidate)
        for candidate in TYPE_CANDIDATES
    }

    dominant_type = _select_dominant_type(
        candidate_counts=candidate_counts,
        non_null_count=non_null_count,
        threshold=threshold,
    )

    invalid_values: list[dict[str, Any]] = []

    if dominant_type is not None:
        for row_index, value in non_null_entries:
            if not _matches_candidate(value, dominant_type):
                invalid_values.append(
                    {
                        "row_index": row_index,
                        "value": value,
                        "expected_type": dominant_type,
                    }
                )

    valid_count = candidate_counts[dominant_type] if dominant_type is not None else 0
    invalid_count = len(invalid_values)

    return {
        "column": column_name,
        "dominant_type": dominant_type,
        "total_values": total_values,
        "non_null_count": non_null_count,
        "null_count": null_count,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "candidate_counts": candidate_counts,
        "invalid_values": invalid_values,
        "is_mixed_type": dominant_type is not None and invalid_count > 0,
    }


def analyze_table_type_evidence(
    table: Table,
    threshold: float = DOMINANT_TYPE_THRESHOLD,
) -> dict[str, Any]:
    """
    Analyze type evidence for all table columns.

    Args:
        table:
            Internal dataset table.

        threshold:
            Minimum valid ratio needed for dominant type detection.

    Returns:
        Table-level type diagnostic dictionary.
    """
    columns = []
    mixed_type_columns = []

    for column in table.schema.columns:
        values = [row.get(column.name) for row in table.rows]
        diagnostics = analyze_column_type_evidence(
            values=values,
            column_name=column.name,
            threshold=threshold,
        )

        columns.append(diagnostics)

        if diagnostics["is_mixed_type"]:
            mixed_type_columns.append(diagnostics)

    return {
        "columns": columns,
        "mixed_type_columns": mixed_type_columns,
    }


def _count_candidate_matches(
    entries: list[tuple[int, Any]],
    candidate: str,
) -> int:
    """
    Count values matching one type candidate.
    """
    return sum(1 for _, value in entries if _matches_candidate(value, candidate))


def _matches_candidate(value: Any, candidate: str) -> bool:
    """
    Check whether value matches a candidate type.
    """
    if candidate == "boolean":
        return is_boolean(value)

    if candidate == "integer":
        return is_integer(value)

    if candidate == "float":
        return is_float(value)

    if candidate == "datetime":
        return is_datetime(value)

    if candidate == "date":
        return is_date(value)

    return False


def _select_dominant_type(
    candidate_counts: dict[str, int],
    non_null_count: int,
    threshold: float,
) -> str | None:
    """
    Select the dominant type candidate.
    """
    if non_null_count == 0:
        return None

    normalized_counts = candidate_counts.copy()

    if normalized_counts["float"] > 0:
        normalized_counts["float"] = max(
            normalized_counts["float"],
            normalized_counts["integer"],
        )

    for candidate in ("boolean", "integer", "float", "datetime", "date"):
        valid_ratio = normalized_counts[candidate] / non_null_count

        if valid_ratio >= threshold:
            return candidate

    return None
