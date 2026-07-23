"""
Database engine and session management.

We keep this deliberately boring: a single SQLAlchemy engine, a session
factory, and a `get_db` dependency for FastAPI routes to pull a session
from. Tests override `get_db` to point at an in-memory SQLite database
instead — see tests/conftest.py.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    # SQLite needs this to allow use across the threads FastAPI's test
    # client spins up.
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.sql_echo,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
