from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def db_session():
    # A fresh in-memory SQLite database per test, so tests can't leak
    # state into each other regardless of execution order.
    # StaticPool keeps a single connection alive for the lifetime of the
    # engine, which is required for an in-memory SQLite database: without
    # it, each new connection (e.g. from a different thread, which is
    # exactly what TestClient uses) would see its own empty database.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def register_and_login(client: TestClient, username: str, role: str | None = None) -> dict:
    """Registers a user and returns an Authorization header dict.

    If `role` is given, promotes the user directly in the DB afterward
    (there's no public "make me an oracle" endpoint, on purpose).
    """
    client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@example.com", "password": "correcthorse123"},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": username, "password": "correcthorse123"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def future_date(days: int = 30) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
