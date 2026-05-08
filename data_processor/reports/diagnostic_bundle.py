"""
Diagnostic bundle utilities.

This module combines quality reports, profiles, table metadata, and validation
reports into one structured diagnostic report.

Purpose:
- create one complete report object
- simplify CLI report export
- support audit trails
- support future UI/reporting systems
"""

from typing import Any

from data_processor.analysis.column_profile import profile_all_columns
from data_processor.analysis.row_profile import profile_all_rows
from data_processor.core.table import Table
from data_processor.validators.constraints import ValidationResult
from data_processor.validators.quality_report import generate_quality_report
from data_processor.validators.validation_report import generate_validation_report


def build_diagnostic_bundle(
    table: Table,
    validation_results: list[ValidationResult] | None = None,
) -> dict[str, Any]:
    """
    Build a complete diagnostic bundle for a table.

    Args:
        table:
            Internal dataset table.

        validation_results:
            Optional constraint validation results.

    Returns:
        Complete diagnostic report dictionary.
    """
    if validation_results is None:
        validation_results = []

    return {
        "table_name": table.name,
        "row_count": table.row_count(),
        "column_count": table.column_count(),
        "metadata": table.metadata,
        "quality_report": generate_quality_report(table),
        "column_profiles": profile_all_columns(table),
        "row_profiles": profile_all_rows(table),
        "validation_report": generate_validation_report(validation_results),
    }
