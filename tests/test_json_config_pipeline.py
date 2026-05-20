import subprocess
import sys
from pathlib import Path


def test_json_cli_runs_from_config(tmp_path: Path) -> None:
    config_path = tmp_path / "json_config.json"
    output_path = tmp_path / "customers_clean.csv"
    report_path = tmp_path / "customers_report.json"

    config_path.write_text(
        """
        {
          "input_format": "json",
          "input_path": "tests/fixtures/json/simple_customers.json",
          "output_path": "OUTPUT_PATH",
          "report_path": "REPORT_PATH"
        }
        """.replace("OUTPUT_PATH", str(output_path).replace("\\", "\\\\"))
        .replace("REPORT_PATH", str(report_path).replace("\\", "\\\\")),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_json_pipeline.py",
            "--config",
            str(config_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_path.exists()
    assert report_path.exists()
    assert "Config:" in result.stdout
    assert "JSON pipeline completed." in result.stdout


def test_json_cli_rejects_csv_config_format(tmp_path: Path) -> None:
    config_path = tmp_path / "csv_config.json"
    output_path = tmp_path / "customers_clean.csv"

    config_path.write_text(
        """
        {
          "input_format": "csv",
          "input_path": "tests/fixtures/json/simple_customers.json",
          "output_path": "OUTPUT_PATH"
        }
        """.replace("OUTPUT_PATH", str(output_path).replace("\\", "\\\\")),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_json_pipeline.py",
            "--config",
            str(config_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "input_format" in result.stderr or "input_format" in result.stdout
