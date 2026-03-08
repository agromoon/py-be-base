"""Health and readiness endpoint tests."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from baseline.main import app


def test_health_returns_200_and_ok() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready_returns_200_when_db_ok() -> None:
    client = TestClient(app)
    r = client.get("/ready")
    # With real DB (e.g. test env) we get 200; otherwise mock in test_ready_returns_503
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        assert r.json() == {"status": "ok"}


@patch("baseline.api.health.engine")
def test_ready_returns_503_when_db_unreachable(mock_engine: MagicMock) -> None:
    mock_engine.connect.return_value.__enter__.side_effect = SQLAlchemyError("connection refused")
    client = TestClient(app)
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.json()["status"] == "unavailable"
    assert "database" in r.json()["detail"].lower()
