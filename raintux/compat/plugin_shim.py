"""Map Windows-only Rainmeter plugin measure names to Linux equivalents."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginMapping:
    """Windows plugin id → RainTux measure type / notes."""

    windows_name: str
    linux_type: str
    notes: str = ""


# TODO: extend from community feedback / skin corpus analysis.
PLUGIN_MAP: dict[str, PluginMapping] = {
    "nowplaying": PluginMapping("NowPlaying", "NowPlaying", "MPRIS2 via D-Bus"),
    "win7audio": PluginMapping("Win7Audio", "PipeWire", "pulsectl / pipewire-python"),
    "radeon": PluginMapping("Radeon", "SysInfo", "GPU stats — vendor-specific"),
}


def map_plugin_name(windows_plugin: str) -> PluginMapping | None:
    """Return a mapping when the Windows plugin has a Linux strategy."""
    key = windows_plugin.strip().lower()
    return PLUGIN_MAP.get(key)
