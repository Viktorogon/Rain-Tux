"""Scrolling histogram meter (``Meter=Histogram``) — Phase 2."""

from __future__ import annotations

import cairo

from raintux.meters.base_meter import MeterLayout


def draw_histogram_meter(cr: cairo.Context, layout: MeterLayout) -> None:
    """TODO: ring buffer of samples, Cairo path fill."""
    _ = cr, layout
