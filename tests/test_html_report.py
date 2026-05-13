from data_processor.reports.html_report import render_html_report


def create_diagnostic_bundle() -> dict:
    return {
        "table_name": "customers",
        "row_count": 2,
        "column_count": 3,
        "metadata": {"source_format": "csv"},
        "parse_diagnostics": {"delimiter": ","},
        "quality_report": {
            "duplicate_row_count": 0,
            "empty_columns": [],
            "high_null_columns": [],
            "missing_values_by_column": {"email": 1},
        },
        "validation_report": {
            "total_results": 1,
            "passed_count": 0,
            "failed_count": 1,
            "has_failures": True,
            "failures_by_column": {"email": 1},
            "failures_by_constraint": {"regex_pattern": 1},
            "failed_results": [
                {
                    "row_index": 1,
                    "column_name": "email",
                    "value": "invalid-email",
                }
            ],
        },
        "quarantine_candidates": {
            "candidate_count": 1,
            "summary": {"error": 1, "warning": 0, "info": 0},
            "candidates": [{"row_index": 1, "severity": "error"}],
        },
        "row_classification": {
            "summary": {"normal_row": 2},
            "suspicious_rows": [],
        },
        "type_diagnostics": {"mixed_type_columns": []},
    }


def test_render_html_report_returns_html_document() -> None:
    html = render_html_report(create_diagnostic_bundle())

    assert "<!doctype html>" in html
    assert '<html lang="en">' in html
    assert "CSV Diagnostic Report" in html
    assert "customers" in html


def test_render_html_report_contains_expected_sections() -> None:
    html = render_html_report(create_diagnostic_bundle())

    assert "Summary" in html
    assert "Pipeline Status" in html
    assert "Quality Report" in html
    assert "Validation Report" in html
    assert "Quarantine Candidates" in html
    assert "Row Classification" in html
    assert "Type Diagnostics" in html
    assert "Parse Diagnostics" in html
    assert "Metadata" in html


def test_render_html_report_includes_pipeline_status() -> None:
    html = render_html_report(
        diagnostic_bundle=create_diagnostic_bundle(),
        pipeline_status={
            "status": "failed_policy",
            "strict_mode": True,
            "strict_mode_failed": True,
            "error_count": 1,
            "warning_count": 0,
            "reasons": [],
        },
    )

    assert "failed_policy" in html
    assert "Strict mode failed" in html


def test_render_html_report_escapes_html_values() -> None:
    diagnostic_bundle = create_diagnostic_bundle()
    diagnostic_bundle["table_name"] = "<script>alert('x')</script>"

    html = render_html_report(diagnostic_bundle)

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
