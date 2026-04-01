"""MPRIS2 / D-Bus now-playing (Phase 2 — playerctl-style)."""

from __future__ import annotations

from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class NowPlayingMeasure(BaseMeasure):
    """Expose title/artist from `org.mpris.MediaPlayer2` — TODO."""

    async def _poll(self) -> str:
        return ""
