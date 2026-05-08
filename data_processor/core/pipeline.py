"""
Pipeline orchestration.

This module connects adapters, cleaners, inference, validation, reporting,
and exporters.

Purpose:
- run the CSV cleaning workflow
- keep processing steps ordered
- avoid putting cleaning logic directly into the pipeline
- optionally export diagnostic reports
"""

from pathlib import Path
from typing import Any

from data_processor.adapters.csv_adapter import CsvAdapter
from data_processor.cleaners.nulls import clean_table_nulls
from data_processor.cleaners.text import clean_table_text
from data_processor.cleaners.type_caster import cast_table_by_schema
from data_processor.exporters.csv_exporter import export_table_to_csv
from data_processor.exporters.json_report_exporter import export_report_to_json
from data_processor.inference.schema_inference import infer_schema_metadata
from data_processor.inference.type_inference import infer_table_types
from data_processor.reports.diagnostic_bundle import build_diagnostic_bundle
from data_processor.validators.quality_report import generate_quality_report


def run_csv_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    report_path: str | Path | None = None,
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

    Returns:
        Dictionary containing the final table, quality report,
        and diagnostic bundle.
    """
    adapter = CsvAdapter(input_path)
    table = adapter.read()

    clean_table_nulls(table)
    clean_table_text(table)

    infer_table_types(table)
    cast_table_by_schema(table)

    infer_table_types(table)
    infer_schema_metadata(table)

    quality_report = generate_quality_report(table)

    diagnostic_bundle = build_diagnostic_bundle(table)

    export_table_to_csv(
        table=table,
        output_path=output_path,
    )

    if report_path is not None:
        export_report_to_json(
            report=diagnostic_bundle,
            output_path=report_path,
        )

    return {
        "table": table,
        "quality_report": quality_report,
        "diagnostic_bundle": diagnostic_bundle,
    }
