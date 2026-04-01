"""Physical RAM / swap usage via psutil."""

from __future__ import annotations

import asyncio
from pathlib import Path

import psutil

from raintux.measures.base_measure import BaseMeasure


class RamMeasure(BaseMeasure):
    """``Type=Memory`` or ``Type=Swap`` style metrics."""

    def __init__(self, *, name: str, section: dict[str, str], skin_root: Path, interval_ms: int) -> None:
        super().__init__(name=name, section=section, skin_root=skin_root, interval_ms=interval_ms)
        cf = {k.lower(): v for k, v in section.items()}
        mtype = (cf.get("type") or "").lower()
        self._swap = "swap" in mtype

    async def _poll(self) -> float:
        def read() -> float:
            if self._swap:
                s = psutil.swap_memory()
                return float(s.percent)
            m = psutil.virtual_memory()
            return float(m.percent)

        return await asyncio.to_thread(read)

    def display_string(self) -> str:
        if self._value is None:
            return "0"
        return f"{float(self._value):.0f}"
