"""FastAPI application with AG-UI endpoint."""

from __future__ import annotations

from dataclasses import replace
from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response

from agentic_writer.api.studio import create_studio_agent
from agentic_writer.config import output_dir
from agentic_writer.export_names import resolve_export_pdf_path
from agentic_writer.models import StoryFormat
from agentic_writer.api.studio_progress import (
    StudioProgressBridge,
    reset_studio_progress_bridge,
    set_studio_progress_bridge,
)
from agentic_writer.api.studio_state import StudioState
from pydantic_ai.ui import StateDeps

try:
    from pydantic_ai.ui.ag_ui import AGUIAdapter
except ImportError:
    AGUIAdapter = None  # type: ignore[misc, assignment]

_studio_agent = None
_default_deps = StateDeps(StudioState())


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic Writer Studio")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/manuscript/{slug}", response_class=PlainTextResponse)
    async def get_manuscript(slug: str) -> PlainTextResponse:
        """Manuscrit final pour l'UI Studio (évite de passer tout le MD dans l'état AG-UI)."""
        path = output_dir(slug) / "manuscript_final.md"
        if not path.is_file():
            raise HTTPException(status_code=404, detail="manuscript_final.md introuvable")
        return PlainTextResponse(
            path.read_text(encoding="utf-8"),
            media_type="text/markdown; charset=utf-8",
        )

    def _pdf_path_or_404(slug: str, format: StoryFormat | None) -> Path:
        work = output_dir(slug)
        path = resolve_export_pdf_path(work, slug, format)
        if path is None:
            raise HTTPException(status_code=404, detail="pdf introuvable")
        return path

    @app.get("/pdf/{slug}")
    async def get_pdf(
        slug: str,
        format: StoryFormat | None = Query(
            None,
            description="Format récit (flash, nouvelle, novella) pour {slug}-{format}.pdf",
        ),
    ) -> FileResponse:
        """PDF imprimable pour prévisualisation inline dans le Studio."""
        path = _pdf_path_or_404(slug, format)
        filename = path.name
        return FileResponse(
            path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )

    @app.head("/pdf/{slug}", response_model=None)
    async def head_pdf(
        slug: str,
        format: StoryFormat | None = Query(
            None,
            description="Format récit (flash, nouvelle, novella) pour {slug}-{format}.pdf",
        ),
    ) -> Response:
        """Existence check for Studio UI (GET also works; HEAD avoids full download)."""
        path = _pdf_path_or_404(slug, format)
        filename = path.name
        return Response(
            status_code=200,
            headers={
                "Content-Type": "application/pdf",
                "Content-Length": str(path.stat().st_size),
                "Content-Disposition": f'inline; filename="{filename}"',
            },
        )

    @app.post("/agui")
    async def agui_endpoint(request: Request) -> Response:
        if AGUIAdapter is None:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                {"error": "Install pydantic-ai-slim[ag-ui] for studio"},
                status_code=501,
            )
        global _studio_agent
        if _studio_agent is None:
            _studio_agent = create_studio_agent()

        deps = replace(_default_deps)
        try:
            adapter = await AGUIAdapter.from_request(
                request,
                agent=_studio_agent,
            )
        except ValidationError as exc:
            return Response(
                content=exc.json(),
                media_type="application/json",
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        bridge = StudioProgressBridge()
        token = set_studio_progress_bridge(bridge)

        async def merged_stream():
            try:
                async for event in bridge.interleave(adapter.run_stream(deps=deps)):
                    yield event
            finally:
                reset_studio_progress_bridge(token)
                await bridge.close()

        return adapter.streaming_response(merged_stream())

    return app
