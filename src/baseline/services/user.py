"""User service: business logic and password hashing."""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from baseline.exceptions import ConflictError, NotFoundError
from baseline.repositories.user import UserRepository, UserRepositoryProtocol
from baseline.schemas.user import UserCreate, UserRead, UserUpdate

_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(plain: str) -> str:
    return _password_context.hash(plain)


class UserService:
    """Application service for user operations."""

    def __init__(
        self,
        db: Session,
        repo: UserRepositoryProtocol | None = None,
    ) -> None:
        self._db = db
        self._repo = repo if repo is not None else UserRepository()

    def get_user(self, user_id: int) -> UserRead:
        """Return a user by id. Raises NotFoundError if not found."""
        user = self._repo.get_user(self._db, user_id)
        if user is None:
            raise NotFoundError("User not found")
        return UserRead.model_validate(user)

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserRead]:
        """Return a list of users with optional pagination."""
        users = self._repo.get_users(self._db, skip=skip, limit=limit)
        return [UserRead.model_validate(u) for u in users]

    def create_user(self, payload: UserCreate) -> UserRead:
        """Create a user. Raises ConflictError if name or email already exists."""
        if self._repo.get_user_by_name(self._db, payload.name):
            raise ConflictError("name already taken")
        if self._repo.get_user_by_email(self._db, payload.email):
            raise ConflictError("email already taken")
        hashed = _hash_password(payload.password)
        user = self._repo.create_user(self._db, payload, hashed)
        return UserRead.model_validate(user)

    def update_user(self, user_id: int, payload: UserUpdate) -> UserRead:
        """Update a user. Raises NotFoundError if not found."""
        hashed: str | None = None
        if payload.password is not None:
            hashed = _hash_password(payload.password)
        user = self._repo.update_user(self._db, user_id, payload, hashed)
        if user is None:
            raise NotFoundError("User not found")
        return UserRead.model_validate(user)

    def delete_user(self, user_id: int) -> None:
        """Delete a user. Raises NotFoundError if not found."""
        user = self._repo.delete_user(self._db, user_id)
        if user is None:
            raise NotFoundError("User not found")
