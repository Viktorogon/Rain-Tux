"""Text meter (``Meter=String``) via PangoCairo."""

from __future__ import annotations

import logging
from collections.abc import Callable

import cairo
from gi.repository import Pango, PangoCairo

from raintux.meters.base_meter import MeterLayout, rgba_from_rainmeter, substitute_measures

log = logging.getLogger(__name__)


def draw_string_meter(
    cr: cairo.Context,
    layout: MeterLayout,
    get_measure: Callable[[str], str],
) -> None:
    """Draw anti-aliased UTF-8 text with optional shadow (basic)."""
    cf = {k.lower(): v for k, v in layout.raw.items()}
    text_key = "text" if "text" in cf else "string"
    raw_text = cf.get(text_key, "")
    text = substitute_measures(raw_text, get_measure)

    font = cf.get("fontface", "Sans")
    size = float(cf.get("fontsize", "12"))
    color_s = cf.get("fontcolor", "255,255,255,255")
    r, g, b, a = rgba_from_rainmeter(color_s)

    shadow = cf.get("stringeffect", "").lower() == "shadow"
    if shadow:
        sr, sg, sb, sa = rgba_from_rainmeter(cf.get("fonteffectcolor", "0,0,0,200"))
        desc = Pango.FontDescription.from_string(f"{font} {size:g}")
        pl = PangoCairo.create_layout(cr)
        pl.set_font_description(desc)
        pl.set_text(text, -1)
        cr.save()
        cr.translate(layout.x + 1, layout.y + 1)
        cr.set_source_rgba(sr, sg, sb, sa)
        PangoCairo.show_layout(cr, pl)
        cr.restore()

    desc = Pango.FontDescription.from_string(f"{font} {size:g}")
    pl = PangoCairo.create_layout(cr)
    pl.set_font_description(desc)
    pl.set_text(text, -1)
    cr.save()
    cr.translate(layout.x, layout.y)
    cr.set_source_rgba(r, g, b, a)
    PangoCairo.show_layout(cr, pl)
    cr.restore()
