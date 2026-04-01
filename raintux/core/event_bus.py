"""Lightweight publish/subscribe bus for measure → meter update notifications."""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

log = logging.getLogger(__name__)

Subscriber = Callable[[str, Any], Awaitable[None] | None]


class EventBus:
    """Async-friendly pub/sub keyed by topic (e.g. measure name or `skin:refresh`)."""

    def __init__(self) -> None:
        self._subs: dict[str, list[Subscriber]] = defaultdict(list)
        self._lock = asyncio.Lock()

    def subscribe(self, topic: str, callback: Subscriber) -> None:
        """Register a callback for a topic."""
        self._subs[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Subscriber) -> None:
        """Remove a callback; no-op if missing."""
        if topic not in self._subs:
            return
        try:
            self._subs[topic].remove(callback)
        except ValueError:
            pass

    async def publish(self, topic: str, payload: Any = None) -> None:
        """Notify subscribers; await async handlers sequentially."""
        async with self._lock:
            handlers = list(self._subs.get(topic, ()))
        for handler in handlers:
            try:
                result = handler(topic, payload)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                log.exception("event handler failed topic=%s", topic)
