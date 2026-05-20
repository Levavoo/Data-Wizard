"""
Command-line entry point for the JSON pipeline.
"""

import argparse
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_processor.config.pipeline_config import load_pipeline_config
from data_processor.config.pipeline_config_resolver import resolve_pipeline_config_options
from data_processor.core.json_pipeline import run_json_pipeline
from data_processor.validators.constraint_config import load_constraints_from_file

EXECUTION_ERROR_EXIT_CODE = 1


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Run the JSON data pipeline.")
    parser.add_argument("input_path", type=Path, nargs="?", help="Source JSON file path.")
    parser.add_argument("output_path", type=Path, nargs="?", help="Clean CSV output path.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--constraints-path", type=Path, default=None)
    parser.add_argument("--report-path", type=Path, default=None)
    parser.add_argument("--html-report-path", type=Path, default=None)
    parser.add_argument("--quarantine-candidates-path", type=Path, default=None)
    parser.add_argument("--quarantine-rows-path", type=Path, default=None)
    parser.add_argument("--accepted-rows-path", type=Path, default=None)
    parser.add_argument("--strict", action="store_true", default=None)

    return parser.parse_args()


def build_runtime_options(args: argparse.Namespace) -> dict[str, Any]:
    """
    Build JSON runtime options from optional config and CLI overrides.
    """
    if args.config is not None:
        config = load_pipeline_config(args.config)
        runtime_options = resolve_pipeline_config_options(config)

        if runtime_options["input_format"] != "json":
            raise ValueError("JSON pipeline config must set input_format to 'json'.")
    else:
        runtime_options = {
            "input_format": "json",
            "input_path": None,
            "output_path": None,
            "constraints_path": None,
            "report_path": None,
            "html_report_path": None,
            "quarantine_candidates_path": None,
            "quarantine_rows_path": None,
            "accepted_rows_path": None,
            "strict_mode": False,
        }

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

    if args.strict is not None:
        runtime_options["strict_mode"] = args.strict

    if runtime_options.get("input_path") is None:
        raise ValueError("Missing input_path. Provide positional input_path or --config.")

    if runtime_options.get("output_path") is None:
        raise ValueError("Missing output_path. Provide positional output_path or --config.")

    return runtime_options


def main() -> int:
    """
    CLI entry point.
    """
    args = parse_arguments()

    try:
        runtime_options = build_runtime_options(args)
        constraints = []

        if runtime_options["constraints_path"] is not None:
            constraints = load_constraints_from_file(runtime_options["constraints_path"])

        result = run_json_pipeline(
            input_path=runtime_options["input_path"],
            output_path=runtime_options["output_path"],
            report_path=runtime_options["report_path"],
            html_report_path=runtime_options["html_report_path"],
            quarantine_candidates_path=runtime_options["quarantine_candidates_path"],
            quarantine_rows_path=runtime_options["quarantine_rows_path"],
            accepted_rows_path=runtime_options["accepted_rows_path"],
            constraints=constraints,
            strict_mode=runtime_options["strict_mode"],
        )
    except Exception as error:
        print("JSON pipeline failed.", file=sys.stderr)
        print(str(error), file=sys.stderr)
        return EXECUTION_ERROR_EXIT_CODE

    pipeline_status = result["pipeline_status"]

    print("JSON pipeline completed.")

    if args.config is not None:
        print(f"Config: {args.config}")

    print(f"Input: {runtime_options['input_path']}")
    print(f"Output: {runtime_options['output_path']}")
    print(f"Status: {pipeline_status['status']}")

    if runtime_options["report_path"] is not None:
        print(f"JSON report: {runtime_options['report_path']}")

    if runtime_options["html_report_path"] is not None:
        print(f"HTML report: {runtime_options['html_report_path']}")

    if runtime_options["quarantine_candidates_path"] is not None:
        print(f"Quarantine candidates: {runtime_options['quarantine_candidates_path']}")

    if runtime_options["quarantine_rows_path"] is not None:
        print(f"Quarantine rows: {runtime_options['quarantine_rows_path']}")

    if runtime_options["accepted_rows_path"] is not None:
        print(f"Accepted rows: {runtime_options['accepted_rows_path']}")

    return 1 if pipeline_status.get("strict_failed") else 0


if __name__ == "__main__":
    raise SystemExit(main())
