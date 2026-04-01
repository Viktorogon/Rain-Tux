"""Vector ``Meter=Shape`` drawing (rectangle / ellipse subset)."""

from __future__ import annotations

import logging
import re

import cairo

from raintux.meters.base_meter import MeterLayout, rgba_from_rainmeter

log = logging.getLogger(__name__)


def _shape_tokens(raw_shape: str) -> list[str]:
    return [t.strip() for t in raw_shape.split("|") if t.strip()]


def draw_shape_meter(cr: cairo.Context, layout: MeterLayout) -> None:
    """
    Rainmeter ``Shape`` pipeline subset: ``Rectangle x,y,w,h`` and ``Ellipse``.

    Also honors ``Meter=Shape`` with ``Shape=Rectangle`` and X,Y,W,H from keys.
    """
    cf = {k.lower(): v for k, v in layout.raw.items()}
    shape = cf.get("shape", "rectangle").strip()
    fill = cf.get("fill", "fill color")
    # Parse Fill Color r,g,b,a
    color = "255,255,255,200"
    m = re.search(r"fill color\s+([^|]+)", fill, re.I)
    if m:
        color = m.group(1).strip()
    elif "fillColor".lower() in "".join(cf.keys()):
        pass
    r, g, b, a = rgba_from_rainmeter(color)

    cr.save()
    cr.translate(layout.x, layout.y)
    w, h = float(layout.w or 1), float(layout.h or 1)

    kind = shape.split()[0].lower() if shape else "rectangle"
    tokens = _shape_tokens(shape)

    if kind == "ellipse" or (tokens and tokens[0].lower() == "ellipse"):
        cr.scale(1.0, 1.0)
        cr.translate(w / 2.0, h / 2.0)
        cr.scale(w / 2.0, h / 2.0)
        cr.arc(0, 0, 1, 0, 6.283185307179586)
    else:
        cr.rectangle(0, 0, w, h)

    cr.set_source_rgba(r, g, b, a)
    cr.fill()
    cr.restore()
