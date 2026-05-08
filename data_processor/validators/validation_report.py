"""
Validation report utilities.

This module summarizes validation results produced by the constraint engine.

Purpose:
- count passed and failed validation results
- group failures by column
- group failures by constraint type
- identify failed rows
- provide report data for CLI, UI, and export layers
"""

from collections import Counter
from typing import Any

from data_processor.validators.constraints import ValidationResult


def generate_validation_report(
    results: list[ValidationResult],
) -> dict[str, Any]:
    """
    Generate a summary report from validation results.

    Args:
        results:
            Validation results from constraint validation.

    Returns:
        Dictionary containing validation summary data.
    """
    failed_results = [result for result in results if not result.passed]

    passed_results = [result for result in results if result.passed]

    return {
        "total_results": len(results),
        "passed_count": len(passed_results),
        "failed_count": len(failed_results),
        "has_failures": bool(failed_results),
        "failures_by_column": failures_by_column(failed_results),
        "failures_by_constraint": failures_by_constraint(failed_results),
        "failed_rows": failed_rows(failed_results),
        "failed_results": [result.to_dict() for result in failed_results],
    }


def failures_by_column(
    failed_results: list[ValidationResult],
) -> dict[str, int]:
    """
    Count validation failures by column.

    Args:
        failed_results:
            Failed validation results.

    Returns:
        Mapping of column name to failure count.
    """
    counter = Counter(result.column_name for result in failed_results)

    return dict(counter)


def failures_by_constraint(
    failed_results: list[ValidationResult],
) -> dict[str, int]:
    """
    Count validation failures by constraint type.

    Args:
        failed_results:
            Failed validation results.

    Returns:
        Mapping of constraint type to failure count.
    """
    counter = Counter(result.constraint_type for result in failed_results)

    return dict(counter)


def failed_rows(
    failed_results: list[ValidationResult],
) -> list[int]:
    """
    Return sorted unique row indexes with validation failures.

    Args:
        failed_results:
            Failed validation results.

    Returns:
        Sorted row indexes.
    """
    row_indexes = {
        result.row_index for result in failed_results if result.row_index is not None
    }

    return sorted(row_indexes)
