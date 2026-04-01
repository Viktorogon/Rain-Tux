"""Rotating image / needle meter — Phase 2."""

from __future__ import annotations

import cairo

from raintux.meters.base_meter import MeterLayout


def draw_rotator_meter(cr: cairo.Context, layout: MeterLayout) -> None:
    """TODO: bind rotation angle to measure value."""
    _ = cr, layout
