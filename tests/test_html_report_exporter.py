from pathlib import Path

from data_processor.exporters.html_report_exporter import export_report_to_html


def test_export_report_to_html_writes_file(tmp_path: Path) -> None:
    output_path = tmp_path / "reports" / "report.html"

    export_report_to_html(
        html_report="<!doctype html><html><body>Report</body></html>",
        output_path=output_path,
    )

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == (
        "<!doctype html><html><body>Report</body></html>"
    )


def test_export_report_to_html_creates_parent_directories(tmp_path: Path) -> None:
    output_path = tmp_path / "nested" / "reports" / "report.html"

    export_report_to_html(
        html_report="<html></html>",
        output_path=output_path,
    )

    assert output_path.exists()
