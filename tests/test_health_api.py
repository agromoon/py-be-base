"""Health and readiness endpoint tests."""

from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from baseline.main import app


def test_health_returns_200_and_ok() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@patch("baseline.api.health.engine")
def test_ready_returns_200_when_db_ok(mock_engine: MagicMock) -> None:
    """Readiness returns 200 when DB check succeeds; no real DB required (e.g. CI)."""
    mock_engine.__class__ = AsyncEngine  # so endpoint uses async path
    mock_conn = MagicMock()
    mock_conn.execute = AsyncMock(return_value=None)

    async def aenter(self: object) -> MagicMock:
        return mock_conn

    async def aexit(self: object, *a: object) -> None:
        return None

    mock_cm = MagicMock()
    mock_cm.__aenter__ = aenter
    mock_cm.__aexit__ = aexit
    mock_engine.connect.return_value = mock_cm

    client = TestClient(app)
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@patch("baseline.api.health.engine")
def test_ready_returns_503_when_db_unreachable(mock_engine: MagicMock) -> None:
    mock_engine.connect.return_value.__enter__.side_effect = SQLAlchemyError("connection refused")
    client = TestClient(app)
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.json()["status"] == "unavailable"
    assert "database" in r.json()["detail"].lower()
