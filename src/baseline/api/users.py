"""User REST API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from baseline.db import get_db
from baseline.models.user import UserCreate, UserRead, UserUpdate
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
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Create a new user."""
    try:
        return service.create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Update a user by id."""
    user = service.update_user(user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(_get_user_service),
) -> None:
    """Delete a user by id."""
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
