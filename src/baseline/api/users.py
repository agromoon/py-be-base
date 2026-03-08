"""User REST API."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from baseline.db import get_db
from baseline.schemas.user import UserCreate, UserRead, UserUpdate
from baseline.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


async def _get_user_service(
    session: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(session)


@router.get("", response_model=list[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(_get_user_service),
) -> list[UserRead]:
    """List users with optional pagination."""
    return await service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Get a user by id."""
    return await service.get_user(user_id)


@router.post("", response_model=UserRead, status_code=201)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Create a new user."""
    return await service.create_user(payload)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(_get_user_service),
) -> UserRead:
    """Update a user by id."""
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    service: UserService = Depends(_get_user_service),
) -> None:
    """Delete a user by id."""
    await service.delete_user(user_id)
