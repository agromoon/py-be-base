from sqlalchemy.orm import Session

from baseline.db import SessionLocal


def test_session_local_creates_session() -> None:
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()
