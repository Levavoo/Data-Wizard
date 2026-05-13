"""
Command-line runner for the CSV cleaning pipeline.

This script allows the CSV pipeline to be executed from PowerShell.

Example:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv

With profile:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --profile migration_audit

With JSON report:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --report-path data/processed/report.json

With HTML report:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --html-report-path data/processed/report.html

With quarantine exports:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --quarantine-candidates-path data/processed/quarantine_candidates.json --quarantine-rows-path data/processed/quarantine_rows.csv --accepted-rows-path data/processed/accepted_rows.csv

With constraints:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --constraints-path data/raw/constraints.json

With strict mode:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --constraints-path data/raw/constraints.json --strict
"""

import argparse
import json
import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from data_processor.config.cleaning_profiles import list_builtin_profile_names
from data_processor.config.profile_resolver import resolve_profile_options
from data_processor.core.pipeline import run_csv_pipeline
from data_processor.reports.pipeline_status import exit_code_from_pipeline_status
from data_processor.validators.constraint_config import load_constraints_from_config
from data_processor.validators.constraints import Constraint

EXECUTION_ERROR_EXIT_CODE = 1


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(description="Run the CSV cleaning pipeline.")

    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "output_path",
        type=Path,
        help="Path where the cleaned CSV should be written.",
    )

    parser.add_argument(
        "--profile",
        choices=list_builtin_profile_names(),
        default=None,
        help="Optional built-in cleaning profile to use.",
    )

    parser.add_argument(
        "--report-path",
        type=Path,
        default=None,
        help="Optional path where the diagnostic JSON report should be written.",
    )

    parser.add_argument(
        "--html-report-path",
        type=Path,
        default=None,
        help="Optional path where the diagnostic HTML report should be written.",
    )

    parser.add_argument(
        "--quarantine-candidates-path",
        type=Path,
        default=None,
        help="Optional path where quarantine candidate JSON should be written.",
    )

    parser.add_argument(
        "--quarantine-rows-path",
        type=Path,
        default=None,
        help="Optional path where quarantine candidate rows CSV should be written.",
    )

    parser.add_argument(
        "--accepted-rows-path",
        type=Path,
        default=None,
        help="Optional path where accepted rows CSV should be written.",
    )

    parser.add_argument(
        "--constraints-path",
        type=Path,
        default=None,
        help="Optional JSON file containing validation constraints.",
    )

    strict_group = parser.add_mutually_exclusive_group()
    strict_group.add_argument(
        "--strict",
        action="store_true",
        default=None,
        help="Exit with code 2 when strict policy failures are reported.",
    )
    strict_group.add_argument(
        "--no-strict",
        action="store_true",
        default=None,
        help="Disable strict mode even when the selected profile enables it.",
    )

    return parser.parse_args()


def load_constraints_from_path(path: Path | None) -> list[Constraint]:
    """
    Load validation constraints from a JSON file.

    Args:
        path:
            Optional constraints JSON path.

    Returns:
        List of Constraint objects.
    """
    if path is None:
        return []

    with path.open(mode="r", encoding="utf-8") as constraints_file:
        config = json.load(constraints_file)

    return load_constraints_from_config(config)


def resolve_cli_strict_override(args: argparse.Namespace) -> bool | None:
    """
    Resolve explicit CLI strict override.

    Returns:
        True, False, or None when no explicit strict override was provided.
    """
    if args.strict is True:
        return True

    if args.no_strict is True:
        return False

    return None


def main() -> int:
    """
    Run the CSV pipeline from command-line arguments.

    Returns:
        Process exit code.
    """
    args = parse_arguments()

    try:
        profile_options = resolve_profile_options(
            args.profile,
            overrides={"strict_mode": resolve_cli_strict_override(args)},
        )
        constraints = load_constraints_from_path(args.constraints_path)

        result = run_csv_pipeline(
            input_path=args.input_path,
            output_path=args.output_path,
            report_path=args.report_path,
            html_report_path=args.html_report_path,
            quarantine_candidates_path=args.quarantine_candidates_path,
            quarantine_rows_path=args.quarantine_rows_path,
            accepted_rows_path=args.accepted_rows_path,
            constraints=constraints,
            strict_mode=profile_options["strict_mode"],
        )
    except Exception as error:
        print("CSV pipeline failed.", file=sys.stderr)
        print(str(error), file=sys.stderr)
        return EXECUTION_ERROR_EXIT_CODE

    print("CSV pipeline completed.")
    print()
    print(f"Input file: {args.input_path}")
    print(f"Output file: {args.output_path}")
    print(f"Profile: {profile_options['profile_name']}")
    print(f"Profile description: {profile_options['profile_description']}")

    if args.report_path is not None:
        print(f"Diagnostic JSON report: {args.report_path}")

    if args.html_report_path is not None:
        print(f"Diagnostic HTML report: {args.html_report_path}")

    if args.quarantine_candidates_path is not None:
        print(f"Quarantine candidates JSON: {args.quarantine_candidates_path}")

    if args.quarantine_rows_path is not None:
        print(f"Quarantine rows CSV: {args.quarantine_rows_path}")

    if args.accepted_rows_path is not None:
        print(f"Accepted rows CSV: {args.accepted_rows_path}")

    if args.constraints_path is not None:
        print(f"Constraints file: {args.constraints_path}")

    print(f"Strict mode: {profile_options['strict_mode']}")

    print()
    print("Pipeline status:")
    pprint(result["pipeline_status"])

    print()
    print("Quality report:")
    pprint(result["quality_report"])

    print()
    print("Validation report:")
    pprint(result["diagnostic_bundle"]["validation_report"])

    return exit_code_from_pipeline_status(result["pipeline_status"])


if __name__ == "__main__":
    raise SystemExit(main())
