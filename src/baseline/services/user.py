"""User service: business logic and password hashing."""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from baseline.repositories.user import UserRepository
from baseline.schemas.user import UserCreate, UserRead, UserUpdate

_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(plain: str) -> str:
    return _password_context.hash(plain)


class UserService:
    """Application service for user operations."""

    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = UserRepository()

    def get_user(self, user_id: int) -> UserRead | None:
        """Return a user by id as UserRead, or None if not found."""
        user = self._repo.get_user(self._db, user_id)
        return UserRead.model_validate(user) if user else None

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserRead]:
        """Return a list of users with optional pagination."""
        users = self._repo.get_users(self._db, skip=skip, limit=limit)
        return [UserRead.model_validate(u) for u in users]

    def create_user(self, payload: UserCreate) -> UserRead:
        """Create a user. Raises ValueError if name or email already exists."""
        if self._repo.get_user_by_name(self._db, payload.name):
            raise ValueError("name already taken")
        if self._repo.get_user_by_email(self._db, payload.email):
            raise ValueError("email already taken")
        hashed = _hash_password(payload.password)
        user = self._repo.create_user(self._db, payload, hashed)
        return UserRead.model_validate(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserRead | None:
        """Update a user. Returns None if not found."""
        hashed: str | None = None
        if payload.password is not None:
            hashed = _hash_password(payload.password)
        user = self._repo.update_user(self._db, user_id, payload, hashed)
        return UserRead.model_validate(user) if user else None

    def delete_user(self, user_id: int) -> bool:
        """Delete a user. Returns True if deleted, False if not found."""
        user = self._repo.delete_user(self._db, user_id)
        return user is not None
