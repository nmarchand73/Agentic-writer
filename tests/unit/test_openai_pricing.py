"""OpenAI docs pricing table and cost estimation."""

from decimal import Decimal

import pytest
from pydantic_ai.usage import RunUsage

from agentic_writer.openai_pricing import (
    clear_pricing_cache,
    estimate_cost_from_openai_pricing,
    load_pricing_table,
    model_ref_for_pricing,
    resolve_model_rates,
)

pytestmark = pytest.mark.unit

SAMPLE_TABLE = {
    "source": "test",
    "models": {
        "gpt-4.1-mini": {"input": 0.4, "cached_input": 0.1, "output": 1.6},
        "gpt-4o-mini": {"input": 0.15, "cached_input": 0.075, "output": 0.6},
    },
}


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_pricing_cache()
    yield
    clear_pricing_cache()


def test_model_ref_for_pricing_strips_prefix():
    assert model_ref_for_pricing("openai-chat:gpt-4.1-mini") == "gpt-4.1-mini"


def test_bundled_table_has_project_models():
    table = load_pricing_table()
    models = table["models"]
    assert "gpt-4.1-mini" in models
    assert "gpt-4.1-nano" in models


def test_resolve_model_rates_dated_snapshot():
    rates = resolve_model_rates("gpt-4.1-mini-2025-04-14", SAMPLE_TABLE)
    assert rates is not None
    assert rates.input_per_1m == Decimal("0.4")
    assert rates.output_per_1m == Decimal("1.6")
    assert rates.cached_input_per_1m == Decimal("0.1")


def test_estimate_cost_basic():
    usage = RunUsage(input_tokens=1_000_000, output_tokens=500_000, requests=1)
    cost = estimate_cost_from_openai_pricing(
        usage, "openai-chat:gpt-4o-mini", table=SAMPLE_TABLE
    )
    assert cost == Decimal("0.450000")


def test_estimate_cost_cached_input():
    usage = RunUsage(
        input_tokens=1_000_000,
        output_tokens=0,
        cache_read_tokens=200_000,
        requests=1,
    )
    cost = estimate_cost_from_openai_pricing(
        usage, "gpt-4.1-mini", table=SAMPLE_TABLE
    )
    assert cost == Decimal("0.340000")
