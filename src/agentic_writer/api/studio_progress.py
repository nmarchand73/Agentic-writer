"""Live AG-UI state events during long-running studio tools."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextvars import ContextVar, Token
from typing import Any

try:
    from ag_ui.core import BaseEvent
except ImportError:  # pragma: no cover
    BaseEvent = Any  # type: ignore[misc, assignment]

_SENTINEL = object()

_bridge_var: ContextVar[StudioProgressBridge | None] = ContextVar(
    "studio_progress_bridge",
    default=None,
)


class StudioProgressBridge:
    """Queue AG-UI events from tools; merge into the SSE stream while the agent runs."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[Any] = asyncio.Queue()

    def emit_nowait(self, event: BaseEvent) -> None:
        self._queue.put_nowait(event)

    async def close(self) -> None:
        await self._queue.put(_SENTINEL)

    async def interleave(
        self,
        primary: AsyncIterator[BaseEvent],
    ) -> AsyncIterator[BaseEvent]:
        """Yield primary stream events and queued progress events as they arrive."""
        primary_iter = primary.__aiter__()
        primary_done = False
        primary_error: BaseException | None = None
        primary_task: asyncio.Task[BaseEvent | None] | None = None

        async def _next_primary() -> BaseEvent | None:
            nonlocal primary_done, primary_error
            try:
                return await primary_iter.__anext__()
            except StopAsyncIteration:
                primary_done = True
                return None
            except BaseException as exc:
                primary_done = True
                primary_error = exc
                return None

        def _start_primary() -> None:
            nonlocal primary_task
            if not primary_done and primary_task is None:
                primary_task = asyncio.create_task(_next_primary())

        progress_task: asyncio.Task[Any] | None = None

        while True:
            _start_primary()
            if progress_task is None or progress_task.done():
                progress_task = asyncio.create_task(self._queue.get())

            wait_for: set[asyncio.Task[Any]] = {progress_task}
            if primary_task is not None and not primary_task.done():
                wait_for.add(primary_task)

            done, pending = await asyncio.wait(wait_for, return_when=asyncio.FIRST_COMPLETED)

            if progress_task in done:
                item = progress_task.result()
                progress_task = None
                if item is _SENTINEL:
                    if primary_done:
                        break
                    continue
                yield item
                continue

            if primary_task is not None and primary_task in done:
                if progress_task in pending:
                    progress_task.cancel()
                    progress_task = None
                event = primary_task.result()
                primary_task = None
                if primary_error is not None:
                    raise primary_error
                if event is not None:
                    yield event
                elif primary_done:
                    while True:
                        try:
                            item = self._queue.get_nowait()
                        except asyncio.QueueEmpty:
                            break
                        if item is not _SENTINEL:
                            yield item
                    break


def set_studio_progress_bridge(bridge: StudioProgressBridge | None) -> Token:
    return _bridge_var.set(bridge)


def reset_studio_progress_bridge(token: Token) -> None:
    _bridge_var.reset(token)


def get_studio_progress_bridge() -> StudioProgressBridge | None:
    return _bridge_var.get()
