"""
JSON report exporter.

This module writes report dictionaries to JSON files.

Purpose:
- save quality reports
- save validation reports
- save profiling reports
- support audit trails and diagnostics
"""

import json
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any


def export_report_to_json(
    report: dict[str, Any],
    output_path: str | Path,
    encoding: str = "utf-8",
    indent: int = 4,
) -> None:
    """
    Export a report dictionary to a JSON file.

    Args:
        report:
            Report dictionary.

        output_path:
            Target JSON output path.

        encoding:
            Output file encoding.

        indent:
            JSON indentation level.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        mode="w",
        encoding=encoding,
    ) as json_file:
        json.dump(
            report,
            json_file,
            indent=indent,
            ensure_ascii=False,
            default=serialize_report_value,
        )


def serialize_report_value(value: Any) -> str:
    """
    Convert non-JSON-native values into JSON-safe strings.

    Args:
        value:
            Value to serialize.

    Returns:
        JSON-safe string value.

    Raises:
        TypeError:
            If value cannot be serialized.
    """
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, set):
        return str(sorted(value))

    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")
