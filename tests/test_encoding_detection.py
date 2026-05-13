from pathlib import Path

from data_processor.adapters.encoding_detection import detect_text_encoding


def test_detect_text_encoding_detects_utf8(tmp_path: Path) -> None:
    path = tmp_path / "utf8.csv"
    path.write_text("Name,City\nAlice,München\n", encoding="utf-8")

    result = detect_text_encoding(path)

    assert result["selected_encoding"] in {"utf-8", "utf-8-sig"}
    assert result["confidence"] == "high"


def test_detect_text_encoding_detects_utf8_bom(tmp_path: Path) -> None:
    path = tmp_path / "utf8_bom.csv"
    path.write_text("Name,City\nAlice,Berlin\n", encoding="utf-8-sig")

    result = detect_text_encoding(path)

    assert result["selected_encoding"] == "utf-8-sig"
    assert result["confidence"] == "high"
    assert "byte order mark" in result["reason"]


def test_detect_text_encoding_falls_back_to_cp1252(tmp_path: Path) -> None:
    path = tmp_path / "cp1252.csv"
    path.write_bytes("Name,City\nAlice,Düsseldorf – West\n".encode("cp1252"))

    result = detect_text_encoding(path)

    assert result["selected_encoding"] == "cp1252"
    assert result["confidence"] == "medium"
    assert result["candidate_results"][0]["success"] is False


def test_detect_text_encoding_allows_custom_candidates(tmp_path: Path) -> None:
    path = tmp_path / "latin1.csv"
    path.write_bytes("Name,City\nAlice,Café\n".encode("latin-1"))

    result = detect_text_encoding(path, candidates=("latin-1",))

    assert result["selected_encoding"] == "latin-1"
