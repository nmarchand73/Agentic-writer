"""Run pydantic-ai agents and record usage for cost tracking."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from agentic_writer.log_config import get_logger
from agentic_writer.usage_cost import UsageLedger

if TYPE_CHECKING:
    from pydantic_ai import Agent

log = get_logger("pipeline")


async def run_agent_tracked(
    agent: Agent[Any, Any],
    prompt: str,
    *,
    ledger: UsageLedger,
    label: str,
    model: str,
    on_usage: Callable[[UsageLedger], Awaitable[None] | None] | None = None,
) -> Any:
    """Call ``agent.run``, log progressive cost, return result."""
    result = await agent.run(prompt)
    detail = ledger.record(label, model, result.usage)
    log.info("Coût cumulé — {}", detail)
    if on_usage is not None:
        hook = on_usage(ledger)
        if hook is not None:
            await hook
    return result
