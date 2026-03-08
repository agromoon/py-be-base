"""Health and readiness endpoints for deployments and load balancers."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from baseline.db import engine

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> JSONResponse:
    """Liveness: process is running. Returns 200 with minimal JSON."""
    return JSONResponse(content={"status": "ok"})


@router.get("/ready")
def ready() -> JSONResponse:
    """Readiness: app can serve traffic (DB reachable). Returns 200 or 503."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "detail": "database unreachable"},
        )
    return JSONResponse(content={"status": "ok"})
