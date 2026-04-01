"""KDE Plasma / KWin tweaks on top of the shared layer-shell GTK path."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gi.repository import Gtk

from raintux.wayland.layer_window import LayerShellWindow
from raintux.wayland.wlr_backend import create_overlay_window

if TYPE_CHECKING:
    pass

log = logging.getLogger(__name__)


def create_kde_overlay(app: Gtk.Application, **kwargs: object) -> LayerShellWindow:
    """
    Create a Plasma-friendly overlay window.

    TODO: Apply KWin-specific margin/anchor heuristics and optional
    ``org.kde.plasmashell`` D-Bus fallback when layer-shell is unavailable.
    """
    win = create_overlay_window(app, **kwargs)  # type: ignore[arg-type]
    log.debug("KDE overlay created (shared WLR GTK layer path)")
    return win
