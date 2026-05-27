"""Studio progress bridge — interleaved SSE events."""

from __future__ import annotations

import asyncio

import pytest

from agentic_writer.api.studio_progress import StudioProgressBridge


async def _collect(stream):
    return [item async for item in stream]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_interleave_yields_progress_before_primary_finishes():
    bridge = StudioProgressBridge()

    async def primary():
        await asyncio.sleep(0.05)
        yield "a"
        await asyncio.sleep(0.05)
        yield "b"

    async def emit_progress():
        await asyncio.sleep(0.01)
        bridge.emit_nowait("p1")
        await asyncio.sleep(0.05)
        bridge.emit_nowait("p2")

    progress_task = asyncio.create_task(emit_progress())
    events = await _collect(bridge.interleave(primary()))
    await progress_task

    assert events.index("p1") < events.index("a")
    assert events.index("p2") < events.index("b")
