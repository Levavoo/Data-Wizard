"""
HTML report exporter.

This module writes rendered HTML report strings to UTF-8 files.
"""

from pathlib import Path


def export_report_to_html(
    html_report: str,
    output_path: str | Path,
    encoding: str = "utf-8",
) -> None:
    """
    Export an HTML report string to a file.

    Args:
        html_report:
            Rendered HTML report string.

        output_path:
            Target HTML output path.

        encoding:
            Output file encoding.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_report, encoding=encoding)
