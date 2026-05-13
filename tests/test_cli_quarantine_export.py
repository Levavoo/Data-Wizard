import json
import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_creates_quarantine_export_files(tmp_path: Path, monkeypatch) -> None:
    """
    Verify CLI writes quarantine export files when paths are provided.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    constraints_path = tmp_path / "constraints.json"
    quarantine_candidates_path = tmp_path / "reports" / "quarantine_candidates.json"
    quarantine_rows_path = tmp_path / "reports" / "quarantine_rows.csv"
    accepted_rows_path = tmp_path / "reports" / "accepted_rows.csv"

    input_path.write_text(
        "Customer ID,Country,Email,Amount\n"
        "1,Germany,alice@example.com,100\n"
        "2,Mars,invalid-email,-5\n"
        "TOTAL,,,\n",
        encoding="utf-8",
    )
    constraints_path.write_text(
        "["
        '{"column": "country", "type": "allowed_values", "values": ["Germany"]},'
        '{"column": "email", "type": "regex", "pattern": "^[^@]+@[^@]+\\\\.[^@]+$"},'
        '{"column": "amount", "type": "min_value", "value": 0}'
        "]",
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
            "--quarantine-candidates-path",
            str(quarantine_candidates_path),
            "--quarantine-rows-path",
            str(quarantine_rows_path),
            "--accepted-rows-path",
            str(accepted_rows_path),
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()
    assert quarantine_candidates_path.exists()
    assert quarantine_rows_path.exists()
    assert accepted_rows_path.exists()

    quarantine_candidates = json.loads(
        quarantine_candidates_path.read_text(encoding="utf-8")
    )
    quarantine_rows = quarantine_rows_path.read_text(encoding="utf-8")
    accepted_rows = accepted_rows_path.read_text(encoding="utf-8")

    assert quarantine_candidates["candidate_count"] >= 2
    assert "invalid-email" in quarantine_rows
    assert "TOTAL" in quarantine_rows
    assert "alice@example.com" in accepted_rows
    assert "invalid-email" not in accepted_rows


def test_cli_quarantine_exports_work_with_strict_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify strict policy failure still writes quarantine export files.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
    constraints_path = tmp_path / "constraints.json"
    quarantine_candidates_path = tmp_path / "reports" / "quarantine_candidates.json"
    quarantine_rows_path = tmp_path / "reports" / "quarantine_rows.csv"

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
            "--quarantine-candidates-path",
            str(quarantine_candidates_path),
            "--quarantine-rows-path",
            str(quarantine_rows_path),
            "--strict",
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()
    assert quarantine_candidates_path.exists()
    assert quarantine_rows_path.exists()
    assert "invalid-email" in quarantine_rows_path.read_text(encoding="utf-8")
