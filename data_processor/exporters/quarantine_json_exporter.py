"""
Quarantine candidate JSON exporter.

This module writes the quarantine_candidates report section to a UTF-8 JSON file.
"""

import json
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any


def export_quarantine_candidates_to_json(
    quarantine_candidates: dict[str, Any],
    output_path: str | Path,
    encoding: str = "utf-8",
) -> None:
    """
    Export quarantine candidate report data to JSON.

    Args:
        quarantine_candidates:
            Quarantine candidate report dictionary.

        output_path:
            Target JSON output path.

        encoding:
            Output file encoding.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(mode="w", encoding=encoding) as output_file:
        json.dump(
            quarantine_candidates,
            output_file,
            ensure_ascii=False,
            indent=2,
            default=_json_default,
        )
        output_file.write("\n")


def _json_default(value: Any) -> str:
    """
    Convert non-native JSON values to strings.
    """
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")

    if isinstance(value, date):
        return value.isoformat()

    return str(value)
