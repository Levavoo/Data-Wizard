"""
Pipeline status utilities.

This module builds automation-friendly status information from diagnostic bundles.
It does not mutate data, remove rows, or control CLI exit directly.
"""

from typing import Any

STATUS_SUCCESS = "success"
STATUS_COMPLETED_WITH_WARNINGS = "completed_with_warnings"
STATUS_FAILED_POLICY = "failed_policy"


def build_pipeline_status(
    diagnostic_bundle: dict[str, Any],
    strict_mode: bool = False,
) -> dict[str, Any]:
    """
    Build a structured pipeline status from a diagnostic bundle.

    Args:
        diagnostic_bundle:
            Complete diagnostic bundle.

        strict_mode:
            Whether strict policy failure should be reported.

    Returns:
        Pipeline status dictionary.
    """
    validation_report = diagnostic_bundle.get("validation_report", {})
    quarantine_candidates = diagnostic_bundle.get("quarantine_candidates", {})

    validation_failure_count = validation_report.get("failed_count", 0)
    quarantine_summary = quarantine_candidates.get("summary", {})
    quarantine_error_count = quarantine_summary.get("error", 0)
    quarantine_warning_count = quarantine_summary.get("warning", 0)

    error_count = validation_failure_count + quarantine_error_count
    warning_count = quarantine_warning_count

    reasons = _build_status_reasons(
        validation_failure_count=validation_failure_count,
        quarantine_error_count=quarantine_error_count,
        quarantine_warning_count=quarantine_warning_count,
    )

    strict_mode_failed = strict_mode and (
        validation_failure_count > 0 or quarantine_error_count > 0
    )

    if strict_mode_failed:
        status = STATUS_FAILED_POLICY
    elif warning_count > 0 or error_count > 0:
        status = STATUS_COMPLETED_WITH_WARNINGS
    else:
        status = STATUS_SUCCESS

    return {
        "status": status,
        "has_errors": error_count > 0,
        "has_warnings": warning_count > 0,
        "error_count": error_count,
        "warning_count": warning_count,
        "strict_mode": strict_mode,
        "strict_mode_failed": strict_mode_failed,
        "reasons": reasons,
    }


def _build_status_reasons(
    validation_failure_count: int,
    quarantine_error_count: int,
    quarantine_warning_count: int,
) -> list[dict[str, Any]]:
    """
    Build status reason entries.
    """
    reasons = []

    if validation_failure_count > 0:
        reasons.append(
            {
                "source": "validation_report",
                "severity": "error",
                "code": "validation_failures",
                "count": validation_failure_count,
                "message": "Validation failures were reported.",
            }
        )

    if quarantine_error_count > 0:
        reasons.append(
            {
                "source": "quarantine_candidates",
                "severity": "error",
                "code": "quarantine_error_candidates",
                "count": quarantine_error_count,
                "message": "Error-level quarantine candidates were reported.",
            }
        )

    if quarantine_warning_count > 0:
        reasons.append(
            {
                "source": "quarantine_candidates",
                "severity": "warning",
                "code": "quarantine_warning_candidates",
                "count": quarantine_warning_count,
                "message": "Warning-level quarantine candidates were reported.",
            }
        )

    return reasons


def exit_code_from_pipeline_status(pipeline_status: dict[str, Any]) -> int:
    """
    Convert pipeline status into a CLI exit code.

    Returns:
        0 for successful execution, 2 for strict policy failure.
    """
    if pipeline_status.get("strict_mode_failed") is True:
        return 2

    return 0
