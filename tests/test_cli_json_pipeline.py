import subprocess
import sys
from pathlib import Path


def test_json_cli_writes_clean_csv(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_json_pipeline.py",
            "tests/fixtures/json/simple_customers.json",
            str(output_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_path.exists()
    assert "JSON pipeline completed." in result.stdout
    assert "Alice" in output_path.read_text(encoding="utf-8")


def test_json_cli_writes_reports(tmp_path: Path) -> None:
    output_path = tmp_path / "customers_clean.csv"
    report_path = tmp_path / "customers_report.json"
    html_report_path = tmp_path / "customers_report.html"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_json_pipeline.py",
            "tests/fixtures/json/simple_customers.json",
            str(output_path),
            "--report-path",
            str(report_path),
            "--html-report-path",
            str(html_report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_path.exists()
    assert report_path.exists()
    assert html_report_path.exists()
    assert "JSON report:" in result.stdout
    assert "HTML report:" in result.stdout
