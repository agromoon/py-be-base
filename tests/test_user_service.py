"""Tests for UserService (mocked repository, no DB)."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from baseline.schemas.user import UserCreate, UserUpdate
from baseline.services.user import UserService


def _fake_user(**kw: object) -> SimpleNamespace:
    d = {"id": 1, "name": "alice", "email": "alice@x.com", "hashed_password": "hash"}
    return SimpleNamespace(**{**d, **kw})


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    with patch("baseline.services.user.UserRepository", return_value=mock_repo):
        yield UserService(db=MagicMock())


def test_create_user_success(service, mock_repo):
    mock_repo.get_user_by_name.return_value = None
    mock_repo.get_user_by_email.return_value = None
    mock_repo.create_user.return_value = _fake_user()
    payload = UserCreate(name="alice", email="alice@x.com", password="password123")

    with patch("baseline.services.user._hash_password", return_value="hashed"):
        out = service.create_user(payload)

    assert out.id == 1 and out.name == "alice" and out.email == "alice@x.com"
    assert not hasattr(out, "password")
    mock_repo.create_user.assert_called_once()
    assert mock_repo.create_user.call_args[0][2] == "hashed"


def test_create_user_duplicate_name_raises(service, mock_repo):
    mock_repo.get_user_by_name.return_value = _fake_user()
    payload = UserCreate(name="alice", email="alice@x.com", password="password123")

    with pytest.raises(ValueError, match="name already taken"):
        service.create_user(payload)
    mock_repo.create_user.assert_not_called()


def test_create_user_duplicate_email_raises(service, mock_repo):
    mock_repo.get_user_by_name.return_value = None
    mock_repo.get_user_by_email.return_value = _fake_user()
    payload = UserCreate(name="alice", email="alice@x.com", password="password123")

    with pytest.raises(ValueError, match="email already taken"):
        service.create_user(payload)
    mock_repo.create_user.assert_not_called()


def test_get_user_found(service, mock_repo):
    mock_repo.get_user.return_value = _fake_user()

    out = service.get_user(1)

    assert out and out.id == 1 and out.name == "alice"


def test_get_user_not_found(service, mock_repo):
    mock_repo.get_user.return_value = None

    assert service.get_user(999) is None


def test_get_users(service, mock_repo):
    mock_repo.get_users.return_value = [_fake_user(), _fake_user(id=2, name="bob", email="bob@x.com")]

    out = service.get_users(skip=0, limit=10)

    assert len(out) == 2 and out[0].id == 1 and out[1].name == "bob"


def test_update_user_found(service, mock_repo):
    mock_repo.update_user.return_value = _fake_user(name="alice2")

    out = service.update_user(1, UserUpdate(name="alice2"))

    assert out and out.name == "alice2"


def test_update_user_not_found(service, mock_repo):
    mock_repo.update_user.return_value = None

    assert service.update_user(999, UserUpdate(name="xxx")) is None


def test_delete_user_deleted(service, mock_repo):
    mock_repo.delete_user.return_value = _fake_user()

    assert service.delete_user(1) is True


def test_delete_user_not_found(service, mock_repo):
    mock_repo.delete_user.return_value = None

    assert service.delete_user(999) is False
