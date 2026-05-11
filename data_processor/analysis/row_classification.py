"""
Suspicious row classification utilities.

This module classifies rows for diagnostic purposes only. It does not mutate,
remove, quarantine, or repair rows.
"""

from collections import Counter
from typing import Any

from data_processor.core.table import Table

COMMENT_PREFIXES = ("#", "//", ";")
SUMMARY_PREFIXES = (
    "total",
    "sum",
    "subtotal",
    "grand total",
)
FOOTER_MARKERS = (
    "end of",
    "generated",
    "export complete",
    "report generated",
)


def classify_table_rows(table: Table) -> dict[str, Any]:
    """
    Classify all table rows.

    Args:
        table:
            Internal dataset table.

    Returns:
        Row classification diagnostics.
    """
    classifications = [
        classify_row(
            row=row,
            row_index=row_index,
        )
        for row_index, row in enumerate(table.rows)
    ]

    summary = Counter(
        classification["classification"] for classification in classifications
    )

    suspicious_rows = [
        classification
        for classification in classifications
        if classification["classification"] != "normal_row"
    ]

    return {
        "rows": classifications,
        "suspicious_rows": suspicious_rows,
        "summary": dict(summary),
    }


def classify_row(row: dict[str, Any], row_index: int) -> dict[str, Any]:
    """
    Classify one row.

    Args:
        row:
            Row dictionary.

        row_index:
            Zero-based table row index.

    Returns:
        Row classification dictionary.
    """
    non_empty_values = _non_empty_values(row)

    if not non_empty_values:
        return _classification(
            row=row,
            row_index=row_index,
            classification="empty_row",
            reason="All row values are empty or null.",
            confidence=1.0,
        )

    first_value = str(non_empty_values[0]).strip()
    normalized_first_value = first_value.lower()

    if _is_comment_row(normalized_first_value):
        return _classification(
            row=row,
            row_index=row_index,
            classification="comment_row",
            reason="First non-empty value starts with a comment marker.",
            confidence=0.95,
        )

    if _is_summary_row(normalized_first_value):
        return _classification(
            row=row,
            row_index=row_index,
            classification="summary_row",
            reason="First non-empty value starts with a summary marker.",
            confidence=0.9,
        )

    if _is_footer_row(normalized_first_value):
        return _classification(
            row=row,
            row_index=row_index,
            classification="footer_row",
            reason="First non-empty value contains a footer marker.",
            confidence=0.85,
        )

    if len(non_empty_values) == 1 and len(row) > 1:
        return _classification(
            row=row,
            row_index=row_index,
            classification="garbage_row",
            reason="Only one value is populated in a multi-column row.",
            confidence=0.65,
        )

    return _classification(
        row=row,
        row_index=row_index,
        classification="normal_row",
        reason="Row does not match suspicious row heuristics.",
        confidence=1.0,
    )


def _non_empty_values(row: dict[str, Any]) -> list[Any]:
    """
    Return non-empty values from a row.
    """
    return [
        value
        for value in row.values()
        if value is not None and str(value).strip() != ""
    ]


def _is_comment_row(value: str) -> bool:
    """
    Check whether the first value looks like a comment marker.
    """
    return value.startswith(COMMENT_PREFIXES)


def _is_summary_row(value: str) -> bool:
    """
    Check whether the first value looks like a summary row marker.
    """
    return any(value.startswith(prefix) for prefix in SUMMARY_PREFIXES)


def _is_footer_row(value: str) -> bool:
    """
    Check whether the first value looks like a footer marker.
    """
    return any(marker in value for marker in FOOTER_MARKERS)


def _classification(
    row: dict[str, Any],
    row_index: int,
    classification: str,
    reason: str,
    confidence: float,
) -> dict[str, Any]:
    """
    Build a row classification dictionary.
    """
    return {
        "row_index": row_index,
        "classification": classification,
        "reason": reason,
        "confidence": confidence,
        "row": row,
    }
