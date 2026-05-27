"""FastAPI studio health (slice 5)."""

import pytest
from httpx import ASGITransport, AsyncClient

from agentic_writer.api.app import create_app
from agentic_writer.api.studio_state import StudioState


@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.asyncio
async def test_health_endpoint():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.integration
@pytest.mark.ui
def test_studio_state_model():
    state = StudioState(slug="studio-integ", pitch="Test pitch.")
    assert state.slug == "studio-integ"
    assert state.pitch == "Test pitch."


@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.asyncio
async def test_manuscript_endpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.api.app.output_dir",
        lambda slug: tmp_path / slug,
    )
    work = tmp_path / "hangar-scelle"
    work.mkdir()
    (work / "manuscript_final.md").write_text("# Titre\n\nCorps.", encoding="utf-8")

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/manuscript/hangar-scelle")
    assert resp.status_code == 200
    assert "# Titre" in resp.text


@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.asyncio
async def test_pdf_endpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "agentic_writer.api.app.output_dir",
        lambda slug: tmp_path / slug,
    )
    work = tmp_path / "hangar-scelle"
    work.mkdir()
    (work / "hangar-scelle.pdf").write_bytes(b"%PDF-1.4 test")

    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/pdf/hangar-scelle")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/pdf")
    assert b"%PDF" in resp.content
