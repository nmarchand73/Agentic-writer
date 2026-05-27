"""Studio agent — generative UI with pipeline steps (AG-UI state)."""

from __future__ import annotations

from textwrap import dedent

from ag_ui.core import EventType, StateDeltaEvent, StateSnapshotEvent
from pydantic_ai import Agent, RunContext, ToolReturn
from pydantic_ai.ui import StateDeps

from agentic_writer.api.studio_progress import get_studio_progress_bridge
from agentic_writer.api.studio_state import (
    StudioState,
    ensure_pipeline_steps,
    mark_all_pipeline_steps_completed,
    patch_step_status,
    patch_usage_fields,
    reset_pipeline_step_statuses,
)
from agentic_writer.usage_cost import UsageLedger
from agentic_writer.config import load_settings
from agentic_writer.models import Brief
from agentic_writer.log_config import get_logger
from agentic_writer.pipeline import run_pipeline

studio_log = get_logger("studio")

STUDIO_INSTRUCTIONS = dedent("""
    Tu es l'orchestrateur du studio Agentic Writer (Architecte → chapitres → Editor → Auditeur → export).

    Quand l'utilisateur demande de générer une nouvelle :
    1. Extrais slug et pitch du message (ou demande-les brièvement).
    2. Appelle TOUJOURS `create_pipeline_plan` puis `run_story_generation` (mêmes slug, pitch, md_only).
    3. Ne modifie pas les étapes toi-même — `run_story_generation` met à jour l'UI en direct.
    4. Ne répète pas la liste des étapes dans ta réponse — résume en une phrase avec emoji.

    Format par défaut : nouvelle, langue fr. Export docx/pdf sauf si l'utilisateur demande markdown seul (md_only=true).
""")


def create_studio_agent() -> Agent[StateDeps[StudioState], str]:
    settings = load_settings()

    agent: Agent[StateDeps[StudioState], str] = Agent(
        settings["openai_model"],
        instructions=STUDIO_INSTRUCTIONS,
        deps_type=StateDeps[StudioState],
    )

    def _emit_snapshot(state: StudioState) -> None:
        bridge = get_studio_progress_bridge()
        event = StateSnapshotEvent(
            type=EventType.STATE_SNAPSHOT,
            snapshot=state.model_dump(),
        )
        if bridge is not None:
            bridge.emit_nowait(event)

    @agent.tool
    async def create_pipeline_plan(
        ctx: RunContext[StateDeps[StudioState]],
        slug: str,
        pitch: str,
        format: str = "nouvelle",
        lang: str = "fr",
        md_only: bool = False,
    ) -> ToolReturn:
        """Crée le plan d'étapes affiché dans l'UI (snapshot AG-UI)."""
        state = StudioState(
            slug=slug,
            pitch=pitch,
            format=format,  # type: ignore[arg-type]
            lang=lang,  # type: ignore[arg-type]
            md_only=md_only,
            steps=[],
            manuscript_md=None,
            manuscript_preview=None,
            output_dir=None,
            error=None,
        )
        ensure_pipeline_steps(state, include_export=not md_only)
        ctx.deps.state = state
        _emit_snapshot(state)
        return ToolReturn(
            return_value="Plan pipeline récit créé.",
            metadata=StateSnapshotEvent(
                type=EventType.STATE_SNAPSHOT,
                snapshot=state.model_dump(),
            ),
        )

    @agent.tool
    async def run_story_generation(
        ctx: RunContext[StateDeps[StudioState]],
        slug: str | None = None,
        pitch: str | None = None,
        format: str | None = None,
        lang: str | None = None,
        md_only: bool | None = None,
    ) -> ToolReturn:
        """Exécute le pipeline récit et met à jour les étapes en direct."""
        state = ctx.deps.state
        state.slug = slug or state.slug
        state.pitch = pitch or state.pitch
        if format:
            state.format = format  # type: ignore[assignment]
        if lang:
            state.lang = lang  # type: ignore[assignment]
        if md_only is not None:
            state.md_only = md_only
        if not state.slug or not state.pitch:
            state.error = "slug et pitch requis"
            return ToolReturn(return_value=state.error)

        include_export = not state.md_only
        ensure_pipeline_steps(state, include_export=include_export)
        reset_pipeline_step_statuses(state)

        state.manuscript_md = None
        state.manuscript_preview = None
        state.output_dir = None
        state.usage_input_tokens = 0
        state.usage_output_tokens = 0
        state.usage_requests = 0
        state.estimated_cost_usd = None

        # Snapshot obligatoire avant tout STATE_DELTA (sinon le client a state={})
        _emit_snapshot(state)

        bridge = get_studio_progress_bridge()

        def push_step(index: int, status: str) -> None:
            if index < len(state.steps):
                state.steps[index].status = status  # type: ignore[assignment]
            delta = StateDeltaEvent(
                type=EventType.STATE_DELTA,
                delta=[patch_step_status(index, status)],  # type: ignore[arg-type]
            )
            snapshot = StateSnapshotEvent(
                type=EventType.STATE_SNAPSHOT,
                snapshot=state.model_dump(),
            )
            if bridge is not None:
                bridge.emit_nowait(delta)
                bridge.emit_nowait(snapshot)

        studio_log.info(
            "Génération studio slug={} md_only={}",
            state.slug,
            state.md_only,
        )

        async def on_start(index: int, _label: str) -> None:
            push_step(index, "running")

        async def on_complete(index: int, _label: str) -> None:
            push_step(index, "completed")

        async def on_usage(ledger: UsageLedger) -> None:
            fields = ledger.as_state_fields()
            state.usage_input_tokens = int(fields["usage_input_tokens"])
            state.usage_output_tokens = int(fields["usage_output_tokens"])
            state.usage_requests = int(fields["usage_requests"])
            state.estimated_cost_usd = fields["estimated_cost_usd"]
            delta = StateDeltaEvent(
                type=EventType.STATE_DELTA,
                delta=patch_usage_fields(
                    usage_input_tokens=state.usage_input_tokens,
                    usage_output_tokens=state.usage_output_tokens,
                    usage_requests=state.usage_requests,
                    estimated_cost_usd=state.estimated_cost_usd,
                ),
            )
            snapshot = StateSnapshotEvent(
                type=EventType.STATE_SNAPSHOT,
                snapshot=state.model_dump(),
            )
            if bridge is not None:
                bridge.emit_nowait(delta)
                bridge.emit_nowait(snapshot)

        brief = Brief(
            slug=state.slug,
            pitch=state.pitch,
            format=state.format,
            lang=state.lang,
        )

        try:
            result = await run_pipeline(
                brief,
                md_only=state.md_only,
                on_step_start=on_start,
                on_step_complete=on_complete,
                on_usage=on_usage,
            )
            state.output_dir = result.output_dir
            state.manuscript_md = result.edited.manuscript_corrected
            state.manuscript_preview = result.edited.manuscript_corrected[:500]
            state.error = None
            mark_all_pipeline_steps_completed(state)
            msg = f"Nouvelle générée → {result.output_dir}"
            _emit_snapshot(state)
        except Exception as exc:
            state.error = str(exc)
            msg = f"Échec : {exc}"
            _emit_snapshot(state)

        return ToolReturn(
            return_value=msg,
            metadata=StateSnapshotEvent(
                type=EventType.STATE_SNAPSHOT,
                snapshot=state.model_dump(),
            ),
        )

    return agent
