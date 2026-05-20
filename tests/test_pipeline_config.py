import json
from pathlib import Path

import pytest

from data_processor.config.pipeline_config import load_pipeline_config
from data_processor.config.pipeline_config import validate_pipeline_config


def test_validate_pipeline_config_accepts_valid_config() -> None:
    config = {
        "input_path": "input.csv",
        "output_path": "output.csv",
        "profile": "migration_audit",
        "strict_mode": False,
        "encoding": "utf-8",
        "delimiter": ";",
        "auto_detect_csv": True,
    }

    result = validate_pipeline_config(config)

    assert result == config
    assert result is not config


def test_validate_pipeline_config_rejects_missing_required_field() -> None:
    with pytest.raises(ValueError, match="missing required field"):
        validate_pipeline_config({"input_path": "input.csv"})


def test_validate_pipeline_config_rejects_unknown_field() -> None:
    with pytest.raises(ValueError, match="unknown field"):
        validate_pipeline_config(
            {
                "input_path": "input.csv",
                "output_path": "output.csv",
                "bad_field": True,
            }
        )


def test_validate_pipeline_config_rejects_non_boolean_strict_mode() -> None:
    with pytest.raises(TypeError, match="strict_mode"):
        validate_pipeline_config(
            {
                "input_path": "input.csv",
                "output_path": "output.csv",
                "strict_mode": "yes",
            }
        )


def test_validate_pipeline_config_rejects_non_boolean_auto_detect_csv() -> None:
    with pytest.raises(TypeError, match="auto_detect_csv"):
        validate_pipeline_config(
            {
                "input_path": "input.csv",
                "output_path": "output.csv",
                "auto_detect_csv": "no",
            }
        )


def test_validate_pipeline_config_rejects_non_string_encoding() -> None:
    with pytest.raises(TypeError, match="encoding"):
        validate_pipeline_config(
            {
                "input_path": "input.csv",
                "output_path": "output.csv",
                "encoding": 123,
            }
        )


def test_validate_pipeline_config_rejects_non_string_delimiter() -> None:
    with pytest.raises(TypeError, match="delimiter"):
        validate_pipeline_config(
            {
                "input_path": "input.csv",
                "output_path": "output.csv",
                "delimiter": 123,
            }
        )


def test_validate_pipeline_config_rejects_non_object_config() -> None:
    with pytest.raises(TypeError, match="JSON object"):
        validate_pipeline_config(["not", "an", "object"])


def test_load_pipeline_config_reads_json_file(tmp_path: Path) -> None:
    config_path = tmp_path / "pipeline_config.json"
    config = {
        "input_path": "input.csv",
        "output_path": "output.csv",
        "report_path": "report.json",
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")

    result = load_pipeline_config(config_path)

    assert result == config
