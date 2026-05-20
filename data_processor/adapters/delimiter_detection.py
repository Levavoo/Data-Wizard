"""
Delimiter detection utility for CSV input.

This module uses simple, conservative scoring over text samples and returns
diagnostics rather than only a delimiter string.
"""

import csv
from statistics import mean
from typing import Any

DEFAULT_DELIMITER_CANDIDATES = (",", ";", "\t", "|")


def detect_delimiter(
    text_sample: str,
    candidates: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """
    Detect a likely delimiter from a text sample.

    Args:
        text_sample:
            Text sample from a CSV-like file.

        candidates:
            Optional delimiter candidates.

    Returns:
        Delimiter detection diagnostics.
    """
    if candidates is None:
        candidates = DEFAULT_DELIMITER_CANDIDATES

    candidate_scores = [_score_candidate(text_sample, delimiter) for delimiter in candidates]
    viable_candidates = [score for score in candidate_scores if score["is_viable"]]

    if not viable_candidates:
        return {
            "selected_delimiter": ",",
            "candidate_scores": candidate_scores,
            "confidence": "low",
            "reason": "No viable delimiter detected; falling back to comma.",
        }

    viable_candidates.sort(
        key=lambda score: (
            score["consistent_row_count"],
            score["average_field_count"],
            score["occurrence_count"],
        ),
        reverse=True,
    )

    best = viable_candidates[0]
    tied = [candidate for candidate in viable_candidates if _is_tied(candidate, best)]

    if len(tied) > 1:
        return {
            "selected_delimiter": ",",
            "candidate_scores": candidate_scores,
            "confidence": "low",
            "reason": "Delimiter detection was ambiguous; falling back to comma.",
        }

    return {
        "selected_delimiter": best["delimiter"],
        "candidate_scores": candidate_scores,
        "confidence": _confidence_for_score(best),
        "reason": f"Delimiter {repr(best['delimiter'])} produced the most consistent rows.",
    }


def _score_candidate(text_sample: str, delimiter: str) -> dict[str, Any]:
    """
    Score one delimiter candidate.
    """
    rows = list(
        csv.reader(
            text_sample.splitlines(),
            delimiter=delimiter,
            skipinitialspace=True,
        )
    )
    non_empty_rows = [row for row in rows if row]
    field_counts = [len(row) for row in non_empty_rows]
    multi_field_counts = [count for count in field_counts if count > 1]
    most_common_count = _most_common_count(multi_field_counts)
    consistent_row_count = multi_field_counts.count(most_common_count)

    return {
        "delimiter": delimiter,
        "occurrence_count": text_sample.count(delimiter),
        "row_count": len(non_empty_rows),
        "average_field_count": mean(multi_field_counts) if multi_field_counts else 1,
        "consistent_row_count": consistent_row_count,
        "is_viable": bool(multi_field_counts),
    }


def _most_common_count(values: list[int]) -> int | None:
    """
    Return the most common integer from a list.
    """
    if not values:
        return None

    return max(set(values), key=values.count)


def _is_tied(candidate: dict[str, Any], best: dict[str, Any]) -> bool:
    """
    Return whether a candidate is tied with the best score.
    """
    return (
        candidate["consistent_row_count"] == best["consistent_row_count"]
        and candidate["average_field_count"] == best["average_field_count"]
        and candidate["occurrence_count"] == best["occurrence_count"]
    )


def _confidence_for_score(score: dict[str, Any]) -> str:
    """
    Return a simple confidence label for a delimiter score.
    """
    if score["consistent_row_count"] >= 3 and score["average_field_count"] >= 2:
        return "high"

    if score["consistent_row_count"] >= 2 and score["average_field_count"] >= 2:
        return "medium"

    return "low"
