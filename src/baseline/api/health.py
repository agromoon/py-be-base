"""Health and readiness endpoints for deployments and load balancers."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from baseline.db import engine

router = APIRouter(tags=["health"])

_UNAVAILABLE = JSONResponse(
    status_code=503,
    content={"status": "unavailable", "detail": "database unreachable"},
)


@router.get("/health")
def health() -> JSONResponse:
    """Liveness: process is running. Returns 200 with minimal JSON."""
    return JSONResponse(content={"status": "ok"})


async def _check_async(eng: AsyncEngine) -> None:
    async with eng.connect() as conn:
        await conn.execute(text("SELECT 1"))


@router.get("/ready")
async def ready() -> JSONResponse:
    """Readiness: app can serve traffic (DB reachable). Returns 200 or 503."""
    try:
        if isinstance(engine, AsyncEngine):
            await _check_async(engine)
        else:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return _UNAVAILABLE
    return JSONResponse(content={"status": "ok"})
