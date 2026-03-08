from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from baseline.models.user import User
from baseline.schemas.user import UserCreate, UserUpdate


class UserRepositoryProtocol(Protocol):
    """Protocol for user persistence. Implement for testing or alternate backends."""

    async def get_user(self, session: AsyncSession, user_id: int) -> User | None: ...
    async def get_user_by_name(self, session: AsyncSession, name: str) -> User | None: ...
    async def get_user_by_email(self, session: AsyncSession, email: str) -> User | None: ...
    async def get_users(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]: ...
    async def create_user(self, session: AsyncSession, user: UserCreate, hashed_password: str) -> User: ...
    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: UserUpdate,
        hashed_password: str | None = None,
    ) -> User | None: ...
    async def delete_user(self, session: AsyncSession, user_id: int) -> User | None: ...


class UserRepository:
    """Repository for performing CRUD operations on users."""

    async def get_user(self, session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_name(self, session: AsyncSession, name: str) -> User | None:
        result = await session.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        result = await session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create_user(
        self,
        session: AsyncSession,
        user: UserCreate,
        hashed_password: str,
    ) -> User:
        """Create a new user.

        The password must be hashed by the caller before this method is invoked.
        """
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: UserUpdate,
        hashed_password: str | None = None,
    ) -> User | None:
        """Update an existing user.

        If a new password is provided, it must be hashed by the caller and passed
        in via `hashed_password`.
        """
        result = await session.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            return None

        if user.name is not None:
            db_user.name = user.name
        if user.email is not None:
            db_user.email = user.email
        if user.password is not None and hashed_password is not None:
            db_user.hashed_password = hashed_password

        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def delete_user(self, session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        db_user = result.scalar_one_or_none()
        if db_user:
            await session.delete(db_user)
            await session.commit()
        return db_user
