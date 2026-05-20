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
- optionally export quarantine review files
- optionally pass CSV detection settings to the adapter
- optionally collect pipeline step timings
"""

from contextlib import nullcontext
from pathlib import Path
from typing import Any

from data_processor.adapters.csv_adapter import CsvAdapter
from data_processor.cleaners.nulls import clean_table_nulls
from data_processor.cleaners.text import clean_table_text
from data_processor.cleaners.type_caster import cast_table_by_schema
from data_processor.exporters.csv_exporter import export_table_to_csv
from data_processor.exporters.html_report_exporter import export_report_to_html
from data_processor.exporters.json_report_exporter import export_report_to_json
from data_processor.exporters.quarantine_json_exporter import (
    export_quarantine_candidates_to_json,
)
from data_processor.inference.schema_inference import infer_schema_metadata
from data_processor.inference.type_inference import infer_table_types
from data_processor.reports.diagnostic_bundle import build_diagnostic_bundle
from data_processor.reports.html_report import render_html_report
from data_processor.reports.performance_metrics import PerformanceTimer
from data_processor.reports.pipeline_status import build_pipeline_status
from data_processor.reports.quarantine_row_selection import select_accepted_rows
from data_processor.reports.quarantine_row_selection import select_quarantine_rows
from data_processor.validators.constraints import Constraint
from data_processor.validators.constraints import validate_table_constraints
from data_processor.validators.quality_report import generate_quality_report


def run_csv_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    report_path: str | Path | None = None,
    html_report_path: str | Path | None = None,
    quarantine_candidates_path: str | Path | None = None,
    quarantine_rows_path: str | Path | None = None,
    accepted_rows_path: str | Path | None = None,
    constraints: list[Constraint] | None = None,
    strict_mode: bool = False,
    encoding: str | None = None,
    delimiter: str | None = None,
    auto_detect_csv: bool = True,
    collect_step_timings: bool = False,
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

        quarantine_candidates_path:
            Optional target JSON quarantine candidate report path.

        quarantine_rows_path:
            Optional target CSV path containing quarantine candidate rows.

        accepted_rows_path:
            Optional target CSV path containing non-quarantine rows.

        constraints:
            Optional validation constraints to apply after cleaning and casting.

        strict_mode:
            Whether policy failures should be marked as strict-mode failures.

        encoding:
            Optional explicit CSV text encoding.

        delimiter:
            Optional explicit CSV delimiter.

        auto_detect_csv:
            Whether missing CSV encoding/delimiter settings should be detected.

        collect_step_timings:
            Whether optional pipeline step timings should be returned.

    Returns:
        Dictionary containing the final table, quality report,
        validation results, diagnostic bundle, pipeline status, and optional
        performance metrics.
    """
    if constraints is None:
        constraints = []

    performance_timer = PerformanceTimer() if collect_step_timings else None

    adapter = CsvAdapter(
        input_path,
        encoding=encoding,
        delimiter=delimiter,
        auto_detect=auto_detect_csv,
    )

    with _measure(performance_timer, "adapter_read_seconds"):
        table = adapter.read()

    with _measure(performance_timer, "cleaning_seconds"):
        clean_table_nulls(table)
        clean_table_text(table)

    with _measure(performance_timer, "type_inference_first_pass_seconds"):
        infer_table_types(table)

    with _measure(performance_timer, "type_casting_seconds"):
        cast_table_by_schema(table)

    with _measure(performance_timer, "type_inference_second_pass_seconds"):
        infer_table_types(table)
        infer_schema_metadata(table)

    with _measure(performance_timer, "validation_seconds"):
        validation_results = validate_table_constraints(
            table=table,
            constraints=constraints,
        )

    with _measure(performance_timer, "quality_report_seconds"):
        quality_report = generate_quality_report(table)

    with _measure(performance_timer, "diagnostic_bundle_seconds"):
        diagnostic_bundle = build_diagnostic_bundle(
            table=table,
            validation_results=validation_results,
        )

    with _measure(performance_timer, "pipeline_status_seconds"):
        pipeline_status = build_pipeline_status(
            diagnostic_bundle=diagnostic_bundle,
            strict_mode=strict_mode,
        )

    quarantine_candidates = diagnostic_bundle["quarantine_candidates"]

    with _measure(performance_timer, "clean_csv_export_seconds"):
        export_table_to_csv(
            table=table,
            output_path=output_path,
        )

    with _measure(performance_timer, "json_report_export_seconds"):
        if report_path is not None:
            export_report_to_json(
                report=diagnostic_bundle,
                output_path=report_path,
            )

    with _measure(performance_timer, "html_report_export_seconds"):
        if html_report_path is not None:
            html_report = render_html_report(
                diagnostic_bundle=diagnostic_bundle,
                pipeline_status=pipeline_status,
            )
            export_report_to_html(
                html_report=html_report,
                output_path=html_report_path,
            )

    with _measure(performance_timer, "quarantine_json_export_seconds"):
        if quarantine_candidates_path is not None:
            export_quarantine_candidates_to_json(
                quarantine_candidates=quarantine_candidates,
                output_path=quarantine_candidates_path,
            )

    with _measure(performance_timer, "quarantine_rows_export_seconds"):
        if quarantine_rows_path is not None:
            quarantine_rows = select_quarantine_rows(
                table=table,
                quarantine_candidates=quarantine_candidates,
            )
            export_table_to_csv(
                table=quarantine_rows,
                output_path=quarantine_rows_path,
            )

    with _measure(performance_timer, "accepted_rows_export_seconds"):
        if accepted_rows_path is not None:
            accepted_rows = select_accepted_rows(
                table=table,
                quarantine_candidates=quarantine_candidates,
            )
            export_table_to_csv(
                table=accepted_rows,
                output_path=accepted_rows_path,
            )

    result = {
        "table": table,
        "quality_report": quality_report,
        "validation_results": validation_results,
        "diagnostic_bundle": diagnostic_bundle,
        "pipeline_status": pipeline_status,
    }

    if performance_timer is not None:
        result["performance_metrics"] = performance_timer.to_dict()

    return result


def _measure(performance_timer: PerformanceTimer | None, name: str):
    """
    Measure a block when a performance timer is enabled.
    """
    if performance_timer is None:
        return nullcontext()

    return performance_timer.measure(name)
