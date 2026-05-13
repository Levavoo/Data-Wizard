import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_creates_html_report(tmp_path: Path, monkeypatch) -> None:
    """
    Verify CLI writes an HTML report when --html-report-path is provided.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    html_report_path = tmp_path / "reports" / "report.html"

    input_path.write_text(
        "Name,Country\nAlice,Germany\nBob,France\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--html-report-path",
            str(html_report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert html_report_path.exists()

    html = html_report_path.read_text(encoding="utf-8")

    assert "<!doctype html>" in html
    assert "CSV Diagnostic Report" in html
    assert "Pipeline Status" in html


def test_cli_html_report_works_with_strict_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify CLI still writes HTML report when strict mode returns policy failure.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    html_report_path = tmp_path / "reports" / "report.html"
    constraints_path = tmp_path / "constraints.json"

    input_path.write_text("Email\ninvalid-email\n", encoding="utf-8")
    constraints_path.write_text(
        '[{"column": "email", "type": "regex", "pattern": "^[^@]+@[^@]+\\\\.[^@]+$"}]',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--constraints-path",
            str(constraints_path),
            "--html-report-path",
            str(html_report_path),
            "--strict",
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()
    assert html_report_path.exists()
    assert "failed_policy" in html_report_path.read_text(encoding="utf-8")
