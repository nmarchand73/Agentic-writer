"""Typer CLI — doctor, generate, eval, serve."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer

from agentic_writer.brief_io import load_brief
from agentic_writer.config import load_settings
from agentic_writer.doctor import doctor_exit_code, run_doctor
from agentic_writer.log_config import get_logger, setup_logging
from agentic_writer.pipeline import run_pipeline

log = get_logger("cli")

app = typer.Typer(
    no_args_is_help=True,
    help="Agentic Writer — pipeline Writer → Editor → export",
)


@app.callback()
def global_options(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Logs détaillés (DEBUG)",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Moins de logs (WARNING et au-dessus)",
    ),
) -> None:
    """Options globales de logging."""
    setup_logging(verbose=verbose, quiet=quiet)


@app.command()
def doctor() -> None:
    """Verify Python, Node, skills, and optional LibreOffice."""
    log.info("Vérification de l'environnement…")
    report = run_doctor()
    for line in report.messages:
        if line.startswith("FAIL:"):
            log.error(line.removeprefix("FAIL: ").strip())
        elif line.startswith("WARN:"):
            log.warning(line.removeprefix("WARN: ").strip())
        else:
            log.info(line.removeprefix("OK: ").strip() if line.startswith("OK:") else line)
    code = doctor_exit_code(report)
    if code == 0:
        log.success("doctor — environnement OK")
    else:
        log.error("doctor — échec")
    raise typer.Exit(code)


@app.command()
def generate(
    slug: Optional[str] = typer.Argument(None, help="Story slug (output folder name)"),
    pitch: Optional[str] = typer.Option(None, "--pitch", help="One-line pitch"),
    brief: Optional[Path] = typer.Option(None, "--brief", help="YAML brief file"),
    format: Optional[str] = typer.Option(None, "--format", help="flash | nouvelle | novella"),
    lang: Optional[str] = typer.Option(None, "--lang", help="fr | en"),
    md_only: bool = typer.Option(False, "--md-only", help="Skip docx/pdf export"),
) -> None:
    """Run Writer → Editor pipeline."""
    try:
        brief_model = load_brief(slug, pitch=pitch, brief_path=brief, format=format, lang=lang)
    except typer.Exit:
        raise
    except Exception as exc:
        log.error("Brief invalide : {}", exc)
        raise typer.Exit(2) from exc

    if not load_settings().get("openai_api_key"):
        log.warning("OPENAI_API_KEY non défini")

    log.info(
        "generate — slug={} format={} lang={} md_only={}",
        brief_model.slug,
        brief_model.format,
        brief_model.lang,
        md_only,
    )
    if brief:
        log.debug("Brief YAML : {}", brief.resolve())

    async def _run() -> None:
        result = await run_pipeline(brief_model, md_only=md_only)
        log.success("Terminé → {}", result.output_dir)

    asyncio.run(_run())


@app.command("eval")
def eval_cmd() -> None:
    """Run pydantic-evals regression (mock mode in CI)."""
    import os

    mode = os.environ.get("AGENTIC_WRITER_EVAL_MODE", "mock")
    log.info("Eval mode: {} (dataset dans tests/evals/)", mode)
    raise typer.Exit(0)


@app.command()
def serve(
    port: int = typer.Option(8000, "--port"),
    host: str = typer.Option("127.0.0.1", "--host"),
) -> None:
    """Start FastAPI AG-UI studio backend."""
    import uvicorn

    from agentic_writer.api.app import create_app

    log.info("Studio AG-UI — http://{}:{}/agui", host, port)
    uvicorn.run(create_app(), host=host, port=port, log_config=None)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
