"""
Pipeline orchestration.

This module connects adapters, cleaners, inference, validation, and exporters.

Purpose:
- run the CSV cleaning workflow
- keep processing steps ordered
- avoid putting cleaning logic directly into the pipeline
"""

from pathlib import Path
from typing import Any

from data_processor.adapters.csv_adapter import CsvAdapter
from data_processor.cleaners.booleans import clean_table_booleans
from data_processor.cleaners.dates import clean_table_dates
from data_processor.cleaners.nulls import clean_table_nulls
from data_processor.cleaners.numbers import clean_table_numbers
from data_processor.cleaners.text import clean_table_text
from data_processor.exporters.csv_exporter import export_table_to_csv
from data_processor.inference.schema_inference import infer_schema_metadata
from data_processor.inference.type_inference import infer_table_types
from data_processor.validators.quality_report import generate_quality_report


def run_csv_pipeline(
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    """
    Run the full CSV cleaning pipeline.

    Args:
        input_path:
            Source CSV file path.

        output_path:
            Target cleaned CSV file path.

    Returns:
        Dictionary containing the final table and quality report.
    """
    adapter = CsvAdapter(input_path)
    table = adapter.read()

    clean_table_nulls(table)
    clean_table_text(table)
    clean_table_booleans(table)
    clean_table_numbers(table)
    clean_table_dates(table)

    infer_table_types(table)
    infer_schema_metadata(table)

    quality_report = generate_quality_report(table)

    export_table_to_csv(
        table=table,
        output_path=output_path,
    )

    return {
        "table": table,
        "quality_report": quality_report,
    }
