import json
from pathlib import Path

from data_processor.exporters.quarantine_json_exporter import (
    export_quarantine_candidates_to_json,
)


def test_export_quarantine_candidates_to_json_writes_file(tmp_path: Path) -> None:
    output_path = tmp_path / "reports" / "quarantine_candidates.json"
    quarantine_candidates = {
        "candidate_count": 1,
        "summary": {"error": 1, "warning": 0, "info": 0},
        "candidates": [
            {
                "row_index": 1,
                "severity": "error",
                "reason_count": 1,
                "reasons": [],
                "row": {"email": "invalid-email"},
            }
        ],
    }

    export_quarantine_candidates_to_json(
        quarantine_candidates=quarantine_candidates,
        output_path=output_path,
    )

    assert output_path.exists()

    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert exported == quarantine_candidates


def test_export_quarantine_candidates_to_json_creates_parent_directories(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "nested" / "reports" / "quarantine_candidates.json"

    export_quarantine_candidates_to_json(
        quarantine_candidates={
            "candidate_count": 0,
            "summary": {"error": 0, "warning": 0, "info": 0},
            "candidates": [],
        },
        output_path=output_path,
    )

    assert output_path.exists()
