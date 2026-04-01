"""Load optional ``launch.env`` from the repository root (KEY=VALUE lines)."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Parent of the ``raintux`` package (project root in editable installs)."""
    return Path(__file__).resolve().parent.parent


def load_launch_env() -> None:
    """
    Apply ``launch.env`` so variables like ``RAINTUX_SPLASH_GIF`` are set.

    Does not override variables already present in the process environment.
    """
    path = repo_root() / "launch.env"
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            continue
        key, _, val = s.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and val and key not in os.environ:
            os.environ[key] = val
