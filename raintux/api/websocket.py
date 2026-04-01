"""WebSocket helpers for pushing live skin events to the Skin Manager UI."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastapi import FastAPI


async def broadcast(app: FastAPI, event: str, payload: dict[str, Any]) -> None:
    """Fan-out JSON messages to connected /ws clients."""
    clients = getattr(app.state, "ws_clients", set())
    if not clients:
        return
    msg = json.dumps({"event": event, "data": payload})
    dead: set[Any] = set()
    for ws in clients:
        try:
            await ws.send_text(msg)
        except Exception:
            dead.add(ws)
    for ws in dead:
        clients.discard(ws)


def broadcast_threadsafe(app: FastAPI, event: str, payload: dict[str, Any]) -> None:
    """Schedule :func:`broadcast` from a non-async context (best-effort)."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(broadcast(app, event, payload))
    except RuntimeError:
        pass
