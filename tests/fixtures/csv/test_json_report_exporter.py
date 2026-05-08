import json
from datetime import date
from datetime import datetime
from pathlib import Path

from data_processor.exporters.json_report_exporter import (
    export_report_to_json,
    serialize_report_value,
)


def test_serialize_date() -> None:
    """
    Verify date values are serialized as ISO strings.
    """
    result = serialize_report_value(date(2026, 1, 31))

    assert result == "2026-01-31"


def test_serialize_datetime() -> None:
    """
    Verify datetime values are serialized as ISO strings.
    """
    result = serialize_report_value(datetime(2026, 1, 31, 14, 30, 0))

    assert result == "2026-01-31 14:30:00"


def test_serialize_set() -> None:
    """
    Verify sets are serialized deterministically.
    """
    result = serialize_report_value({"b", "a"})

    assert result == "['a', 'b']"


def test_serialize_unsupported_value() -> None:
    """
    Verify unsupported values raise TypeError.
    """
    try:
        serialize_report_value(object())

    except TypeError:
        assert True
        return

    assert False, "Expected TypeError was not raised."


def test_export_report_to_json(tmp_path: Path) -> None:
    """
    Verify report export creates a JSON file.
    """
    report = {
        "table_name": "customers",
        "row_count": 2,
        "generated_at": datetime(2026, 1, 31, 14, 30, 0),
        "columns": ["name", "country"],
    }

    output_path = tmp_path / "report.json"

    export_report_to_json(
        report=report,
        output_path=output_path,
    )

    assert output_path.exists()

    loaded_report = json.loads(output_path.read_text(encoding="utf-8"))

    assert loaded_report["table_name"] == "customers"
    assert loaded_report["row_count"] == 2
    assert loaded_report["generated_at"] == "2026-01-31 14:30:00"


def test_export_report_creates_directories(tmp_path: Path) -> None:
    """
    Verify missing output directories are created automatically.
    """
    report = {
        "table_name": "customers",
    }

    output_path = tmp_path / "nested" / "reports" / "quality_report.json"

    export_report_to_json(
        report=report,
        output_path=output_path,
    )

    assert output_path.exists()
