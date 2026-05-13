import json
import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_reads_semicolon_csv_with_auto_detection(
    tmp_path: Path,
    monkeypatch,
) -> None:
    input_path = tmp_path / "semicolon.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"

    input_path.write_text(
        "customer_id;name;country\n1;Alice;Germany\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--report-path",
            str(report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    detection = report["parse_diagnostics"]["detection"]

    assert report["parse_diagnostics"]["delimiter"] == ";"
    assert detection["delimiter"]["selected_delimiter"] == ";"


def test_cli_uses_explicit_delimiter_override(
    tmp_path: Path,
    monkeypatch,
) -> None:
    input_path = tmp_path / "pipe.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"

    input_path.write_text(
        "customer_id|name|country\n1|Alice|Germany\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--delimiter",
            "|",
            "--report-path",
            str(report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))
    detection = report["parse_diagnostics"]["detection"]

    assert report["parse_diagnostics"]["delimiter"] == "|"
    assert detection["delimiter"]["confidence"] == "override"


def test_cli_uses_explicit_encoding_override(
    tmp_path: Path,
    monkeypatch,
) -> None:
    input_path = tmp_path / "cp1252.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"

    input_path.write_bytes("name,city\nAlice,Düsseldorf – West\n".encode("cp1252"))

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--encoding",
            "cp1252",
            "--report-path",
            str(report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))
    detection = report["parse_diagnostics"]["detection"]

    assert report["parse_diagnostics"]["encoding"] == "cp1252"
    assert detection["encoding"]["confidence"] == "override"


def test_cli_can_disable_auto_detection(
    tmp_path: Path,
    monkeypatch,
) -> None:
    input_path = tmp_path / "comma.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"

    input_path.write_text("name,city\nAlice,Berlin\n", encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
            "--no-auto-detect-csv",
            "--report-path",
            str(report_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))
    detection = report["parse_diagnostics"]["detection"]

    assert detection["encoding"]["confidence"] == "default"
    assert detection["delimiter"]["confidence"] == "default"


def test_cli_detection_options_override_config_values(
    tmp_path: Path,
    monkeypatch,
) -> None:
    input_path = tmp_path / "pipe.csv"
    output_path = tmp_path / "output.csv"
    report_path = tmp_path / "report.json"
    config_path = tmp_path / "config.json"

    input_path.write_text(
        "customer_id|name|country\n1|Alice|Germany\n",
        encoding="utf-8",
    )
    config_path.write_text(
        json.dumps(
            {
                "input_path": str(input_path),
                "output_path": str(output_path),
                "report_path": str(report_path),
                "delimiter": ";",
                "auto_detect_csv": False,
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
            "--delimiter",
            "|",
        ],
    )

    exit_code = main()

    assert exit_code == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["parse_diagnostics"]["delimiter"] == "|"
