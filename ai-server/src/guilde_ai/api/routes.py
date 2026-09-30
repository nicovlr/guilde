from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from guilde_ai.llm.client import build_system_prompt

router = APIRouter()


class TalkRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class TalkResponse(BaseModel):
    npc_id: str
    npc_name: str
    reply: str
    mode: str
    sources: list[str]


@router.get("/health")
async def health(request: Request) -> dict[str, str]:
    settings = request.app.state.settings
    return {"status": "ok", "mode": settings.llm_mode}


@router.post("/npc/{npc_id}/talk", response_model=TalkResponse)
async def talk(npc_id: str, body: TalkRequest, request: Request) -> TalkResponse:
    rag = request.app.state.rag
    llm = request.app.state.llm
    settings = request.app.state.settings

    npc = next((n for n in rag.company.npcs if n.id == npc_id), None)
    if npc is None:
        raise HTTPException(status_code=404, detail=f"Unknown NPC: {npc_id}")

    chunks = rag.retrieve(body.message, npc_id=npc_id, k=5)
    system = build_system_prompt(npc.name, npc.role, chunks)
    reply = await llm.complete(system=system, user=body.message)
    return TalkResponse(
        npc_id=npc.id,
        npc_name=npc.name,
        reply=reply,
        mode=settings.llm_mode,
        sources=[c.source for c in chunks],
    )
