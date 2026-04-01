"""GNOME Wayland: detect helper extension and fall back to plain GTK overlay."""

from __future__ import annotations

import logging
from typing import Any

from gi.repository import Gtk

from raintux.wayland.layer_window import LayerShellWindow

log = logging.getLogger(__name__)


def gnome_helper_available() -> bool:
    """
    Return True if ``org.raintux.GnomeHelper`` is reachable on the session bus.

    TODO: implement the companion GNOME Shell extension (Phase 4).
    """
    try:
        import dbus

        bus = dbus.SessionBus()
        return bool(bus.name_has_owner("org.raintux.GnomeHelper"))
    except Exception:
        return False


def create_gnome_overlay(app: Gtk.Application, **kwargs: Any) -> LayerShellWindow:
    """GNOME cannot use wlr-layer-shell for arbitrary clients — transparent GTK window for now."""
    if gnome_helper_available():
        log.info("org.raintux.GnomeHelper present — TODO wire D-Bus positioning")
    return LayerShellWindow(app, **kwargs)
