"""CPU utilization via psutil."""

from __future__ import annotations

import asyncio
from pathlib import Path

import psutil

from raintux.measures.base_measure import BaseMeasure


class CpuMeasure(BaseMeasure):
    """``Type=CPU`` — percent busy, non-blocking poll."""

    def __init__(self, *, name: str, section: dict[str, str], skin_root: Path, interval_ms: int) -> None:
        super().__init__(name=name, section=section, skin_root=skin_root, interval_ms=interval_ms)
        self._first = True

    async def _poll(self) -> float:
        # First instant sample may be 0; subsequent calls use short interval in a worker thread.
        interval = 0.05 if not self._first else None
        self._first = False

        def read() -> float:
            return float(psutil.cpu_percent(interval=interval))

        return await asyncio.to_thread(read)

    def display_string(self) -> str:
        if self._value is None:
            return "0"
        return f"{float(self._value):.0f}"
