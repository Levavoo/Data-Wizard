from data_processor.reports.pipeline_status import build_pipeline_status
from data_processor.reports.pipeline_status import exit_code_from_pipeline_status


def test_build_pipeline_status_success() -> None:
    diagnostic_bundle = {
        "validation_report": {"failed_count": 0},
        "quarantine_candidates": {
            "summary": {"error": 0, "warning": 0, "info": 0}
        },
    }

    result = build_pipeline_status(diagnostic_bundle)

    assert result["status"] == "success"
    assert result["has_errors"] is False
    assert result["has_warnings"] is False
    assert result["strict_mode_failed"] is False
    assert result["reasons"] == []


def test_build_pipeline_status_completed_with_warnings_in_non_strict_mode() -> None:
    diagnostic_bundle = {
        "validation_report": {"failed_count": 0},
        "quarantine_candidates": {
            "summary": {"error": 0, "warning": 2, "info": 0}
        },
    }

    result = build_pipeline_status(diagnostic_bundle, strict_mode=False)

    assert result["status"] == "completed_with_warnings"
    assert result["has_errors"] is False
    assert result["has_warnings"] is True
    assert result["warning_count"] == 2
    assert result["strict_mode_failed"] is False


def test_build_pipeline_status_validation_failure_non_strict_mode() -> None:
    diagnostic_bundle = {
        "validation_report": {"failed_count": 1},
        "quarantine_candidates": {
            "summary": {"error": 0, "warning": 0, "info": 0}
        },
    }

    result = build_pipeline_status(diagnostic_bundle, strict_mode=False)

    assert result["status"] == "completed_with_warnings"
    assert result["has_errors"] is True
    assert result["error_count"] == 1
    assert result["strict_mode_failed"] is False


def test_build_pipeline_status_validation_failure_strict_mode() -> None:
    diagnostic_bundle = {
        "validation_report": {"failed_count": 1},
        "quarantine_candidates": {
            "summary": {"error": 0, "warning": 0, "info": 0}
        },
    }

    result = build_pipeline_status(diagnostic_bundle, strict_mode=True)

    assert result["status"] == "failed_policy"
    assert result["has_errors"] is True
    assert result["strict_mode"] is True
    assert result["strict_mode_failed"] is True


def test_build_pipeline_status_quarantine_error_strict_mode() -> None:
    diagnostic_bundle = {
        "validation_report": {"failed_count": 0},
        "quarantine_candidates": {
            "summary": {"error": 1, "warning": 2, "info": 0}
        },
    }

    result = build_pipeline_status(diagnostic_bundle, strict_mode=True)

    assert result["status"] == "failed_policy"
    assert result["error_count"] == 1
    assert result["warning_count"] == 2
    assert result["strict_mode_failed"] is True
    assert len(result["reasons"]) == 2


def test_exit_code_from_pipeline_status_success() -> None:
    pipeline_status = {"strict_mode_failed": False}

    assert exit_code_from_pipeline_status(pipeline_status) == 0


def test_exit_code_from_pipeline_status_strict_policy_failure() -> None:
    pipeline_status = {"strict_mode_failed": True}

    assert exit_code_from_pipeline_status(pipeline_status) == 2
