from contextlib import asynccontextmanager

import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.initiator import init_app
from app.producer import get_aioproducer
from app.users.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


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
def override_dependencies(app: FastAPI):
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
            id=1,
            username="Machine1",
            email="Machine1@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=2,
            username="Machine2",
            email="Machine2@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=3,
            username="Machine3",
            email="Machine3@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=4,
            username="Machine4",
            email="Machine4@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
    ]
    session.add_all(users)
    session.commit()
    return users
