import json
import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_runs_from_config_file(tmp_path: Path, monkeypatch) -> None:
    """
    Verify CLI can run from --config without positional paths.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"
    config_path = tmp_path / "pipeline_config.json"

    input_path.write_text("Name,Country\nAlice,Germany\n", encoding="utf-8")
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "profile": "migration_audit",
                "report_path": str(report_path),
                "strict_mode": False,
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["run_csv_pipeline.py", "--config", str(config_path)],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert report_path.exists()


def test_cli_config_can_write_all_report_outputs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify config-driven CLI can write reports and quarantine exports.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    constraints_path = tmp_path / "constraints.json"
    report_path = tmp_path / "report.json"
    html_report_path = tmp_path / "report.html"
    quarantine_candidates_path = tmp_path / "quarantine_candidates.json"
    quarantine_rows_path = tmp_path / "quarantine_rows.csv"
    accepted_rows_path = tmp_path / "accepted_rows.csv"
    config_path = tmp_path / "pipeline_config.json"

    input_path.write_text(
        "Email\ninvalid-email\nalice@example.com\n",
        encoding="utf-8",
    )
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
                "report_path": str(report_path),
                "html_report_path": str(html_report_path),
                "quarantine_candidates_path": str(quarantine_candidates_path),
                "quarantine_rows_path": str(quarantine_rows_path),
                "accepted_rows_path": str(accepted_rows_path),
                "strict_mode": False,
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["run_csv_pipeline.py", "--config", str(config_path)],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert report_path.exists()
    assert html_report_path.exists()
    assert quarantine_candidates_path.exists()
    assert quarantine_rows_path.exists()
    assert accepted_rows_path.exists()
    assert "invalid-email" in quarantine_rows_path.read_text(encoding="utf-8")


def test_cli_config_strict_mode_returns_two_on_policy_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify config strict mode can trigger strict policy exit code.
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
        ["run_csv_pipeline.py", "--config", str(config_path)],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()
