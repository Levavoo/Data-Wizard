import json
import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_positional_paths_override_config_paths(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify explicit positional paths override config input/output paths.
    """
    config_input_path = tmp_path / "config_input.csv"
    cli_input_path = tmp_path / "cli_input.csv"
    config_output_path = tmp_path / "config_output.csv"
    cli_output_path = tmp_path / "cli_output.csv"
    config_path = tmp_path / "pipeline_config.json"

    config_input_path.write_text("Name\nConfig\n", encoding="utf-8")
    cli_input_path.write_text("Name\nCLI\n", encoding="utf-8")
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(config_input_path),
                "output_path": str(config_output_path),
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(cli_input_path),
            str(cli_output_path),
            "--config",
            str(config_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert cli_output_path.exists()
    assert not config_output_path.exists()
    assert "CLI" in cli_output_path.read_text(encoding="utf-8")


def test_cli_report_path_overrides_config_report_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify explicit report path overrides config report path.
    """
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    config_report_path = tmp_path / "config_report.json"
    cli_report_path = tmp_path / "cli_report.json"
    config_path = tmp_path / "pipeline_config.json"

    input_path.write_text("Name\nAlice\n", encoding="utf-8")
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "report_path": str(config_report_path),
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            "--config",
            str(config_path),
            "--report-path",
            str(cli_report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert cli_report_path.exists()
    assert not config_report_path.exists()


def test_cli_no_strict_overrides_config_strict_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify --no-strict overrides config strict mode.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    constraints_path = tmp_path / "constraints.json"
    config_path = tmp_path / "pipeline_config.json"

    input_path.write_text("Email\ninvalid-email\n", encoding="utf-8")
    constraints_path.write_text(
        '[{"column": "email", "type": "regex", "pattern": "^[^@]+@[^@]+\\\\.[^@]+$"}]',
        encoding="utf-8",
    )
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "constraints_path": str(constraints_path),
                "strict_mode": True,
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            "--config",
            str(config_path),
            "--no-strict",
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()


def test_cli_profile_overrides_config_profile(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify explicit profile overrides config profile.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    constraints_path = tmp_path / "constraints.json"
    config_path = tmp_path / "pipeline_config.json"

    input_path.write_text("Email\ninvalid-email\n", encoding="utf-8")
    constraints_path.write_text(
        '[{"column": "email", "type": "regex", "pattern": "^[^@]+@[^@]+\\\\.[^@]+$"}]',
        encoding="utf-8",
    )
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "profile": "migration_audit",
                "constraints_path": str(constraints_path),
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            "--config",
            str(config_path),
            "--profile",
            "strict_crm",
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()
