"""Restricted Lua execution environment for ``Script`` measures — Phase 2."""

from __future__ import annotations

from typing import Any


class LuaSandbox:
    """TODO: wrap lupa LuaRuntime with stripped globals and CPU/time limits."""

    def __init__(self) -> None:
        self._runtime: Any | None = None

    def eval_chunk(self, source: str) -> Any:
        """Compile and run Lua source in the sandbox — TODO."""
        raise NotImplementedError("Lua sandbox (Phase 2)")
