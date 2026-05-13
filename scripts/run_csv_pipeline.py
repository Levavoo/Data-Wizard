"""
Command-line runner for the CSV cleaning pipeline.

This script allows the CSV pipeline to be executed from PowerShell.

Example:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv

With config:
    python scripts/run_csv_pipeline.py --config examples/csv/customer_migration_config.json

With explicit CSV detection options:
    python scripts/run_csv_pipeline.py data/raw/input.csv data/processed/output.csv --encoding utf-8 --delimiter ";"
"""

import argparse
import json
import sys
from pathlib import Path
from pprint import pprint
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from data_processor.config.cleaning_profiles import list_builtin_profile_names
from data_processor.config.pipeline_config import load_pipeline_config
from data_processor.config.pipeline_config_resolver import resolve_pipeline_config_options
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
        nargs="?",
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "output_path",
        type=Path,
        nargs="?",
        help="Path where the cleaned CSV should be written.",
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional JSON config file for the CSV pipeline.",
    )

    parser.add_argument(
        "--profile",
        choices=list_builtin_profile_names(),
        default=None,
        help="Optional built-in cleaning profile to use.",
    )

    parser.add_argument(
        "--encoding",
        default=None,
        help="Optional explicit CSV text encoding.",
    )

    parser.add_argument(
        "--delimiter",
        default=None,
        help="Optional explicit CSV delimiter.",
    )

    parser.add_argument(
        "--no-auto-detect-csv",
        action="store_true",
        default=None,
        help="Disable CSV encoding and delimiter auto-detection.",
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
        help="Disable strict mode even when config/profile enables it.",
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


def build_runtime_options(args: argparse.Namespace) -> dict[str, Any]:
    """
    Build runtime options from optional config file and explicit CLI values.

    Explicit CLI values override config values.
    """
    if args.config is not None:
        config = load_pipeline_config(args.config)
        runtime_options = resolve_pipeline_config_options(config)
    else:
        runtime_options = {
            "profile_options": resolve_profile_options(None),
            "input_path": None,
            "output_path": None,
            "constraints_path": None,
            "report_path": None,
            "html_report_path": None,
            "quarantine_candidates_path": None,
            "quarantine_rows_path": None,
            "accepted_rows_path": None,
            "strict_mode": False,
            "encoding": None,
            "delimiter": None,
            "auto_detect_csv": True,
        }

    _apply_cli_overrides(runtime_options, args)
    _validate_runtime_paths(runtime_options)

    return runtime_options


def _apply_cli_overrides(
    runtime_options: dict[str, Any],
    args: argparse.Namespace,
) -> None:
    """
    Apply explicit CLI values over config/profile defaults.
    """
    path_overrides = {
        "input_path": args.input_path,
        "output_path": args.output_path,
        "constraints_path": args.constraints_path,
        "report_path": args.report_path,
        "html_report_path": args.html_report_path,
        "quarantine_candidates_path": args.quarantine_candidates_path,
        "quarantine_rows_path": args.quarantine_rows_path,
        "accepted_rows_path": args.accepted_rows_path,
    }

    for key, value in path_overrides.items():
        if value is not None:
            runtime_options[key] = value

    if args.encoding is not None:
        runtime_options["encoding"] = args.encoding

    if args.delimiter is not None:
        runtime_options["delimiter"] = args.delimiter

    if args.no_auto_detect_csv is True:
        runtime_options["auto_detect_csv"] = False

    strict_override = resolve_cli_strict_override(args)

    if args.profile is not None or strict_override is not None:
        profile_name = args.profile
        if profile_name is None:
            profile_name = runtime_options["profile_options"]["profile_name"]

        profile_options = resolve_profile_options(
            profile_name,
            overrides={"strict_mode": strict_override},
        )
        runtime_options["profile_options"] = profile_options
        runtime_options["strict_mode"] = profile_options["strict_mode"]


def _validate_runtime_paths(runtime_options: dict[str, Any]) -> None:
    """
    Ensure required runtime paths are present.
    """
    if runtime_options.get("input_path") is None:
        raise ValueError("Missing input_path. Provide positional input_path or --config.")

    if runtime_options.get("output_path") is None:
        raise ValueError("Missing output_path. Provide positional output_path or --config.")


def main() -> int:
    """
    Run the CSV pipeline from command-line arguments.

    Returns:
        Process exit code.
    """
    args = parse_arguments()

    try:
        runtime_options = build_runtime_options(args)
        profile_options = runtime_options["profile_options"]
        constraints = load_constraints_from_path(runtime_options["constraints_path"])

        result = run_csv_pipeline(
            input_path=runtime_options["input_path"],
            output_path=runtime_options["output_path"],
            report_path=runtime_options["report_path"],
            html_report_path=runtime_options["html_report_path"],
            quarantine_candidates_path=runtime_options["quarantine_candidates_path"],
            quarantine_rows_path=runtime_options["quarantine_rows_path"],
            accepted_rows_path=runtime_options["accepted_rows_path"],
            constraints=constraints,
            strict_mode=runtime_options["strict_mode"],
            encoding=runtime_options["encoding"],
            delimiter=runtime_options["delimiter"],
            auto_detect_csv=runtime_options["auto_detect_csv"],
        )
    except Exception as error:
        print("CSV pipeline failed.", file=sys.stderr)
        print(str(error), file=sys.stderr)
        return EXECUTION_ERROR_EXIT_CODE

    print("CSV pipeline completed.")
    print()

    if args.config is not None:
        print(f"Config file: {args.config}")

    print(f"Input file: {runtime_options['input_path']}")
    print(f"Output file: {runtime_options['output_path']}")
    print(f"Profile: {profile_options['profile_name']}")
    print(f"Profile description: {profile_options['profile_description']}")
    print(f"CSV encoding: {runtime_options['encoding'] or 'auto'}")
    print(f"CSV delimiter: {runtime_options['delimiter'] or 'auto'}")
    print(f"CSV auto-detect: {runtime_options['auto_detect_csv']}")

    if runtime_options["report_path"] is not None:
        print(f"Diagnostic JSON report: {runtime_options['report_path']}")

    if runtime_options["html_report_path"] is not None:
        print(f"Diagnostic HTML report: {runtime_options['html_report_path']}")

    if runtime_options["quarantine_candidates_path"] is not None:
        print(
            "Quarantine candidates JSON: "
            f"{runtime_options['quarantine_candidates_path']}"
        )

    if runtime_options["quarantine_rows_path"] is not None:
        print(f"Quarantine rows CSV: {runtime_options['quarantine_rows_path']}")

    if runtime_options["accepted_rows_path"] is not None:
        print(f"Accepted rows CSV: {runtime_options['accepted_rows_path']}")

    if runtime_options["constraints_path"] is not None:
        print(f"Constraints file: {runtime_options['constraints_path']}")

    print(f"Strict mode: {runtime_options['strict_mode']}")

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
