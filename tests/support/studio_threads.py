"""Helpers BDD — format JSON identique à web/lib/thread-persistence.ts."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any


def thread_file_path(threads_dir: Path, thread_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", thread_id)
    return threads_dir / f"{safe}.json"


def save_thread_fixture(
    threads_dir: Path,
    thread_id: str,
    user_message: str,
    *,
    name: str | None = None,
) -> Path:
    threads_dir.mkdir(parents=True, exist_ok=True)
    title = name if name is not None else _display_title(user_message)
    payload: dict[str, Any] = {
        "threadId": thread_id,
        "name": title,
        "historicRuns": [
            {
                "threadId": thread_id,
                "runId": "bdd",
                "agentId": "agentic_writer_studio",
                "parentRunId": None,
                "events": [],
                "messages": [
                    {"id": "bdd-user-1", "role": "user", "content": user_message},
                ],
                "createdAt": int(time.time() * 1000),
            }
        ],
    }
    path = thread_file_path(threads_dir, thread_id)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.rename(path)
    return path


def load_thread_fixture(threads_dir: Path, thread_id: str) -> dict[str, Any] | None:
    path = thread_file_path(threads_dir, thread_id)
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def thread_file_exists(threads_dir: Path, thread_id: str) -> bool:
    return thread_file_path(threads_dir, thread_id).is_file()


def _display_title(user_message: str) -> str:
    text = user_message.strip()
    if not text:
        return "Conversation"
    return f"{text[:48]}…" if len(text) > 48 else text
