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
    - parse CSV rows
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

        with self.file_path.open(
            mode="r",
            encoding=encoding,
            newline="",
        ) as csv_file:
            reader = csv.DictReader(
                csv_file,
                delimiter=delimiter,
            )

            if reader.fieldnames is None:
                raise ValueError("CSV file does not contain headers.")

            normalized_headers = [
                self._normalize_header(header) for header in reader.fieldnames
            ]

            schema = self._build_schema(
                original_headers=reader.fieldnames,
                normalized_headers=normalized_headers,
            )

            table = Table(
                name=self.source_name(),
                schema=schema,
            )

            for raw_row in reader:
                normalized_row = self._normalize_row(
                    row=raw_row,
                    normalized_headers=normalized_headers,
                )

                table.add_row(normalized_row)

            table.add_metadata("source_format", "csv")
            table.add_metadata("encoding", encoding)
            table.add_metadata("delimiter", delimiter)

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

    def _normalize_header(self, header: str) -> str:
        """
        Normalize a CSV header into an internal column name.

        Args:
            header:
                Raw CSV header.

        Returns:
            Normalized header name.
        """
        return header.strip().lower().replace(" ", "_")

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
        row: dict[str, str | None],
        normalized_headers: list[str],
    ) -> dict[str, str | None]:
        """
        Normalize one CSV row.

        Args:
            row:
                Raw CSV row.

            normalized_headers:
                Internal header names.

        Returns:
            Normalized row dictionary.
        """
        normalized_row: dict[str, str | None] = {}

        for original_header, normalized_header in zip(
            row.keys(),
            normalized_headers,
            strict=True,
        ):
            value = row[original_header]

            normalized_row[normalized_header] = value

        return normalized_row
