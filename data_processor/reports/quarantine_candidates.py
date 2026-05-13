"""
Quarantine candidate report utilities.

This module builds row-level quarantine candidates from existing diagnostic
sections. It does not mutate rows, remove rows, or change export behavior.
"""

from collections import Counter
from typing import Any

SEVERITY_ORDER = {
    "info": 0,
    "warning": 1,
    "error": 2,
}

SUSPICIOUS_ROW_SEVERITIES = {
    "empty_row": "warning",
    "comment_row": "warning",
    "summary_row": "warning",
    "footer_row": "warning",
    "garbage_row": "warning",
}


def build_quarantine_candidates(
    table_rows: list[dict[str, Any]],
    row_classification: dict[str, Any],
    type_diagnostics: dict[str, Any],
    validation_report: dict[str, Any],
) -> dict[str, Any]:
    """
    Build quarantine candidate diagnostics from existing report sections.

    Args:
        table_rows:
            Processed table rows.

        row_classification:
            Row classification diagnostics.

        type_diagnostics:
            Type diagnostics report.

        validation_report:
            Validation report.

    Returns:
        Quarantine candidate report dictionary.
    """
    reasons_by_row: dict[int, list[dict[str, Any]]] = {}

    _add_row_classification_reasons(
        reasons_by_row=reasons_by_row,
        row_classification=row_classification,
    )
    _add_type_diagnostic_reasons(
        reasons_by_row=reasons_by_row,
        type_diagnostics=type_diagnostics,
    )
    _add_validation_reasons(
        reasons_by_row=reasons_by_row,
        validation_report=validation_report,
    )

    candidates = [
        _build_candidate(
            row_index=row_index,
            row=table_rows[row_index] if 0 <= row_index < len(table_rows) else {},
            reasons=reasons,
        )
        for row_index, reasons in sorted(reasons_by_row.items())
    ]

    summary = Counter(candidate["severity"] for candidate in candidates)

    return {
        "candidate_count": len(candidates),
        "summary": {
            "error": summary.get("error", 0),
            "warning": summary.get("warning", 0),
            "info": summary.get("info", 0),
        },
        "candidates": candidates,
    }


def _add_row_classification_reasons(
    reasons_by_row: dict[int, list[dict[str, Any]]],
    row_classification: dict[str, Any],
) -> None:
    """
    Add suspicious row classification reasons.
    """
    for suspicious_row in row_classification.get("suspicious_rows", []):
        row_index = suspicious_row.get("row_index")

        if row_index is None:
            continue

        classification = suspicious_row.get("classification", "unknown")
        severity = SUSPICIOUS_ROW_SEVERITIES.get(classification, "warning")

        _append_reason(
            reasons_by_row=reasons_by_row,
            row_index=row_index,
            reason={
                "source": "row_classification",
                "code": classification,
                "severity": severity,
                "column": None,
                "message": suspicious_row.get("reason", "Suspicious row detected."),
                "value": None,
            },
        )


def _add_type_diagnostic_reasons(
    reasons_by_row: dict[int, list[dict[str, Any]]],
    type_diagnostics: dict[str, Any],
) -> None:
    """
    Add mixed-type invalid value reasons.
    """
    for column_diagnostics in type_diagnostics.get("mixed_type_columns", []):
        column_name = column_diagnostics.get("column")
        dominant_type = column_diagnostics.get("dominant_type")

        for invalid_value in column_diagnostics.get("invalid_values", []):
            row_index = invalid_value.get("row_index")

            if row_index is None:
                continue

            _append_reason(
                reasons_by_row=reasons_by_row,
                row_index=row_index,
                reason={
                    "source": "type_diagnostics",
                    "code": "mixed_type_invalid_value",
                    "severity": "warning",
                    "column": column_name,
                    "message": f"Value does not match dominant type '{dominant_type}'.",
                    "value": invalid_value.get("value"),
                },
            )


def _add_validation_reasons(
    reasons_by_row: dict[int, list[dict[str, Any]]],
    validation_report: dict[str, Any],
) -> None:
    """
    Add validation failure reasons.
    """
    for failed_result in validation_report.get("failed_results", []):
        row_index = failed_result.get("row_index")

        if row_index is None:
            continue

        constraint_type = failed_result.get("constraint_type", "validation_failed")

        _append_reason(
            reasons_by_row=reasons_by_row,
            row_index=row_index,
            reason={
                "source": "validation_report",
                "code": f"{constraint_type}_failed",
                "severity": "error",
                "column": failed_result.get("column_name"),
                "message": failed_result.get("message", "Validation failed."),
                "value": failed_result.get("value"),
            },
        )


def _append_reason(
    reasons_by_row: dict[int, list[dict[str, Any]]],
    row_index: int,
    reason: dict[str, Any],
) -> None:
    """
    Append one reason to one row index.
    """
    reasons_by_row.setdefault(row_index, []).append(reason)


def _build_candidate(
    row_index: int,
    row: dict[str, Any],
    reasons: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Build one quarantine candidate dictionary.
    """
    severity = _max_severity(reasons)

    return {
        "row_index": row_index,
        "severity": severity,
        "reason_count": len(reasons),
        "reasons": reasons,
        "row": row,
    }


def _max_severity(reasons: list[dict[str, Any]]) -> str:
    """
    Return the highest severity from candidate reasons.
    """
    if not reasons:
        return "info"

    return max(
        (reason.get("severity", "info") for reason in reasons),
        key=lambda severity: SEVERITY_ORDER.get(severity, 0),
    )
