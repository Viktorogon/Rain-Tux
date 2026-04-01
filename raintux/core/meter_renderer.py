"""Lay out meters and paint them to a Cairo context."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

import cairo

from raintux.core.skin_parser import ParsedSkin
from raintux.meters.bar_meter import draw_bar_meter
from raintux.meters.base_meter import MeterLayout, parse_coord
from raintux.meters.image_meter import draw_image_meter
from raintux.meters.shape_meter import draw_shape_meter
from raintux.meters.string_meter import draw_string_meter

if TYPE_CHECKING:
    pass

log = logging.getLogger(__name__)


def compute_layout(parsed: ParsedSkin) -> list[MeterLayout]:
    """
    Compute pixel layout for each meter in skin order.

    ``W``/``H`` default heuristically by meter kind when unset.
    """
    prev_r = 0
    prev_b = 0
    prev_x = 0
    prev_y = 0
    prev_w = 0
    prev_h = 0

    out: list[MeterLayout] = []
    for name, section in parsed.meters:
        cf = {k.lower(): v for k, v in section.items()}
        expanded: dict[str, str] = {}
        for k, v in section.items():
            expanded[k] = parsed.variable_text(v)
        ecf = {k.lower(): v for k, v in expanded.items()}
        mtype = ecf.get("meter", "string").strip().lower()

        def gx(key: str, default: str) -> str:
            return ecf.get(key.lower(), default)

        x_s, y_s = gx("x", "0"), gx("y", "0")
        w_s, h_s = gx("w", "120"), gx("h", "30")

        x = parse_coord(x_s, "x", prev_r, prev_b, prev_x)
        y = parse_coord(y_s, "y", prev_r, prev_b, prev_y)

        try:
            w = int(float(w_s))
        except ValueError:
            w = 120
        try:
            h = int(float(h_s))
        except ValueError:
            h = 30

        if mtype == "image":
            w = int(float(w_s)) if w_s else 0
            h = int(float(h_s)) if h_s else 0
        if mtype == "bar":
            w, h = int(float(w_s or 150)), int(float(h_s or 14))

        out.append(MeterLayout(name=name, mtype=mtype, x=x, y=y, w=w, h=h, raw=expanded))
        prev_x, prev_y = x, y
        prev_w, prev_h = w, h
        prev_r = x + w
        prev_b = y + h
    return out


def render_skin(
    cr: cairo.Context,
    parsed: ParsedSkin,
    get_measure: Callable[[str], str],
    layouts: list[MeterLayout] | None = None,
) -> None:
    """Paint all meters for the given skin."""
    lays = layouts or compute_layout(parsed)
    cr.save()
    cr.set_operator(cairo.OPERATOR_OVER)
    for layout in lays:
        try:
            if layout.mtype == "string":
                draw_string_meter(cr, layout, get_measure)
            elif layout.mtype == "image":
                draw_image_meter(cr, layout, parsed.root)
            elif layout.mtype in ("shape", "roundline"):
                draw_shape_meter(cr, layout)
            elif layout.mtype == "bar":
                draw_bar_meter(cr, layout, get_measure)
            else:
                log.debug("unknown meter type %s [%s]", layout.mtype, layout.name)
        except Exception:
            log.exception("meter render failed %s", layout.name)
    cr.restore()
