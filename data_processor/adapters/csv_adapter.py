"""
CSV adapter.

Reads CSV files and converts them into the canonical internal Table model.

This adapter is intentionally limited to parsing and structural conversion.
It does not clean values, infer types, validate constraints, or export data.
"""

import csv
from typing import Any

from data_processor.adapters.base_adapter import BaseAdapter
from data_processor.adapters.delimiter_detection import detect_delimiter
from data_processor.adapters.encoding_detection import detect_text_encoding
from data_processor.adapters.parse_diagnostics import ParseDiagnostics
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


class CsvAdapter(BaseAdapter):
    """
    CSV file adapter.

    Responsibilities:
    - validate source file
    - detect or use configured encoding
    - detect or use configured delimiter
    - detect likely header row
    - preserve pre-header metadata rows
    - parse CSV rows
    - normalize headers
    - make duplicate headers unique
    - create Schema
    - create Table
    - attach parse diagnostics

    Not responsible for:
    - cleaning
    - type inference
    - validation
    - transformations
    """

    supported_extensions = (".csv",)

    def __init__(
        self,
        file_path,
        encoding: str | None = None,
        delimiter: str | None = None,
        auto_detect: bool = True,
    ) -> None:
        """
        Initialize the CSV adapter.

        Args:
            file_path:
                Source CSV path.

            encoding:
                Optional explicit text encoding.

            delimiter:
                Optional explicit CSV delimiter.

            auto_detect:
                Whether missing encoding/delimiter values should be detected.
        """
        super().__init__(file_path)
        self.encoding_override = encoding
        self.delimiter_override = delimiter
        self.auto_detect = auto_detect
        self.detection_diagnostics: dict[str, Any] = {}

    def read(self) -> Table:
        """
        Read the CSV file into the internal Table model.

        Returns:
            Parsed Table object.

        Raises:
            ValueError:
                If the CSV cannot be parsed.
        """
        self.validate_file()

        encoding = self._resolve_encoding()
        delimiter = self._resolve_delimiter(encoding)

        rows = self._read_rows(
            encoding=encoding,
            delimiter=delimiter,
        )

        if not rows:
            raise ValueError("CSV file is empty.")

        header_row_index = self._detect_header_row_index(rows)
        original_headers = rows[header_row_index]

        if not original_headers:
            raise ValueError("CSV file does not contain headers.")

        data_rows = rows[header_row_index + 1 :]
        preamble_rows = rows[:header_row_index]

        normalized_headers = self._normalize_headers(original_headers)
        parse_diagnostics = self._build_parse_diagnostics(
            rows=rows,
            original_headers=original_headers,
            normalized_headers=normalized_headers,
            header_row_index=header_row_index,
            preamble_rows=preamble_rows,
            delimiter=delimiter,
            encoding=encoding,
        )

        schema = self._build_schema(
            original_headers=original_headers,
            normalized_headers=normalized_headers,
        )

        table = Table(
            name=self.source_name(),
            schema=schema,
        )

        for raw_row in data_rows:
            normalized_row = self._normalize_row(
                raw_row=raw_row,
                normalized_headers=normalized_headers,
            )

            table.add_row(normalized_row)

        table.add_metadata("source_format", "csv")
        table.add_metadata("encoding", encoding)
        table.add_metadata("delimiter", delimiter)
        table.add_metadata("header_row_index", header_row_index)
        table.add_metadata("preamble_rows", preamble_rows)
        table.add_metadata("parse_diagnostics", parse_diagnostics.to_dict())

        return table

    def _resolve_encoding(self) -> str:
        """
        Resolve explicit or detected encoding.
        """
        if self.encoding_override is not None:
            diagnostics = {
                "selected_encoding": self.encoding_override,
                "candidate_results": [],
                "confidence": "override",
                "reason": "Explicit encoding override was provided.",
            }
            self.detection_diagnostics["encoding"] = diagnostics
            self._validate_encoding(self.encoding_override)
            return self.encoding_override

        if not self.auto_detect:
            diagnostics = {
                "selected_encoding": "utf-8",
                "candidate_results": [],
                "confidence": "default",
                "reason": "Auto-detection disabled; using UTF-8 default.",
            }
            self.detection_diagnostics["encoding"] = diagnostics
            self._validate_encoding("utf-8")
            return "utf-8"

        diagnostics = detect_text_encoding(self.file_path)
        self.detection_diagnostics["encoding"] = diagnostics
        return diagnostics["selected_encoding"]

    def _resolve_delimiter(self, encoding: str) -> str:
        """
        Resolve explicit or detected delimiter.
        """
        if self.delimiter_override is not None:
            diagnostics = {
                "selected_delimiter": self.delimiter_override,
                "candidate_scores": [],
                "confidence": "override",
                "reason": "Explicit delimiter override was provided.",
            }
            self.detection_diagnostics["delimiter"] = diagnostics
            return self.delimiter_override

        if not self.auto_detect:
            diagnostics = {
                "selected_delimiter": ",",
                "candidate_scores": [],
                "confidence": "default",
                "reason": "Auto-detection disabled; using comma default.",
            }
            self.detection_diagnostics["delimiter"] = diagnostics
            return ","

        sample = self._read_text_sample(encoding)
        diagnostics = detect_delimiter(sample)
        self.detection_diagnostics["delimiter"] = diagnostics
        return diagnostics["selected_delimiter"]

    def _validate_encoding(self, encoding: str) -> None:
        """
        Validate that the selected encoding can read the file sample.
        """
        with self.file_path.open(mode="r", encoding=encoding) as test_file:
            test_file.read(2048)

    def _read_text_sample(self, encoding: str) -> str:
        """
        Read a text sample for delimiter detection.
        """
        with self.file_path.open(mode="r", encoding=encoding) as csv_file:
            return csv_file.read(4096)

    def _read_rows(
        self,
        encoding: str,
        delimiter: str,
    ) -> list[list[str]]:
        """
        Read all CSV rows.

        Args:
            encoding:
                File encoding.

            delimiter:
                CSV delimiter.

        Returns:
            List of CSV rows.
        """
        with self.file_path.open(
            mode="r",
            encoding=encoding,
            newline="",
        ) as csv_file:
            reader = csv.reader(
                csv_file,
                delimiter=delimiter,
                skipinitialspace=True,
            )

            return list(reader)

    def _detect_header_row_index(
        self,
        rows: list[list[str]],
    ) -> int:
        """
        Detect the most likely header row.

        Heuristic:
        - prefer the first row with more than one field
        - require at least one following row with the same field count
        - fall back to the first row if no stronger candidate exists

        This supports files with metadata/preamble lines before the header
        while avoiding accidental selection of a single malformed data row.
        """
        for index, row in enumerate(rows):
            field_count = len(row)

            if field_count <= 1:
                continue

            following_rows = rows[index + 1 :]

            has_matching_data_row = any(
                len(following_row) == field_count for following_row in following_rows
            )

            if has_matching_data_row:
                return index

        return 0

    def _normalize_header(self, header: str) -> str:
        """
        Normalize a CSV header into an internal column name.

        Args:
            header:
                Raw CSV header.

        Returns:
            Normalized header name.
        """
        normalized_header = header.strip().lower().replace(" ", "_")

        if not normalized_header:
            return "unnamed_column"

        return normalized_header

    def _normalize_headers(
        self,
        headers: list[str],
    ) -> list[str]:
        """
        Normalize CSV headers and make duplicates unique.

        Args:
            headers:
                Raw CSV headers.

        Returns:
            Unique normalized headers.
        """
        normalized_headers: list[str] = []
        header_counts: dict[str, int] = {}

        for header in headers:
            normalized_header = self._normalize_header(header)

            current_count = header_counts.get(
                normalized_header,
                0,
            )

            if current_count == 0:
                unique_header = normalized_header

            else:
                unique_header = f"{normalized_header}_{current_count + 1}"

            header_counts[normalized_header] = current_count + 1
            normalized_headers.append(unique_header)

        return normalized_headers

    def _build_parse_diagnostics(
        self,
        rows: list[list[str]],
        original_headers: list[str],
        normalized_headers: list[str],
        header_row_index: int,
        preamble_rows: list[list[str]],
        delimiter: str,
        encoding: str,
    ) -> ParseDiagnostics:
        """
        Build parser diagnostics from raw CSV structure.
        """
        diagnostics = ParseDiagnostics(
            header_row_index=header_row_index,
            preamble_row_count=len(preamble_rows),
            delimiter=delimiter,
            encoding=encoding,
            detection=self.detection_diagnostics,
        )

        header_count = len(normalized_headers)
        diagnostics.empty_headers = [
            index for index, header in enumerate(original_headers) if not header.strip()
        ]
        diagnostics.duplicate_headers = self._find_duplicate_headers(original_headers)

        if header_row_index > 0:
            diagnostics.add_warning("Header row was not the first source row.")

        if diagnostics.empty_headers:
            diagnostics.add_warning("One or more headers were empty.")

        if diagnostics.duplicate_headers:
            diagnostics.add_warning("One or more headers were duplicated.")

        for source_row_index, raw_row in enumerate(
            rows[header_row_index + 1 :],
            start=header_row_index + 1,
        ):
            row_field_count = len(raw_row)

            if row_field_count > header_count:
                diagnostics.add_extra_fields(
                    row_index=source_row_index,
                    count=row_field_count - header_count,
                )

            elif row_field_count < header_count:
                diagnostics.add_missing_fields(
                    row_index=source_row_index,
                    count=header_count - row_field_count,
                )

        if diagnostics.rows_with_extra_fields:
            diagnostics.add_warning("One or more rows contain extra fields.")

        if diagnostics.rows_with_missing_fields:
            diagnostics.add_warning("One or more rows contain missing fields.")

        return diagnostics

    def _find_duplicate_headers(
        self,
        headers: list[str],
    ) -> list[str]:
        """
        Find duplicated headers after standard header normalization.
        """
        seen: set[str] = set()
        duplicates: list[str] = []

        for header in headers:
            normalized_header = self._normalize_header(header)

            if normalized_header in seen and normalized_header not in duplicates:
                duplicates.append(normalized_header)

            seen.add(normalized_header)

        return duplicates

    def _build_schema(
        self,
        original_headers: list[str],
        normalized_headers: list[str],
    ) -> Schema:
        """
        Build a schema from CSV headers.
        """
        schema = Schema()

        for original, normalized in zip(
            original_headers,
            normalized_headers,
            strict=True,
        ):
            column = Column(
                name=normalized,
                original_name=original,
            )

            schema.add_column(column)

        return schema

    def _normalize_row(
        self,
        raw_row: list[str],
        normalized_headers: list[str],
    ) -> dict[str, str | None]:
        """
        Normalize one CSV row.
        """
        normalized_row: dict[str, str | None] = {}

        for index, normalized_header in enumerate(normalized_headers):
            value = raw_row[index] if index < len(raw_row) else None
            normalized_row[normalized_header] = value

        return normalized_row
