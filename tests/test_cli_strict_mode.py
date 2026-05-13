import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_returns_zero_without_strict_mode_on_validation_failures(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify non-strict CLI execution exits 0 when processing succeeds.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
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
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()


def test_cli_returns_two_with_strict_mode_on_policy_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify strict CLI execution exits 2 on policy failure.
    """
    input_path = tmp_path / "customers.csv"
    output_path = tmp_path / "output.csv"
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
            "--strict",
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()


def test_cli_returns_one_on_execution_error(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify CLI execution exits 1 when processing raises an execution error.
    """
    input_path = tmp_path / "missing.csv"
    output_path = tmp_path / "output.csv"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_csv_pipeline.py",
            str(input_path),
            str(output_path),
        ],
    )

    exit_code = main()

    assert exit_code == 1
    assert not output_path.exists()
