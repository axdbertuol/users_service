import asyncio
from contextlib import asynccontextmanager
import os

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.initiator import init_app
from app.producer import get_aioproducer, loop
from app.users.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

mock_user_password = {
    "plain": "P@ssw0rd",
    "hashed": "$2b$12$9GpKYahAVQZXPrKb1c2jxerzhkKudmZBfkFqGcx/dSBjHS1l7xAGW",
}


@pytest_asyncio.fixture(scope="package", autouse=True)
async def app():
    """Setup FastAPI application for testing."""

    @asynccontextmanager
    async def lifespan(app):
        print("Starting up")
        yield
        print("Shutting down")

    app = init_app(start_db=False, lifespan=lifespan)

    return app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def set_env_variables(monkeypatch):
    monkeypatch.setenv(
        "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080")


class MockAIOKafkaProducer:
    async def start(self):
        pass

    async def stop(self):
        pass

    async def send_and_wait(self, topic, value):
        pass

    async def send(self, topic, value, key):
        pass


mock_aioproducer = MockAIOKafkaProducer()


@pytest_asyncio.fixture(scope="function")
async def override_kafka_dependencies(app: FastAPI):
    """Override dependencies for testing."""

    def override_get_aioproducer():
        yield mock_aioproducer

    app.dependency_overrides[get_aioproducer] = override_get_aioproducer
    yield
    app.dependency_overrides.pop(get_aioproducer, None)


@pytest_asyncio.fixture(scope="package")
async def setup_database():
    """Setup database for testing."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture(scope="function")
async def session(app, setup_database):
    """Database session for testing."""
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# @pytest_asyncio.fixture(scope="session")
# async def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client(app, setup_database):
    """Async test client for the application."""
    async with LifespanManager(app) as manager:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=manager.app), base_url="http://test"
        ) as ac:
            yield ac


@pytest_asyncio.fixture(scope="function")
async def insert_users(session: Session):
    users = [
        User(
            id="1",
            username="Machine1",
            hashed_password=mock_user_password["hashed"],
            email="Machine1@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id="2",
            username="Machine2",
            email="Machine2@example.com",
            hashed_password=mock_user_password["hashed"],
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id="3",
            username="Machine3",
            email="Machine3@example.com",
            hashed_password=mock_user_password["hashed"],
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id="4",
            username="Machine4",
            email="Machine4@example.com",
            hashed_password=mock_user_password["hashed"],
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
    ]
    session.add_all(users)
    session.commit()
    return users


@pytest_asyncio.fixture(scope="function")
async def login_tokens(insert_users, async_client):
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "Machine1", "password": mock_user_password["plain"]},
    )
    tokens = login_response.json()
    return tokens
