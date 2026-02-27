from sqlalchemy.orm import Session

from baseline.models.user import User, UserCreate, UserUpdate


class UserRepository:
    """Repository for performing CRUD operations on users."""

    def get_user(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_name(self, db: Session, name: str) -> User | None:
        return db.query(User).filter(User.name == name).first()

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate, hashed_password: str) -> User:
        """Create a new user.

        The password must be hashed by the caller before this method is invoked.
        """
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(
        self,
        db: Session,
        user_id: int,
        user: UserUpdate,
        hashed_password: str | None = None,
    ) -> User | None:
        """Update an existing user.

        If a new password is provided, it must be hashed by the caller and passed
        in via `hashed_password`.
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        if user.name is not None:
            db_user.name = user.name
        if user.email is not None:
            db_user.email = user.email
        if user.password is not None and hashed_password is not None:
            db_user.hashed_password = hashed_password

        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> User | None:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
