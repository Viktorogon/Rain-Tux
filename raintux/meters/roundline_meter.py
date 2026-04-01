"""Circular roundline gauge — Phase 2."""

from __future__ import annotations

import cairo

from raintux.meters.base_meter import MeterLayout


def draw_roundline_meter(cr: cairo.Context, layout: MeterLayout) -> None:
    """TODO: arc stroke with start/end angles from measures."""
    _ = cr, layout
