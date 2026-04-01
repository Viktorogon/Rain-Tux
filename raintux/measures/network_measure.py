"""Network I/O measure (Phase 2: psutil net_io_counters + deltas)."""

from __future__ import annotations

from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class NetworkMeasure(BaseMeasure):
    """``Type=Net`` / NetIn / NetOut — TODO implement delta smoothing."""

    def __init__(self, *, name: str, section: dict[str, str], skin_root: Path, interval_ms: int) -> None:
        super().__init__(name=name, section=section, skin_root=skin_root, interval_ms=interval_ms)

    async def _poll(self) -> float:
        # TODO: track interface totals and format bits/sec as Rainmeter does
        return 0.0
