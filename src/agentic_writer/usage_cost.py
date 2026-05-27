"""Token usage and USD estimates for pipeline runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from pydantic_ai.usage import RunUsage

from agentic_writer.openai_pricing import estimate_cost_from_openai_pricing


def estimate_cost_usd(usage: RunUsage, model: str) -> tuple[Decimal | None, str]:
    """Return (USD total, pricing source id) for this usage chunk."""
    cost = estimate_cost_from_openai_pricing(usage, model)
    if cost is not None:
        return cost, "openai_docs"
    return None, "unknown"


def format_token_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


@dataclass
class UsageLedger:
    """Cumulative usage and cost across pipeline LLM calls."""

    total: RunUsage = field(default_factory=RunUsage)
    total_cost_usd: Decimal = field(default_factory=lambda: Decimal("0"))
    _priced: bool = field(default=False, repr=False)
    pricing_source: str = field(default="unknown", repr=False)

    def record(self, label: str, model: str, run_usage: RunUsage) -> str:
        """Add one agent run; return a one-line summary for logs / UI."""
        self.total += run_usage
        chunk_cost, source = estimate_cost_usd(run_usage, model)
        if chunk_cost is not None:
            self.total_cost_usd += chunk_cost
            self._priced = True
            if self.pricing_source == "unknown" and source != "unknown":
                self.pricing_source = source
        return self.summary(prefix=f"{label} · ")

    def summary(self, *, prefix: str = "") -> str:
        parts = [
            f"{format_token_count(self.total.input_tokens)} in",
            f"{format_token_count(self.total.output_tokens)} out",
            f"{self.total.requests} req",
        ]
        if self._priced:
            src = (
                "tarifs OpenAI"
                if self.pricing_source == "openai_docs"
                else "estimation"
            )
            parts.append(f"≈ ${self.total_cost_usd:.4f} ({src})")
        else:
            parts.append("(prix USD non estimé)")
        return prefix + " · ".join(parts)

    def as_state_fields(self) -> dict[str, float | int | None]:
        return {
            "usage_input_tokens": self.total.input_tokens,
            "usage_output_tokens": self.total.output_tokens,
            "usage_requests": self.total.requests,
            "estimated_cost_usd": float(self.total_cost_usd) if self._priced else None,
        }
