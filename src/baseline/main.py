from __future__ import annotations

import logging
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uvicorn import run as uvicorn_run

from baseline.api import users_router
from baseline.config import config
from baseline.exceptions import AppError

logger = logging.getLogger(__name__)


def get_alembic_config() -> Config:
    """Return the Alembic configuration for this project."""
    project_root = Path(__file__).resolve().parents[2]
    alembic_ini = project_root / "alembic.ini"
    return Config(str(alembic_ini))


def run_migrations() -> None:
    """Run all pending database migrations up to head."""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


app = FastAPI(title=config.app_name)
app.include_router(users_router)


@app.exception_handler(AppError)
def app_error_handler(_request: object, exc: AppError) -> JSONResponse:
    """Log internal message; return generic detail and stable status code to client."""
    logger.warning("%s: %s", type(exc).__name__, exc.args[0] if exc.args else exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def main() -> None:
    """Entry point for command-line usage."""
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        run_migrations()
    else:
        uvicorn_run(
            "baseline.main:app",
            host="0.0.0.0",
            port=8000,
            reload=config.debug,
        )
