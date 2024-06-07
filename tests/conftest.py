from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.initiator import init_app

from app.common.database import Base, get_db
from app.users.models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="package", autouse=True)
def app():
    """Setup FastAPI application for testing."""
    app = init_app(start_db=False)
    return app


@pytest.fixture(scope="package")
def setup_database():
    """Setup database for testing."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="package")
def client(app, setup_database):
    """Test client for the application."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def session(app: FastAPI, setup_database):
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


@pytest.fixture(scope="function")
def insert_users(session: Session):
    users = [
        User(
            id=1,
            username="Machine-1",
            email="Machine1@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=2,
            username="Machine-2",
            email="Machine2@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=3,
            username="Machine-3",
            email="Machine3@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
        User(
            id=4,
            username="Machine-4",
            email="Machine4@example.com",
            full_name="Machine Tester",
            status="active",
            role="user",
        ),
    ]
    session.add_all(users)
    session.commit()
    return users
