from data_processor.reports.quarantine_candidates import build_quarantine_candidates


def test_build_quarantine_candidates_from_validation_failures() -> None:
    table_rows = [
        {"email": "alice@example.com"},
        {"email": "invalid-email"},
    ]
    row_classification = {"suspicious_rows": []}
    type_diagnostics = {"mixed_type_columns": []}
    validation_report = {
        "failed_results": [
            {
                "row_index": 1,
                "column_name": "email",
                "constraint_type": "regex_pattern",
                "message": "Value does not match pattern.",
                "value": "invalid-email",
            }
        ]
    }

    result = build_quarantine_candidates(
        table_rows=table_rows,
        row_classification=row_classification,
        type_diagnostics=type_diagnostics,
        validation_report=validation_report,
    )

    assert result["candidate_count"] == 1
    assert result["summary"] == {"error": 1, "warning": 0, "info": 0}
    assert result["candidates"][0]["row_index"] == 1
    assert result["candidates"][0]["severity"] == "error"
    assert result["candidates"][0]["reasons"][0]["source"] == "validation_report"


def test_build_quarantine_candidates_from_suspicious_rows() -> None:
    table_rows = [
        {"customer_id": "1", "amount": "100"},
        {"customer_id": "TOTAL", "amount": "100"},
    ]
    row_classification = {
        "suspicious_rows": [
            {
                "row_index": 1,
                "classification": "summary_row",
                "reason": "First non-empty value starts with a summary marker.",
            }
        ]
    }
    type_diagnostics = {"mixed_type_columns": []}
    validation_report = {"failed_results": []}

    result = build_quarantine_candidates(
        table_rows=table_rows,
        row_classification=row_classification,
        type_diagnostics=type_diagnostics,
        validation_report=validation_report,
    )

    assert result["candidate_count"] == 1
    assert result["summary"] == {"error": 0, "warning": 1, "info": 0}
    assert result["candidates"][0]["severity"] == "warning"
    assert result["candidates"][0]["reasons"][0]["code"] == "summary_row"


def test_build_quarantine_candidates_from_type_diagnostics() -> None:
    table_rows = [
        {"amount": "100"},
        {"amount": "unknown"},
    ]
    row_classification = {"suspicious_rows": []}
    type_diagnostics = {
        "mixed_type_columns": [
            {
                "column": "amount",
                "dominant_type": "float",
                "invalid_values": [
                    {
                        "row_index": 1,
                        "value": "unknown",
                    }
                ],
            }
        ]
    }
    validation_report = {"failed_results": []}

    result = build_quarantine_candidates(
        table_rows=table_rows,
        row_classification=row_classification,
        type_diagnostics=type_diagnostics,
        validation_report=validation_report,
    )

    assert result["candidate_count"] == 1
    assert result["candidates"][0]["row_index"] == 1
    assert result["candidates"][0]["severity"] == "warning"
    assert result["candidates"][0]["reasons"][0]["source"] == "type_diagnostics"
    assert result["candidates"][0]["reasons"][0]["column"] == "amount"


def test_build_quarantine_candidates_groups_multiple_reasons_by_row() -> None:
    table_rows = [
        {"email": "invalid-email", "amount": "unknown"},
    ]
    row_classification = {
        "suspicious_rows": [
            {
                "row_index": 0,
                "classification": "garbage_row",
                "reason": "Only one value is populated in a multi-column row.",
            }
        ]
    }
    type_diagnostics = {
        "mixed_type_columns": [
            {
                "column": "amount",
                "dominant_type": "float",
                "invalid_values": [
                    {"row_index": 0, "value": "unknown"},
                ],
            }
        ]
    }
    validation_report = {
        "failed_results": [
            {
                "row_index": 0,
                "column_name": "email",
                "constraint_type": "regex_pattern",
                "message": "Value does not match pattern.",
                "value": "invalid-email",
            }
        ]
    }

    result = build_quarantine_candidates(
        table_rows=table_rows,
        row_classification=row_classification,
        type_diagnostics=type_diagnostics,
        validation_report=validation_report,
    )

    assert result["candidate_count"] == 1
    assert result["summary"] == {"error": 1, "warning": 0, "info": 0}
    assert result["candidates"][0]["severity"] == "error"
    assert result["candidates"][0]["reason_count"] == 3


def test_build_quarantine_candidates_returns_empty_report_without_reasons() -> None:
    result = build_quarantine_candidates(
        table_rows=[{"customer_id": "1"}],
        row_classification={"suspicious_rows": []},
        type_diagnostics={"mixed_type_columns": []},
        validation_report={"failed_results": []},
    )

    assert result == {
        "candidate_count": 0,
        "summary": {"error": 0, "warning": 0, "info": 0},
        "candidates": [],
    }


def test_build_quarantine_candidates_does_not_mutate_rows() -> None:
    table_rows = [{"email": "invalid-email"}]
    original_rows = [row.copy() for row in table_rows]

    build_quarantine_candidates(
        table_rows=table_rows,
        row_classification={"suspicious_rows": []},
        type_diagnostics={"mixed_type_columns": []},
        validation_report={
            "failed_results": [
                {
                    "row_index": 0,
                    "column_name": "email",
                    "constraint_type": "regex_pattern",
                    "message": "Value does not match pattern.",
                    "value": "invalid-email",
                }
            ]
        },
    )

    assert table_rows == original_rows
