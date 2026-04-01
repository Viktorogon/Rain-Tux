"""Open-Meteo weather (Phase 2 — no API key)."""

from __future__ import annotations

from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class WeatherMeasure(BaseMeasure):
    """HTTP fetch + JSON parse via aiohttp; TODO."""

    async def _poll(self) -> str:
        return "—"
