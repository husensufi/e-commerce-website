from contextlib import asynccontextmanager
from fastapi import FastAPI
from middlewares.cors import apply_cors_middleware
from routers import api_router
from auth.router import router as auth_router
from database import engine
from models.common import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup if they don't exist (fallback if Alembic not run)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI E-Commerce",
        description="E-Commerce REST API powered by FastAPI + PostgreSQL",
        version="2.0.0",
        lifespan=lifespan,
    )

    # Middlewares
    app = apply_cors_middleware(app)

    # Routers
    app.include_router(api_router)
    app.include_router(auth_router)

    return app