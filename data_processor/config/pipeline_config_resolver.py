"""
Pipeline config resolver.

This module converts a validated pipeline config dictionary into runtime options.
It does not run the pipeline or load constraints.
"""

from pathlib import Path
from typing import Any

from data_processor.config.profile_resolver import resolve_profile_options

PATH_FIELDS = {
    "input_path",
    "output_path",
    "constraints_path",
    "report_path",
    "html_report_path",
    "quarantine_candidates_path",
    "quarantine_rows_path",
    "accepted_rows_path",
}


def resolve_pipeline_config_options(config: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve validated config into runtime options.

    Args:
        config:
            Validated pipeline config dictionary.

    Returns:
        Runtime options dictionary.
    """
    profile_options = resolve_profile_options(
        config.get("profile"),
        overrides={"strict_mode": config.get("strict_mode")},
    )

    resolved: dict[str, Any] = {
        "profile_options": profile_options,
        "input_format": config.get("input_format", "csv"),
        "input_path": config["input_path"],
        "output_path": config["output_path"],
        "constraints_path": config.get("constraints_path"),
        "report_path": config.get("report_path"),
        "html_report_path": config.get("html_report_path"),
        "quarantine_candidates_path": config.get("quarantine_candidates_path"),
        "quarantine_rows_path": config.get("quarantine_rows_path"),
        "accepted_rows_path": config.get("accepted_rows_path"),
        "strict_mode": profile_options["strict_mode"],
        "encoding": config.get("encoding"),
        "delimiter": config.get("delimiter"),
        "auto_detect_csv": config.get("auto_detect_csv", True),
    }

    return _convert_path_values(resolved)


def _convert_path_values(options: dict[str, Any]) -> dict[str, Any]:
    """
    Convert configured path strings into Path objects.
    """
    converted = dict(options)

    for field in PATH_FIELDS:
        value = converted.get(field)
        if value is not None:
            converted[field] = Path(value)

    return converted
