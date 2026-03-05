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


def get_db() -> Generator[Session]:
    """Yield a database session. Use with FastAPI Depends or as context manager."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_session = contextmanager(get_db)
