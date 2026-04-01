"""Local time / date string formatting."""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class TimeMeasure(BaseMeasure):
    """``Type=Time`` — formats with Rainmeter-like ``Format=`` (subset of strftime)."""

    def __init__(self, *, name: str, section: dict[str, str], skin_root: Path, interval_ms: int) -> None:
        super().__init__(name=name, section=section, skin_root=skin_root, interval_ms=interval_ms)
        cf = {k.lower(): v for k, v in section.items()}
        self._fmt = cf.get("format", "%H:%M:%S").replace("#CRLF#", "\n")

    async def _poll(self) -> str:
        def read() -> str:
            return datetime.now().strftime(self._fmt)

        return await asyncio.to_thread(read)

    def display_string(self) -> str:
        if self._value is None:
            return ""
        return str(self._value)
