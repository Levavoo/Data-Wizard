"""
HTML diagnostic report renderer.

This module converts diagnostic report data into a static, self-contained HTML
string. It does not write files or mutate diagnostic data.
"""

from html import escape
from typing import Any


def render_html_report(
    diagnostic_bundle: dict[str, Any],
    pipeline_status: dict[str, Any] | None = None,
) -> str:
    """
    Render a diagnostic bundle as a static HTML report.

    Args:
        diagnostic_bundle:
            Complete diagnostic bundle.

        pipeline_status:
            Optional pipeline status dictionary.

    Returns:
        HTML report string.
    """
    title = f"CSV Diagnostic Report — {diagnostic_bundle.get('table_name', 'dataset')}"

    body_sections = [
        _render_summary(diagnostic_bundle),
        _render_pipeline_status(pipeline_status),
        _render_quality_report(diagnostic_bundle.get("quality_report", {})),
        _render_validation_report(diagnostic_bundle.get("validation_report", {})),
        _render_quarantine_candidates(
            diagnostic_bundle.get("quarantine_candidates", {})
        ),
        _render_row_classification(diagnostic_bundle.get("row_classification", {})),
        _render_type_diagnostics(diagnostic_bundle.get("type_diagnostics", {})),
        _render_parse_diagnostics(diagnostic_bundle.get("parse_diagnostics", {})),
        _render_metadata(diagnostic_bundle.get("metadata", {})),
    ]

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{escape(title)}</title>",
            "<style>",
            _html_styles(),
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{escape(title)}</h1>",
            *body_sections,
            "</body>",
            "</html>",
        ]
    )


def _render_summary(diagnostic_bundle: dict[str, Any]) -> str:
    """
    Render top-level summary fields.
    """
    rows = [
        ("Table", diagnostic_bundle.get("table_name")),
        ("Rows", diagnostic_bundle.get("row_count")),
        ("Columns", diagnostic_bundle.get("column_count")),
    ]

    return _section(
        title="Summary",
        content=_key_value_table(rows),
    )


def _render_pipeline_status(pipeline_status: dict[str, Any] | None) -> str:
    """
    Render pipeline status if available.
    """
    if pipeline_status is None:
        return _section(
            title="Pipeline Status",
            content="<p>No pipeline status was provided.</p>",
        )

    rows = [
        ("Status", pipeline_status.get("status")),
        ("Strict mode", pipeline_status.get("strict_mode")),
        ("Strict mode failed", pipeline_status.get("strict_mode_failed")),
        ("Errors", pipeline_status.get("error_count")),
        ("Warnings", pipeline_status.get("warning_count")),
    ]

    reasons = pipeline_status.get("reasons", [])

    return _section(
        title="Pipeline Status",
        content=_key_value_table(rows) + _details_block("Reasons", reasons),
    )


def _render_quality_report(quality_report: dict[str, Any]) -> str:
    """
    Render quality report summary.
    """
    rows = [
        ("Duplicate rows", quality_report.get("duplicate_row_count")),
        ("Empty columns", quality_report.get("empty_columns")),
        ("High-null columns", quality_report.get("high_null_columns")),
        ("Missing values by column", quality_report.get("missing_values_by_column")),
    ]

    return _section(
        title="Quality Report",
        content=_key_value_table(rows),
    )


def _render_validation_report(validation_report: dict[str, Any]) -> str:
    """
    Render validation report summary.
    """
    rows = [
        ("Total results", validation_report.get("total_results")),
        ("Passed", validation_report.get("passed_count")),
        ("Failed", validation_report.get("failed_count")),
        ("Has failures", validation_report.get("has_failures")),
        ("Failures by column", validation_report.get("failures_by_column")),
        ("Failures by constraint", validation_report.get("failures_by_constraint")),
    ]

    return _section(
        title="Validation Report",
        content=_key_value_table(rows)
        + _details_block("Failed results", validation_report.get("failed_results", [])),
    )


