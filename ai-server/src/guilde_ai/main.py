from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from guilde_ai.api.routes import router
from guilde_ai.config import Settings, get_settings
from guilde_ai.llm.client import MockLlm, OpenAICompatibleLlm
from guilde_ai.rag.store import InMemoryRag


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.rag = InMemoryRag.from_seed(settings.company_seed)
        if settings.llm_mode == "openai":
            app.state.llm = OpenAICompatibleLlm(
                base_url=settings.llm_base_url,
                model=settings.llm_model,
                api_key=settings.llm_api_key,
            )
        else:
            app.state.llm = MockLlm()
        yield

    app = FastAPI(title="GUILDE AI Server", version="0.1.0", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
