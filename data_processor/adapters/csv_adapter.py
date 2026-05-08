"""
CSV adapter.

Reads CSV files and converts them into the canonical internal Table model.

This adapter is intentionally limited to parsing and structural conversion.
It does not clean values, infer types, validate constraints, or export data.
"""

import csv

from data_processor.adapters.base_adapter import BaseAdapter
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


class CsvAdapter(BaseAdapter):
    """
    CSV file adapter.

    Responsibilities:
    - validate source file
    - detect encoding fallback
    - detect delimiter
    - detect likely header row
    - preserve pre-header metadata rows
    - parse CSV rows
    - normalize headers
    - make duplicate headers unique
    - create Schema
    - create Table

    Not responsible for:
    - cleaning
    - type inference
    - validation
    - transformations
    """

    supported_extensions = (".csv",)

    ENCODINGS = (
        "utf-8",
        "utf-8-sig",
        "cp1252",
    )

    DELIMITER_CANDIDATES = (
        ",",
        ";",
        "\t",
        "|",
    )

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

        encoding = self._detect_encoding()
        delimiter = self._detect_delimiter(encoding)

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

        return table

    def _detect_encoding(self) -> str:
        """
        Detect a working text encoding.

        Returns:
            Valid encoding string.

        Raises:
            ValueError:
                If no encoding works.
        """
        for encoding in self.ENCODINGS:
            try:
                with self.file_path.open(
                    mode="r",
                    encoding=encoding,
                ) as test_file:
                    test_file.read(2048)

                return encoding

            except UnicodeDecodeError:
                continue

        raise ValueError(f"Unable to decode CSV file: {self.file_path}")

    def _detect_delimiter(self, encoding: str) -> str:
        """
        Detect the CSV delimiter.

        Args:
            encoding:
                Working file encoding.

        Returns:
            Detected delimiter.
        """
        with self.file_path.open(
            mode="r",
            encoding=encoding,
        ) as csv_file:
            sample = csv_file.read(4096)

        try:
            dialect = csv.Sniffer().sniff(
                sample,
                delimiters=self.DELIMITER_CANDIDATES,
            )

            return dialect.delimiter

        except csv.Error:
            return ","

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

    def _build_schema(
        self,
        original_headers: list[str],
        normalized_headers: list[str],
    ) -> Schema:
        """
        Build a schema from CSV headers.

        Args:
            original_headers:
                Raw CSV headers.

            normalized_headers:
                Normalized internal headers.

        Returns:
            Schema object.
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

        Args:
            raw_row:
                Raw CSV row as a list of values.

            normalized_headers:
                Internal unique header names.

        Returns:
            Normalized row dictionary.
        """
        normalized_row: dict[str, str | None] = {}

        for index, normalized_header in enumerate(normalized_headers):
            value = raw_row[index] if index < len(raw_row) else None
            normalized_row[normalized_header] = value

        return normalized_row
