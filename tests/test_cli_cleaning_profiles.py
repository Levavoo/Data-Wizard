import sys
from pathlib import Path

from scripts.run_csv_pipeline import main


def test_cli_profile_strict_crm_enables_strict_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify strict_crm profile enables strict mode by default.
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
            "--profile",
            "strict_crm",
            "--constraints-path",
            str(constraints_path),
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()


def test_cli_no_strict_overrides_strict_profile(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify --no-strict disables strict mode from selected profile.
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
            "--profile",
            "strict_crm",
            "--constraints-path",
            str(constraints_path),
            "--no-strict",
        ],
    )

    exit_code = main()

    assert exit_code == 0
    assert output_path.exists()


def test_cli_without_profile_keeps_default_non_strict_behavior(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify no-profile CLI behavior remains non-strict by default.
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


def test_cli_explicit_strict_overrides_default_profile(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify explicit --strict enables strict behavior even for default profile.
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
            "--profile",
            "default",
            "--constraints-path",
            str(constraints_path),
            "--strict",
        ],
    )

    exit_code = main()

    assert exit_code == 2
    assert output_path.exists()
