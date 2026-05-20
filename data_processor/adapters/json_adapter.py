"""
JSON adapter.

Reads supported JSON files and converts them into the canonical internal Table
model.
"""

import json
from typing import Any

from data_processor.adapters.base_adapter import BaseAdapter
from data_processor.adapters.json_parse_diagnostics import JsonParseDiagnostics
from data_processor.core.column import Column
from data_processor.core.schema import Schema
from data_processor.core.table import Table


class JsonAdapter(BaseAdapter):
    """
    JSON file adapter.

    Supported first scope:
    - root value is a list
    - every list item is an object
    - object keys become columns
    - missing keys become None
    - nested objects/arrays become compact JSON strings and diagnostics
    """

    supported_extensions = (".json",)

    def read(self) -> Table:
        """
        Read the JSON file into the internal Table model.
        """
        self.validate_file()
        payload = self._read_payload()

        if not isinstance(payload, list):
            raise ValueError("JSON root must be a list of objects.")

        diagnostics = JsonParseDiagnostics(
            root_type="list",
            record_count=len(payload),
        )

        invalid_indexes = [
            index for index, item in enumerate(payload) if not isinstance(item, dict)
        ]

        for index in invalid_indexes:
            diagnostics.add_invalid_record_index(index)

        if invalid_indexes:
            raise ValueError(
                "JSON root must be a list of objects. "
                f"Invalid record indexes: {invalid_indexes}"
            )

        records: list[dict[str, Any]] = payload
        original_keys = self._collect_keys(records)
        normalized_keys = self._normalize_keys(original_keys)
        diagnostics.column_count = len(normalized_keys)
        diagnostics.missing_key_counts = self._missing_key_counts(
            records=records,
            original_keys=original_keys,
        )

        schema = self._build_schema(
            original_keys=original_keys,
            normalized_keys=normalized_keys,
        )
        table = Table(
            name=self.source_name(),
            schema=schema,
        )

        for record in records:
            table.add_row(
                self._normalize_record(
                    record=record,
                    original_keys=original_keys,
                    normalized_keys=normalized_keys,
                    diagnostics=diagnostics,
                )
            )

        if diagnostics.nested_value_columns:
            diagnostics.add_warning("Nested object values were converted to JSON strings.")

        if diagnostics.array_value_columns:
            diagnostics.add_warning("Array values were converted to JSON strings.")

        table.add_metadata("source_format", "json")
        table.add_metadata("parse_diagnostics", diagnostics.to_dict())

        return table

    def _read_payload(self) -> Any:
        """
        Read and decode JSON payload.
        """
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON file: {self.file_path}") from error

    def _collect_keys(self, records: list[dict[str, Any]]) -> list[str]:
        """
        Collect the union of object keys while preserving first-seen order.
        """
        keys: list[str] = []

        for record in records:
            for key in record:
                if key not in keys:
                    keys.append(key)

        return keys

    def _normalize_key(self, key: str) -> str:
        """
        Normalize a JSON key into an internal column name.
        """
        normalized_key = key.strip().lower().replace(" ", "_")

        if not normalized_key:
            return "unnamed_column"

        return normalized_key

    def _normalize_keys(self, keys: list[str]) -> list[str]:
        """
        Normalize keys and make duplicate normalized names unique.
        """
        normalized_keys: list[str] = []
        key_counts: dict[str, int] = {}

        for key in keys:
            normalized_key = self._normalize_key(key)
            current_count = key_counts.get(normalized_key, 0)

            if current_count == 0:
                unique_key = normalized_key
            else:
                unique_key = f"{normalized_key}_{current_count + 1}"

            key_counts[normalized_key] = current_count + 1
            normalized_keys.append(unique_key)

        return normalized_keys

    def _missing_key_counts(
        self,
        records: list[dict[str, Any]],
        original_keys: list[str],
    ) -> dict[str, int]:
        """
        Count missing keys per original key.
        """
        return {
            key: sum(1 for record in records if key not in record)
            for key in original_keys
            if any(key not in record for record in records)
        }

    def _build_schema(
        self,
        original_keys: list[str],
        normalized_keys: list[str],
    ) -> Schema:
        """
        Build schema from JSON keys.
        """
        schema = Schema()

        for original, normalized in zip(original_keys, normalized_keys, strict=True):
            schema.add_column(
                Column(
                    name=normalized,
                    original_name=original,
                )
            )

        return schema

    def _normalize_record(
        self,
        record: dict[str, Any],
        original_keys: list[str],
        normalized_keys: list[str],
        diagnostics: JsonParseDiagnostics,
    ) -> dict[str, Any]:
        """
        Convert one JSON object into a normalized table row.
        """
        normalized_record: dict[str, Any] = {}

        for original_key, normalized_key in zip(
            original_keys,
            normalized_keys,
            strict=True,
        ):
            value = record.get(original_key)
            normalized_record[normalized_key] = self._normalize_value(
                value=value,
                column_name=normalized_key,
                diagnostics=diagnostics,
            )

        return normalized_record

    def _normalize_value(
        self,
        value: Any,
        column_name: str,
        diagnostics: JsonParseDiagnostics,
    ) -> Any:
        """
        Normalize unsupported nested JSON values into compact JSON strings.
        """
        if isinstance(value, dict):
            diagnostics.add_nested_value_column(column_name)
            return json.dumps(value, separators=(",", ":"), ensure_ascii=False)

        if isinstance(value, list):
            diagnostics.add_array_value_column(column_name)
            return json.dumps(value, separators=(",", ":"), ensure_ascii=False)

        return value
