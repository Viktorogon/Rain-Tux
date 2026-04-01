"""Bitmap meter (``Meter=Image``) using Cairo image surfaces."""

from __future__ import annotations

import logging
from pathlib import Path

import cairo

from raintux.meters.base_meter import MeterLayout

log = logging.getLogger(__name__)


def draw_image_meter(cr: cairo.Context, layout: MeterLayout, root: Path) -> None:
    """Load ``ImageName`` (PNG preferred) scaled into ``W``×``H`` when set."""
    cf = {k.lower(): v for k, v in layout.raw.items()}
    name = cf.get("imagename", "")
    if not name:
        return
    path = (root / name).resolve()
    if not path.is_file():
        log.warning("missing image %s", path)
        return
    try:
        if path.suffix.lower() == ".png":
            surf = cairo.ImageSurface.create_from_png(str(path))
        else:
            from io import BytesIO

            from PIL import Image

            im = Image.open(path).convert("RGBA")
            bio = BytesIO()
            im.save(bio, format="PNG")
            bio.seek(0)
            surf = cairo.ImageSurface.create_from_png(bio)
    except Exception:
        log.exception("image load failed %s", path)
        return

    cr.save()
    cr.translate(layout.x, layout.y)
    sw, sh = surf.get_width(), surf.get_height()
    tw, th = layout.w or sw, layout.h or sh
    if tw and th and (tw != sw or th != sh):
        cr.scale(tw / float(sw), th / float(sh))
    cr.set_source_surface(surf, 0, 0)
    cr.paint_with_alpha(1.0)
    cr.restore()
