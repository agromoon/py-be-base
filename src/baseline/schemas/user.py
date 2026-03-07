"""User API schemas (request/response DTOs)."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

NameStr = Annotated[str, StringConstraints(min_length=3, max_length=64)]
PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserBase(BaseModel):
    """Shared user fields."""

    name: NameStr
    email: EmailStr


class UserCreate(UserBase):
    """Create user payload; password is hashed before storage."""

    password: PasswordStr


class UserUpdate(BaseModel):
    """Partial update payload; all fields optional."""

    name: NameStr | None = None
    email: EmailStr | None = None
    password: PasswordStr | None = None


class UserRead(UserBase):
    """User response (from DB)."""

    id: int
    model_config = ConfigDict(from_attributes=True)
