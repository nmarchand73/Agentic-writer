"""Usage ledger and pricing helpers."""

import pytest
from decimal import Decimal

from pydantic_ai.usage import RunUsage

from agentic_writer.openai_pricing import model_ref_for_pricing
from agentic_writer.usage_cost import UsageLedger, format_token_count


pytestmark = pytest.mark.unit


def test_format_token_count():
    assert format_token_count(1500) == "1.5k"
    assert format_token_count(2_000_000) == "2.00M"


def test_ledger_accumulates_tokens():
    ledger = UsageLedger()
    ledger.record("a", "openai-chat:gpt-4o-mini", RunUsage(input_tokens=100, output_tokens=20, requests=1))
    ledger.record("b", "openai-chat:gpt-4o-mini", RunUsage(input_tokens=50, output_tokens=10, requests=1))
    assert ledger.total.input_tokens == 150
    assert ledger.total.output_tokens == 30
    assert ledger.total.requests == 2


def test_ledger_summary_includes_cost_when_priced(monkeypatch):
    ledger = UsageLedger()

    def fake_estimate(usage: RunUsage, model: str) -> tuple[Decimal | None, str]:
        return Decimal("0.0100"), "openai_docs"

    monkeypatch.setattr("agentic_writer.usage_cost.estimate_cost_usd", fake_estimate)
    ledger.record("x", "gpt-4o", RunUsage(input_tokens=1000, output_tokens=100, requests=1))
    assert "≈ $0.0100" in ledger.summary()
