"""
Base adapter interface.

This module defines the abstract adapter contract used by all input adapters.
Every format-specific adapter should inherit from BaseAdapter and implement
the read method.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from data_processor.core.table import Table


class BaseAdapter(ABC):
    """
    Abstract base class for file format adapters.

    Adapters are responsible only for converting external data formats into
    the internal Table model.

    They should not clean, validate, transform, or export data.
    """

    supported_extensions: tuple[str, ...] = ()

    def __init__(self, file_path: str | Path) -> None:
        """
        Initialize the adapter.

        Args:
            file_path:
                Path to the source file.
        """
        self.file_path = Path(file_path)

    def validate_file(self) -> None:
        """
        Validate that the source file exists and has a supported extension.

        Raises:
            FileNotFoundError:
                If the source file does not exist.

            ValueError:
                If the file extension is not supported by the adapter.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File does not exist: {self.file_path}")

        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

        if self.supported_extensions:
            extension = self.file_path.suffix.lower()

            if extension not in self.supported_extensions:
                raise ValueError(
                    f"Unsupported file extension '{extension}'. "
                    f"Supported extensions: {self.supported_extensions}"
                )

    def source_name(self) -> str:
        """
        Return a readable source name based on the file name.

        Returns:
            File stem without extension.
        """
        return self.file_path.stem

    @abstractmethod
    def read(self) -> Table:
        """
        Read the source file and return an internal Table.

        Returns:
            Table object containing parsed source data.
        """
        raise NotImplementedError
