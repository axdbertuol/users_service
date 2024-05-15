import os
from typing import Annotated, Any

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.common.database import Base, get_db
from app.common.dependencies import make_user_router_deps
from app.main import app
from app.users.models import User
from app.users.user_repository import UserRepository
from app.users.user_service import UserService

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def override_dependency(q: Union[str, None] = None):
#     return {"q": q, "skip": 5, "limit": 10}


def override_make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
):
    user_repo = UserRepository(session=db, model_type=User)
    user_service = UserService(user_repo=user_repo)

    return user_service


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[make_user_router_deps] = override_make_user_router_deps


# @pytest.fixture(scope="session", autouse=True)
# def setup_before_all_tests():
#     # Example of running an external setup script
#     subprocess.run(["python", "app/tests/test_setup.py"], check=True)
#     print("Setup script executed before all tests")

#     yield

#     # Optionally add teardown code here
#     print("Running teardown after all tests")


os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db():
    # Initialize the test database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