def _render_quarantine_candidates(quarantine_candidates: dict[str, Any]) -> str:
    """
    Render quarantine candidate summary.
    """
    rows = [
        ("Candidate count", quarantine_candidates.get("candidate_count")),
        ("Summary", quarantine_candidates.get("summary")),
    ]

    return _section(
        title="Quarantine Candidates",
        content=_key_value_table(rows)
        + _details_block("Candidates", quarantine_candidates.get("candidates", [])),
    )


def _render_row_classification(row_classification: dict[str, Any]) -> str:
    """
    Render row classification summary.
    """
    rows = [
        ("Summary", row_classification.get("summary")),
        (
            "Suspicious row count",
            len(row_classification.get("suspicious_rows", [])),
        ),
    ]

    return _section(
        title="Row Classification",
        content=_key_value_table(rows)
        + _details_block(
            "Suspicious rows",
            row_classification.get("suspicious_rows", []),
        ),
    )


def _render_type_diagnostics(type_diagnostics: dict[str, Any]) -> str:
    """
    Render type diagnostics summary.
    """
    mixed_type_columns = type_diagnostics.get("mixed_type_columns", [])
    rows = [("Mixed-type column count", len(mixed_type_columns))]

    return _section(
        title="Type Diagnostics",
        content=_key_value_table(rows)
        + _details_block("Mixed-type columns", mixed_type_columns),
    )


def _render_parse_diagnostics(parse_diagnostics: dict[str, Any]) -> str:
    """
    Render parse diagnostics.
    """
    return _section(
        title="Parse Diagnostics",
        content=_details_block("Parse diagnostics", parse_diagnostics),
    )


def _render_metadata(metadata: dict[str, Any]) -> str:
    """
    Render metadata.
    """
    return _section(
        title="Metadata",
        content=_details_block("Metadata", metadata),
    )


def _section(title: str, content: str) -> str:
    """
    Render one HTML section.
    """
    return f'<section><h2>{escape(title)}</h2>{content}</section>'


def _key_value_table(rows: list[tuple[str, Any]]) -> str:
    """
    Render key/value rows as an HTML table.
    """
    table_rows = []

    for key, value in rows:
        table_rows.append(
            "<tr>"
            f"<th>{escape(str(key))}</th>"
            f"<td>{_format_value(value)}</td>"
            "</tr>"
        )

    return "<table><tbody>" + "".join(table_rows) + "</tbody></table>"


def _details_block(title: str, value: Any) -> str:
    """
    Render nested values inside a preformatted block.
    """
    return (
        "<details open>"
        f"<summary>{escape(title)}</summary>"
        f"<pre>{_format_preformatted(value)}</pre>"
        "</details>"
    )


def _format_value(value: Any) -> str:
    """
    Format a scalar or nested value safely for HTML table cells.
    """
    if isinstance(value, dict | list):
        return f"<pre>{_format_preformatted(value)}</pre>"

    return escape(str(value))


def _format_preformatted(value: Any) -> str:
    """
    Format nested values safely for preformatted HTML blocks.
    """
    return escape(repr(value))


def _html_styles() -> str:
    """
    Return inline CSS for the static report.
    """
    return """
body {
    font-family: Arial, sans-serif;
    line-height: 1.5;
    margin: 2rem;
    color: #222;
    background: #fff;
}
section {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1rem;
}
th, td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    vertical-align: top;
    text-align: left;
}
th {
    width: 16rem;
    background: #f4f4f4;
}
pre {
    white-space: pre-wrap;
    word-break: break-word;
    background: #f8f8f8;
    padding: 0.75rem;
    border-radius: 6px;
}
summary {
    cursor: pointer;
    font-weight: bold;
}
@media print {
    body {
        margin: 1rem;
    }
    section {
        page-break-inside: avoid;
    }
}
""".strip()
