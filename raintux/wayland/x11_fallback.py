"""X11 / XWayland fallback using EWMH desktop-type hints (optional)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

log = logging.getLogger(__name__)


class X11FallbackHints:
    """
    Apply ``_NET_WM_WINDOW_TYPE_DESKTOP`` and stickiness hints under X11.

    TODO: wire python-xlib / ewmh once an X11 GDK surface is available.
    """

    def __init__(self, window_id: int | None = None) -> None:
        self._xid = window_id

    def apply(self) -> None:
        """No-op stub until X11 properties are set from GDK surface."""
        log.debug("X11 fallback hints not applied (stub), xid=%s", self._xid)
