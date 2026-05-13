"""
Pipeline orchestration.

This module connects adapters, cleaners, inference, validation, reporting,
and exporters.

Purpose:
- run the CSV cleaning workflow
- keep processing steps ordered
- avoid putting cleaning logic directly into the pipeline
- optionally validate constraints
- optionally build strict-mode status
- optionally export diagnostic reports
"""

from pathlib import Path
from typing import Any

from data_processor.adapters.csv_adapter import CsvAdapter
from data_processor.cleaners.nulls import clean_table_nulls
from data_processor.cleaners.text import clean_table_text
from data_processor.cleaners.type_caster import cast_table_by_schema
from data_processor.exporters.csv_exporter import export_table_to_csv
from data_processor.exporters.html_report_exporter import export_report_to_html
from data_processor.exporters.json_report_exporter import export_report_to_json
from data_processor.inference.schema_inference import infer_schema_metadata
from data_processor.inference.type_inference import infer_table_types
from data_processor.reports.diagnostic_bundle import build_diagnostic_bundle
from data_processor.reports.html_report import render_html_report
from data_processor.reports.pipeline_status import build_pipeline_status
from data_processor.validators.constraints import Constraint
from data_processor.validators.constraints import validate_table_constraints
from data_processor.validators.quality_report import generate_quality_report


def run_csv_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    report_path: str | Path | None = None,
    html_report_path: str | Path | None = None,
    constraints: list[Constraint] | None = None,
    strict_mode: bool = False,
) -> dict[str, Any]:
    """
    Run the full CSV cleaning pipeline.

    Args:
        input_path:
            Source CSV file path.

        output_path:
            Target cleaned CSV file path.

        report_path:
            Optional target JSON diagnostic report path.

        html_report_path:
            Optional target HTML diagnostic report path.

        constraints:
            Optional validation constraints to apply after cleaning and casting.

        strict_mode:
            Whether policy failures should be marked as strict-mode failures.

    Returns:
        Dictionary containing the final table, quality report,
        validation results, diagnostic bundle, and pipeline status.
    """
    if constraints is None:
        constraints = []

    adapter = CsvAdapter(input_path)
    table = adapter.read()

    clean_table_nulls(table)
    clean_table_text(table)

    infer_table_types(table)
    cast_table_by_schema(table)

    infer_table_types(table)
    infer_schema_metadata(table)

    validation_results = validate_table_constraints(
        table=table,
        constraints=constraints,
    )

    quality_report = generate_quality_report(table)

    diagnostic_bundle = build_diagnostic_bundle(
        table=table,
        validation_results=validation_results,
    )

    pipeline_status = build_pipeline_status(
        diagnostic_bundle=diagnostic_bundle,
        strict_mode=strict_mode,
    )

    export_table_to_csv(
        table=table,
        output_path=output_path,
    )

    if report_path is not None:
        export_report_to_json(
            report=diagnostic_bundle,
            output_path=report_path,
        )

    if html_report_path is not None:
        html_report = render_html_report(
            diagnostic_bundle=diagnostic_bundle,
            pipeline_status=pipeline_status,
        )
        export_report_to_html(
            html_report=html_report,
            output_path=html_report_path,
        )

    return {
        "table": table,
        "quality_report": quality_report,
        "validation_results": validation_results,
        "diagnostic_bundle": diagnostic_bundle,
        "pipeline_status": pipeline_status,
    }
