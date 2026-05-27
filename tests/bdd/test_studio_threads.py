"""BDD slice 7 — persistance des threads Studio (niveau 2)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from tests.support.studio_threads import (
    load_thread_fixture,
    save_thread_fixture,
    thread_file_exists,
)

scenarios("../../specs/bdd/07_studio_threads.feature")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_ROOT = PROJECT_ROOT / "web"


@pytest.fixture
def context():
    return {}


@pytest.fixture
def threads_dir(tmp_path) -> Path:
    return tmp_path / "studio-threads"


def _run_runner_bdd(
    threads_dir: Path,
    *,
    script: str,
    thread_id: str,
    message: str = "",
) -> None:
    env = {
        **os.environ,
        "AGENTIC_WRITER_THREADS_DIR": str(threads_dir.resolve()),
        "BDD_SCRIPT": script,
        "BDD_THREAD_ID": thread_id,
        "BDD_MESSAGE": message,
    }
    result = subprocess.run(
        ["npx", "--yes", "tsx", "tests/thread-runner-bdd.ts"],
        cwd=WEB_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            "Échec runner studio BDD:\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


@given("un dossier studio threads vide")
def empty_threads_dir(context, threads_dir):
    context["threads_dir"] = threads_dir
    threads_dir.mkdir(parents=True, exist_ok=True)


@given(parsers.parse('un thread "{thread_id}" sauvegardé sur disque'))
def thread_saved_minimal(context, threads_dir, thread_id):
    context["threads_dir"] = threads_dir
    context["last_thread_id"] = thread_id
    save_thread_fixture(threads_dir, thread_id, "Message BDD minimal")


@given(
    parsers.parse(
        'un thread "{thread_id}" sauvegardé sur disque avec le message "{message}"'
    )
)
def thread_saved_with_message(context, threads_dir, thread_id, message):
    context["threads_dir"] = threads_dir
    context["last_thread_id"] = thread_id
    save_thread_fixture(threads_dir, thread_id, message)


@when(
    parsers.parse(
        'je sauvegarde un thread "{thread_id}" avec le message utilisateur "{message}"'
    )
)
def save_thread_step(context, threads_dir, thread_id, message):
    context["threads_dir"] = threads_dir
    context["last_thread_id"] = thread_id
    save_thread_fixture(threads_dir, thread_id, message)


@when("je crée un runner studio frais sur ce dossier")
def fresh_runner(context, threads_dir):
    context["threads_dir"] = threads_dir


@then(parsers.parse("le runner liste {count:d} threads"))
def runner_lists_count(threads_dir, count):
    env = {
        **os.environ,
        "AGENTIC_WRITER_THREADS_DIR": str(threads_dir.resolve()),
        "BDD_SCRIPT": "count",
        "BDD_THREAD_COUNT": str(count),
    }
    result = subprocess.run(
        ["npx", "--yes", "tsx", "tests/thread-runner-bdd.ts"],
        cwd=WEB_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"Échec count threads:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


@when(parsers.parse('je supprime le thread "{thread_id}" via le runner studio'))
def delete_thread_runner(context, threads_dir, thread_id):
    context["threads_dir"] = threads_dir
    _run_runner_bdd(threads_dir, script="delete", thread_id=thread_id)


@then(parsers.parse('le fichier thread "{thread_id}" existe sur disque'))
def thread_file_exists_step(threads_dir, thread_id):
    assert thread_file_exists(threads_dir, thread_id)


@then(parsers.parse('le fichier thread "{thread_id}" n\'existe pas sur disque'))
def thread_file_missing_step(threads_dir, thread_id):
    assert not thread_file_exists(threads_dir, thread_id)


@then(parsers.parse('le thread sur disque a pour titre "{title}"'))
def thread_title_on_disk(context, threads_dir, title):
    thread_id = context.get("last_thread_id", "bdd-save-1")
    data = load_thread_fixture(threads_dir, thread_id)
    assert data is not None
    assert data.get("name") == title


@then(parsers.parse('le runner liste le thread "{thread_id}"'))
def runner_lists_thread(threads_dir, thread_id):
    _run_runner_bdd(threads_dir, script="list-and-messages", thread_id=thread_id)


@then(
    parsers.parse('le runner expose le message "{message}" pour ce thread')
)
def runner_has_message(context, threads_dir, message):
    thread_id = context["last_thread_id"]
    _run_runner_bdd(
        threads_dir,
        script="list-and-messages",
        thread_id=thread_id,
        message=message,
    )
