"""wlroots-oriented backend: GTK4 + layer-shell (Hyprland, Sway, many others)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gi.repository import Gtk

from raintux.wayland.compositor_detect import CompositorKind, detect_compositor, registry_has_layer_shell
from raintux.wayland.layer_window import LayerShellWindow

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


def create_overlay_window(
    app: Gtk.Application,
    *,
    title: str,
    width: int,
    height: int,
    skin_id: str,
) -> LayerShellWindow:
    """
    Create a layer-surface backed window when the compositor exposes layer-shell.

    Phase 1 uses ``Gtk4LayerShell``; raw ``pywayland`` layer setup remains a TODO
    for headless / non-GTK embedding.
    """
    kind = detect_compositor()
    has_ls = registry_has_layer_shell()
    if kind == CompositorKind.UNKNOWN and not has_ls:
        log.warning("Compositor unknown and layer-shell not detected — window may not sit on desktop layer")
    return LayerShellWindow(app, title=title, width=width, height=height, namespace=skin_id[:64])
