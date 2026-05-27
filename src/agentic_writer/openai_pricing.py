"""OpenAI token pricing from bundled JSON (see ``data/openai_pricing.json``).

Refresh with: ``uv run python scripts/refresh_openai_pricing.py``
Source: https://developers.openai.com/api/docs/pricing
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
from importlib import resources
from pathlib import Path

from pydantic_ai.usage import RunUsage

_PRICING_FILE = "openai_pricing.json"


@dataclass(frozen=True)
class ModelRates:
    """USD per 1M tokens."""

    input_per_1m: Decimal
    output_per_1m: Decimal
    cached_input_per_1m: Decimal | None = None


def model_ref_for_pricing(model: str) -> str:
    """Strip pydantic-ai provider prefix."""
    for prefix in ("openai-chat:", "openai-responses:", "openai:"):
        if model.startswith(prefix):
            return model.removeprefix(prefix)
    return model


def _pricing_path() -> Path:
    return Path(__file__).resolve().parent / "data" / _PRICING_FILE


@lru_cache(maxsize=1)
def load_pricing_table() -> dict[str, object]:
    """Load ``data/openai_pricing.json`` shipped with the package."""
    path = _pricing_path()
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    raw = resources.files("agentic_writer.data").joinpath(_PRICING_FILE).read_text(
        encoding="utf-8"
    )
    return json.loads(raw)


def clear_pricing_cache() -> None:
    """Invalidate cached table (tests)."""
    load_pricing_table.cache_clear()


def _lookup_keys(model_ref: str) -> list[str]:
    ref = model_ref.strip().lower()
    keys = [ref]
    undated = re.sub(r"-\d{4}-\d{2}-\d{2}.*$", "", ref)
    if undated != ref:
        keys.append(undated)
    return keys


def resolve_model_rates(
    model_ref: str, table: dict[str, object] | None = None
) -> ModelRates | None:
    data = table if table is not None else load_pricing_table()
    models = data.get("models")
    if not isinstance(models, dict):
        return None
    for key in _lookup_keys(model_ref):
        entry = models.get(key)
        if not isinstance(entry, dict):
            continue
        inp, out = entry.get("input"), entry.get("output")
        if inp is None or out is None:
            continue
        cached = entry.get("cached_input")
        return ModelRates(
            input_per_1m=Decimal(str(inp)),
            output_per_1m=Decimal(str(out)),
            cached_input_per_1m=(
                Decimal(str(cached)) if cached is not None else None
            ),
        )
    return None


def estimate_cost_from_openai_pricing(
    usage: RunUsage,
    model: str,
    *,
    table: dict[str, object] | None = None,
) -> Decimal | None:
    """Estimate USD from bundled OpenAI docs pricing."""
    rates = resolve_model_rates(model_ref_for_pricing(model), table)
    if rates is None:
        return None

    million = Decimal("1000000")
    cache_read = usage.cache_read_tokens
    non_cached_in = max(0, usage.input_tokens - cache_read)

    cost = (Decimal(non_cached_in) / million) * rates.input_per_1m
    if cache_read > 0:
        cache_rate = rates.cached_input_per_1m or rates.input_per_1m
        cost += (Decimal(cache_read) / million) * cache_rate
    cost += (Decimal(usage.output_tokens) / million) * rates.output_per_1m
    return cost.quantize(Decimal("0.000001"))
