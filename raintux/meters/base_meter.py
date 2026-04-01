"""Shared Cairo drawing helpers for skin meters."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cairo

log = logging.getLogger(__name__)


def rgba_from_rainmeter(color: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    """Parse ``R,G,B[,A]`` (0-255) or ``#RRGGBB`` into Cairo floats."""
    color = color.strip()
    if color.startswith("#") and len(color) >= 7:
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        a = alpha
        if len(color) >= 9:
            a = int(color[7:9], 16) / 255.0
        return (r, g, b, a)
    parts = [p.strip() for p in color.split(",")]
    try:
        r = int(parts[0]) / 255.0
        g = int(parts[1]) / 255.0
        b = int(parts[2]) / 255.0
        a = int(parts[3]) / 255.0 if len(parts) > 3 else alpha
        return (r, g, b, a)
    except (ValueError, IndexError):
        log.debug("bad color %r, default white", color)
        return (1.0, 1.0, 1.0, alpha)


def substitute_measures(text: str, get_measure: Any) -> str:
    """Replace ``[MeasureName]`` with string values."""
    if not text:
        return text

    def repl(m: re.Match[str]) -> str:
        return get_measure(m.group(1))

    return re.sub(r"\[([^\]]+)\]", repl, text)


def parse_coord(value: str, axis: str, prev_right: int, prev_bottom: int, fallback: int = 0) -> int:
    """
    Parse Rainmeter ``X`` / ``Y``.

    ``X=…R`` is relative to the previous meter's **right** edge; ``Y=…B`` to its
    **bottom** edge (Rainmeter semantics).
    """
    value = value.strip()
    if axis == "x" and value.endswith(("R", "r")):
        prefix = value[:-1]
        off = int(float(prefix)) if prefix else 0
        return prev_right + off
    if axis == "y" and value.endswith(("B", "b")):
        prefix = value[:-1]
        off = int(float(prefix)) if prefix else 0
        return prev_bottom + off
    try:
        return int(float(value))
    except ValueError:
        return fallback


@dataclass
class MeterLayout:
    """Resolved geometry in Cairo device pixels."""

    name: str
    mtype: str
    x: int
    y: int
    w: int
    h: int
    raw: dict[str, str]
