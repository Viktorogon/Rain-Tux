"""Disk free / used via psutil."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import psutil

from raintux.measures.base_measure import BaseMeasure


class DiskMeasure(BaseMeasure):
    """``Type=FreeDisk`` / ``Type=Disk`` — percent free or used for a path."""

    def __init__(self, *, name: str, section: dict[str, str], skin_root: Path, interval_ms: int) -> None:
        super().__init__(name=name, section=section, skin_root=skin_root, interval_ms=interval_ms)
        cf = {k.lower(): v for k, v in section.items()}
        drive = cf.get("drive", "/").strip('"')
        if len(drive) == 2 and drive[1] == ":":
            # Windows-style path in skin — map to POSIX root for Phase 1
            self._path = "/" if drive.lower().startswith("c") else "/home"
        else:
            self._path = drive or "/"
        self._show_free = "free" in (cf.get("type") or "").lower() or cf.get("type", "").lower() == "freedisk"

    async def _poll(self) -> float:
        def read() -> float:
            path = self._path
            if not Path(path).exists():
                path = os.path.expanduser("~")
            usage = psutil.disk_usage(path)
            if self._show_free:
                return float(usage.free) / float(usage.total) * 100.0
            return float(usage.used) / float(usage.total) * 100.0

        return await asyncio.to_thread(read)

    def display_string(self) -> str:
        if self._value is None:
            return "0"
        return f"{float(self._value):.0f}"
