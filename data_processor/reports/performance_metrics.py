"""
Performance metrics helpers.

These helpers collect optional timing information for pipeline stages. They are
not used unless explicitly requested by the pipeline caller.
"""

from contextlib import contextmanager
from time import perf_counter
from typing import Iterator


class PerformanceTimer:
    """
    Collect named duration measurements.
    """

    def __init__(self) -> None:
        """Initialize an empty timer."""
        self.timings: dict[str, float] = {}

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        """
        Measure one named block.
        """
        started_at = perf_counter()

        try:
            yield

        finally:
            self.timings[name] = self.timings.get(name, 0.0) + (
                perf_counter() - started_at
            )

    def to_dict(self) -> dict[str, float]:
        """
        Return collected timings.
        """
        return dict(self.timings)
