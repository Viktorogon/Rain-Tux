"""Normalize Rainmeter-style .ini files for cross-platform loading."""

from __future__ import annotations

import re
from pathlib import Path


_WIN_PATH_SEP = re.compile(r"\\+")


def normalize_text(text: str) -> str:
    """Strip BOM, normalize newlines, fix Windows path separators in values."""
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines_out: list[str] = []
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped and not stripped.startswith(";") and "=" in stripped:
            key, _sep, value = stripped.partition("=")
            key = key.rstrip()
            value = value.strip()
            if any(ch in value for ch in ("\\", "/")):
                value = _WIN_PATH_SEP.sub("/", value)
            line = f"{key}={value}"
        lines_out.append(line)
    return "\n".join(lines_out)


def read_ini_normalized(path: Path) -> str:
    """Read UTF-8 (with optional BOM) and return normalized content."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1", errors="replace")
    return normalize_text(text)
