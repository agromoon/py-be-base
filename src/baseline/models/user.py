from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class User(Base):
    """User model for the database

    Attributes:
        id: The user's ID
        name: The user's unique name/handle
        email: The user's email
        hashed_password: The user's hashed password
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


NameStr = Annotated[str, StringConstraints(min_length=3, max_length=64)]
PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserBase(BaseModel):
    """User base model for the database

    Attributes:
        name: The user's name/handle
        email: The user's email
    """

    name: NameStr
    email: EmailStr


class UserCreate(UserBase):
    """User create model for the database

    Attributes:
        name: The user's name
        email: The user's email
        password: The user's password (plain text; will be hashed before storage)
    """

    password: PasswordStr


class UserUpdate(BaseModel):
    """User update model for the database.

    All fields are optional so that partial updates are possible.

    Attributes:
        name: The user's new name/handle, if changing.
        email: The user's new email, if changing.
        password: The user's new password, if changing.
    """

    name: NameStr | None = None
    email: EmailStr | None = None
    password: PasswordStr | None = None


class UserRead(UserBase):
    """User read model for the database

    Attributes:
        id: The user's ID
        name: The user's name
        email: The user's email
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
