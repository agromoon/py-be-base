"""API tests: status codes and response contract (mock UserService, no DB)."""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from baseline.api.users import _get_user_service
from baseline.main import app
from baseline.schemas.user import UserRead


def _fake_read(**kw: object) -> UserRead:
    d = {"id": 1, "name": "alice", "email": "alice@x.com"}
    return UserRead(**{**d, **kw})


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def client(mock_service):
    app.dependency_overrides[_get_user_service] = lambda: mock_service
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_list_users_200(client, mock_service):
    mock_service.get_users.return_value = [_fake_read()]
    r = client.get("/users")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 1 and data[0]["name"] == "alice"


def test_get_user_200(client, mock_service):
    mock_service.get_user.return_value = _fake_read()
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1 and "password" not in r.json()


def test_get_user_404(client, mock_service):
    mock_service.get_user.return_value = None
    r = client.get("/users/999")
    assert r.status_code == 404


def test_create_user_201(client, mock_service):
    mock_service.create_user.return_value = _fake_read()
    r = client.post("/users", json={"name": "alice", "email": "a@b.com", "password": "password123"})
    assert r.status_code == 201
    assert r.json()["email"] == "alice@x.com" and "password" not in r.json()


def test_create_user_400_duplicate(client, mock_service):
    mock_service.create_user.side_effect = ValueError("email already taken")
    r = client.post("/users", json={"name": "alice", "email": "a@b.com", "password": "password123"})
    assert r.status_code == 400
    assert "email already taken" in r.json().get("detail", "")


def test_update_user_200(client, mock_service):
    mock_service.update_user.return_value = _fake_read(name="alice2")
    r = client.patch("/users/1", json={"name": "alice2"})
    assert r.status_code == 200
    assert r.json()["name"] == "alice2"


def test_update_user_404(client, mock_service):
    mock_service.update_user.return_value = None
    r = client.patch("/users/999", json={"name": "xxx"})
    assert r.status_code == 404


def test_delete_user_204(client, mock_service):
    mock_service.delete_user.return_value = True
    r = client.delete("/users/1")
    assert r.status_code == 204


def test_delete_user_404(client, mock_service):
    mock_service.delete_user.return_value = False
    r = client.delete("/users/999")
    assert r.status_code == 404
