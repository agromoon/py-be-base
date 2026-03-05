from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from baseline.config import config

engine = create_engine(config.db_url)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@contextmanager
def get_session() -> Generator[Session]:
    """Yield a database session bound to the configured engine."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
