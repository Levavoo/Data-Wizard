"""
Encoding detection utility for CSV input.

This module uses a conservative, dependency-free strategy. It attempts a small
ordered list of encodings and returns diagnostics rather than only a string.
"""

from pathlib import Path
from typing import Any

DEFAULT_ENCODING_CANDIDATES = (
    "utf-8-sig",
    "utf-8",
    "cp1252",
    "latin-1",
)


def detect_text_encoding(
    path: str | Path,
    candidates: tuple[str, ...] | None = None,
    sample_size: int = 8192,
) -> dict[str, Any]:
    """
    Detect a readable text encoding for a file.

    Args:
        path:
            Source file path.

        candidates:
            Optional ordered encoding candidates.

        sample_size:
            Number of bytes to sample.

    Returns:
        Encoding detection diagnostics.

    Raises:
        ValueError:
            If no candidate can decode the sample.
    """
    if candidates is None:
        candidates = DEFAULT_ENCODING_CANDIDATES

    file_path = Path(path)
    sample = file_path.read_bytes()[:sample_size]
    candidate_results = []

    for encoding in candidates:
        try:
            sample.decode(encoding)
            result = {
                "encoding": encoding,
                "success": True,
                "error": None,
            }
            candidate_results.append(result)

            return {
                "selected_encoding": encoding,
                "candidate_results": candidate_results,
                "confidence": _confidence_for_encoding(encoding, sample),
                "reason": _reason_for_encoding(encoding, sample),
            }

        except UnicodeDecodeError as error:
            candidate_results.append(
                {
                    "encoding": encoding,
                    "success": False,
                    "error": str(error),
                }
            )

    raise ValueError(f"Unable to decode text file: {file_path}")


def _confidence_for_encoding(encoding: str, sample: bytes) -> str:
    """
    Return a simple confidence label for the selected encoding.
    """
    if sample.startswith(b"\xef\xbb\xbf") and encoding == "utf-8-sig":
        return "high"

    if encoding in {"utf-8", "utf-8-sig"}:
        return "high"

    if encoding == "cp1252":
        return "medium"

    return "low"


def _reason_for_encoding(encoding: str, sample: bytes) -> str:
    """
    Return a human-readable reason for the selected encoding.
    """
    if sample.startswith(b"\xef\xbb\xbf") and encoding == "utf-8-sig":
        return "UTF-8 byte order mark detected."

    if encoding in {"utf-8", "utf-8-sig"}:
        return "Sample decoded successfully with UTF-8 compatible encoding."

    if encoding == "cp1252":
        return "UTF-8 decoding failed and sample decoded with cp1252."

    return "Fallback encoding decoded the sample."
