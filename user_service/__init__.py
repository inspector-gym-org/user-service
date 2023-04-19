from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .config import settings
from .routes import router
from .database import create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_indexes()
    yield


def build_app() -> FastAPI:
    app = FastAPI(root_path=settings.app_root_path, lifespan=lifespan)
    app.include_router(router)

    return app
