"""API tests: status codes and response contract (mock UserService, no DB)."""

from unittest.mock import AsyncMock

import httpx
import pytest

from baseline.api.users import _get_user_service
from baseline.exceptions import ConflictError, NotFoundError
from baseline.main import app
from baseline.schemas.user import UserRead


def _fake_read(**kw: object) -> UserRead:
    d = {"id": 1, "name": "alice", "email": "alice@x.com"}
    return UserRead(**{**d, **kw})


@pytest.fixture
def mock_service():
    return AsyncMock()


@pytest.fixture
async def client(mock_service):
    async def override():
        return mock_service

    app.dependency_overrides[_get_user_service] = override
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


async def test_list_users_200(client, mock_service):
    mock_service.get_users.return_value = [_fake_read()]
    r = await client.get("/users")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 1 and data[0]["name"] == "alice"


async def test_get_user_200(client, mock_service):
    mock_service.get_user.return_value = _fake_read()
    r = await client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1 and "password" not in r.json()


async def test_get_user_404(client, mock_service):
    mock_service.get_user.side_effect = NotFoundError("User not found")
    r = await client.get("/users/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Resource not found"


async def test_create_user_201(client, mock_service):
    mock_service.create_user.return_value = _fake_read()
    r = await client.post(
        "/users",
        json={"name": "alice", "email": "a@b.com", "password": "password123"},
    )
    assert r.status_code == 201
    assert r.json()["email"] == "alice@x.com" and "password" not in r.json()


async def test_create_user_409_conflict(client, mock_service):
    mock_service.create_user.side_effect = ConflictError("email already taken")
    r = await client.post(
        "/users",
        json={"name": "alice", "email": "a@b.com", "password": "password123"},
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Conflict with existing resource"


async def test_update_user_200(client, mock_service):
    mock_service.update_user.return_value = _fake_read(name="alice2")
    r = await client.patch("/users/1", json={"name": "alice2"})
    assert r.status_code == 200
    assert r.json()["name"] == "alice2"


async def test_update_user_404(client, mock_service):
    mock_service.update_user.side_effect = NotFoundError("User not found")
    r = await client.patch("/users/999", json={"name": "xxx"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Resource not found"


async def test_delete_user_204(client, mock_service):
    mock_service.delete_user.return_value = True
    r = await client.delete("/users/1")
    assert r.status_code == 204


async def test_delete_user_404(client, mock_service):
    mock_service.delete_user.side_effect = NotFoundError("User not found")
    r = await client.delete("/users/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Resource not found"
