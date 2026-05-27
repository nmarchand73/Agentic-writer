#!/usr/bin/env python3
"""Fetch OpenAI API pricing docs and write bundled JSON.

Source: https://developers.openai.com/api/docs/pricing
Uses the Standard tier rows embedded in the page HTML (first price per model).
"""

from __future__ import annotations

import argparse
import html as html_module
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PRICING_URL = "https://developers.openai.com/api/docs/pricing"
OUTPUT = Path(__file__).resolve().parents[1] / "src/agentic_writer/data/openai_pricing.json"

# [1,[[0,"model"],[0,input],[0,cached|""|null],[0,output]]]
_ROW_RE = re.compile(
    r'\[1,\[\[0,"([^"]+)"\],'
    r"\[(?:0,([\d.]+)|1,null)\],"
    r'\[(?:0,([\d.]+)|0,""|1,null)\],'
    r"\[(?:0,([\d.]+)|1,null)\]\]\]"
)


def _model_key(name: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", name.strip()).lower()


def parse_pricing_html(html: str) -> dict[str, dict[str, float | None]]:
    text = html_module.unescape(html)
    models: dict[str, dict[str, float | None]] = {}
    for name, inp, cached, out in _ROW_RE.findall(text):
        key = _model_key(name)
        if key in models:
            continue
        if not inp or not out:
            continue
        models[key] = {
            "input": float(inp),
            "cached_input": float(cached) if cached else None,
            "output": float(out),
        }
    return models


def fetch_html(url: str = PRICING_URL) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "agentic-writer/0.1 (+https://github.com/nmarchand73/Agentic-writer)"
            ),
            "Accept": "text/html",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def build_table(html: str, *, source: str = PRICING_URL) -> dict[str, object]:
    models = parse_pricing_html(html)
    if not models:
        raise RuntimeError("No model rows parsed — page format may have changed")
    return {
        "source": source,
        "tier": "standard",
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "models": models,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        help="Local HTML file instead of fetching the URL",
    )
    parser.add_argument(
        "--url",
        default=PRICING_URL,
        help=f"Pricing page URL (default: {PRICING_URL})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUTPUT,
        help=f"Output JSON path (default: {OUTPUT})",
    )
    args = parser.parse_args()

    if args.input:
        html = args.input.read_text(encoding="utf-8")
        source = str(args.input)
    else:
        print(f"Fetching {args.url}…", file=sys.stderr)
        html = fetch_html(args.url)
        source = args.url

    table = build_table(html, source=source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(table['models'])} models → {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
