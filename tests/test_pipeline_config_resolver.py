from pathlib import Path

from data_processor.config.pipeline_config_resolver import (
    resolve_pipeline_config_options,
)


def test_resolve_pipeline_config_options_uses_profile_defaults() -> None:
    result = resolve_pipeline_config_options(
        {
            "input_path": "input.csv",
            "output_path": "output.csv",
            "profile": "strict_crm",
        }
    )

    assert result["profile_options"]["profile_name"] == "strict_crm"
    assert result["strict_mode"] is True
    assert result["input_path"] == Path("input.csv")
    assert result["output_path"] == Path("output.csv")


def test_resolve_pipeline_config_options_applies_strict_mode_override() -> None:
    result = resolve_pipeline_config_options(
        {
            "input_path": "input.csv",
            "output_path": "output.csv",
            "profile": "strict_crm",
            "strict_mode": False,
        }
    )

    assert result["profile_options"]["profile_name"] == "strict_crm"
    assert result["strict_mode"] is False


def test_resolve_pipeline_config_options_preserves_optional_paths() -> None:
    result = resolve_pipeline_config_options(
        {
            "input_path": "input.csv",
            "output_path": "output.csv",
            "constraints_path": "constraints.json",
            "report_path": "report.json",
            "html_report_path": "report.html",
            "quarantine_candidates_path": "quarantine_candidates.json",
            "quarantine_rows_path": "quarantine_rows.csv",
            "accepted_rows_path": "accepted_rows.csv",
        }
    )

    assert result["constraints_path"] == Path("constraints.json")
    assert result["report_path"] == Path("report.json")
    assert result["html_report_path"] == Path("report.html")
    assert result["quarantine_candidates_path"] == Path("quarantine_candidates.json")
    assert result["quarantine_rows_path"] == Path("quarantine_rows.csv")
    assert result["accepted_rows_path"] == Path("accepted_rows.csv")


def test_resolve_pipeline_config_options_uses_default_profile_when_missing() -> None:
    result = resolve_pipeline_config_options(
        {
            "input_path": "input.csv",
            "output_path": "output.csv",
        }
    )

    assert result["profile_options"]["profile_name"] == "default"
    assert result["strict_mode"] is False
    assert result["auto_detect_csv"] is True
    assert result["encoding"] is None
    assert result["delimiter"] is None


def test_resolve_pipeline_config_options_preserves_detection_options() -> None:
    result = resolve_pipeline_config_options(
        {
            "input_path": "input.csv",
            "output_path": "output.csv",
            "encoding": "cp1252",
            "delimiter": ";",
            "auto_detect_csv": False,
        }
    )

    assert result["encoding"] == "cp1252"
    assert result["delimiter"] == ";"
    assert result["auto_detect_csv"] is False
