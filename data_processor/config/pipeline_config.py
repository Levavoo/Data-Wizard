"""
CSV pipeline config loader.

This module loads and validates JSON config files for CSV pipeline execution.
It does not run the pipeline.
"""

import json
from pathlib import Path
from typing import Any

REQUIRED_CONFIG_FIELDS = {"input_path", "output_path"}
OPTIONAL_CONFIG_FIELDS = {
    "profile",
    "constraints_path",
    "report_path",
    "html_report_path",
    "quarantine_candidates_path",
    "quarantine_rows_path",
    "accepted_rows_path",
    "strict_mode",
    "encoding",
    "delimiter",
    "auto_detect_csv",
}
ALLOWED_CONFIG_FIELDS = REQUIRED_CONFIG_FIELDS | OPTIONAL_CONFIG_FIELDS


def load_pipeline_config(path: str | Path) -> dict[str, Any]:
    """
    Load and validate a CSV pipeline JSON config file.

    Args:
        path:
            Path to JSON config file.

    Returns:
        Validated config dictionary.
    """
    config_path = Path(path)

    with config_path.open(mode="r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return validate_pipeline_config(config)


def validate_pipeline_config(config: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a CSV pipeline config dictionary.
    """
    if not isinstance(config, dict):
        raise TypeError("Pipeline config must be a JSON object.")

    missing_fields = REQUIRED_CONFIG_FIELDS - config.keys()
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Pipeline config is missing required field(s): {missing}.")

    unknown_fields = set(config) - ALLOWED_CONFIG_FIELDS
    if unknown_fields:
        unknown = ", ".join(sorted(unknown_fields))
        allowed = ", ".join(sorted(ALLOWED_CONFIG_FIELDS))
        raise ValueError(
            f"Pipeline config contains unknown field(s): {unknown}. "
            f"Allowed fields: {allowed}."
        )

    if "strict_mode" in config and not isinstance(config["strict_mode"], bool):
        raise TypeError("Pipeline config field 'strict_mode' must be a boolean.")

    if "auto_detect_csv" in config and not isinstance(config["auto_detect_csv"], bool):
        raise TypeError("Pipeline config field 'auto_detect_csv' must be a boolean.")

    if "encoding" in config and not isinstance(config["encoding"], str):
        raise TypeError("Pipeline config field 'encoding' must be a string.")

    if "delimiter" in config and not isinstance(config["delimiter"], str):
        raise TypeError("Pipeline config field 'delimiter' must be a string.")

    return dict(config)
