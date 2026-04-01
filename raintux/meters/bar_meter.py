"""Progress ``Meter=Bar`` (horizontal / vertical)."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable

import cairo

from raintux.meters.base_meter import MeterLayout, rgba_from_rainmeter, substitute_measures

log = logging.getLogger(__name__)


def _parse_percent(metric_val: str) -> float:
    m = re.search(r"([-+]?[0-9]*\.?[0-9]+)", metric_val)
    if not m:
        return 0.0
    v = float(m.group(1))
    return max(0.0, min(100.0, v))


def draw_bar_meter(cr: cairo.Context, layout: MeterLayout, get_measure: Callable[[str], str]) -> None:
    """Draw a filled bar from a bound ``MeasureName`` (0–100)."""
    cf = {k.lower(): v for k, v in layout.raw.items()}
    measure = substitute_measures(cf.get("measurename", ""), get_measure).strip()
    raw = get_measure(measure) if measure else "0"
    pct = _parse_percent(raw)

    orient = cf.get("barorientation", "horizontal").lower()
    bg = rgba_from_rainmeter(cf.get("solidcolor", "40,40,40,180"))
    fg = rgba_from_rainmeter(cf.get("barcolor", "200,80,80,255"))

    x, y, w, h = float(layout.x), float(layout.y), float(layout.w or 100), float(layout.h or 10)
    cr.save()
    cr.rectangle(x, y, w, h)
    cr.set_source_rgba(*bg)
    cr.fill()
    if orient.startswith("v"):
        fill_h = h * (pct / 100.0)
        cr.rectangle(x, y + (h - fill_h), w, fill_h)
    else:
        fill_w = w * (pct / 100.0)
        cr.rectangle(x, y, fill_w, h)
    cr.set_source_rgba(*fg)
    cr.fill()
    cr.restore()
