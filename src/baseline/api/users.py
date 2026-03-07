"""User REST API."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from baseline.db import get_db
from baseline.schemas.user import UserCreate, UserRead, UserUpdate
from baseline.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("", response_model=list[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(_get_user_service),
) -> list[UserRead]:
    """List users with optional pagination."""
    return service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Get a user by id."""
    return service.get_user(user_id)


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Create a new user."""
    return service.create_user(payload)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Update a user by id."""
    return service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(_get_user_service),
) -> None:
    """Delete a user by id."""
    service.delete_user(user_id)
