"""Embedded Lua via lupa (Phase 2)."""

from __future__ import annotations

from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class LuaMeasure(BaseMeasure):
    """Run sandboxed Lua scripts — TODO :mod:`raintux.compat.lua_sandbox`."""

    async def _poll(self) -> str:
        return ""
