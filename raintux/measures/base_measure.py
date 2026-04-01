"""Abstract measure: async polling loop driven by :class:`~raintux.core.measure_manager.MeasureManager`."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


class BaseMeasure(ABC):
    """One logical data source (CPU, time, …) backing meters."""

    def __init__(
        self,
        *,
        name: str,
        section: dict[str, str],
        skin_root: Path,
        interval_ms: int,
    ) -> None:
        self.name = name
        self.section = section
        self.skin_root = skin_root.resolve()
        self.interval_ms = max(50, interval_ms)
        self._value: Any = None

    @property
    def value(self) -> Any:
        """Last polled value (type is measure-specific)."""
        return self._value

    async def update(self) -> None:
        """Poll once; exceptions are logged by the manager loop."""
        self._value = await self._poll()

    @abstractmethod
    async def _poll(self) -> Any:
        """Compute the next measurement (run potentially blocking work in a thread)."""

    def display_string(self) -> str:
        """Default string form for meter text substitution."""
        if self._value is None:
            return ""
        return str(self._value)
