import httpx
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.users.models import User

from .conftest import mock_user_password


@pytest.mark.asyncio
async def test_update_user(
    async_client: httpx.AsyncClient,
    insert_users,
    login_tokens,
    override_kafka_dependencies,
):
    user_update_request = {
        "full_name": "xis",
    }
    response = await async_client.put(
        "/api/v1/users/1",
        json=user_update_request,
        headers={"Authorization": "Bearer " + login_tokens["access_token"]},
    )
    assert response.status_code == 200
    response = await async_client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == user_update_request["full_name"]


@pytest.mark.asyncio
async def test_delete_user(
    async_client, override_kafka_dependencies, login_tokens, insert_users
):

    response = await async_client.delete(
        "/api/v1/users/2",
        headers={"Authorization": "Bearer " + login_tokens["access_token"]},
    )
    assert response.status_code == 200
    response = await async_client.get("/api/v1/users/2")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_user(async_client, override_kafka_dependencies, insert_users):

    response = await async_client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_read_users(async_client, override_kafka_dependencies, insert_users):

    response = await async_client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_signup(async_client: AsyncClient, session: Session):
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "full_name": "test user",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["username"] == "testuser"


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, insert_users: list[User]):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "Machine1", "password": mock_user_password["plain"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_tokens(async_client: AsyncClient, insert_users: list[User]):
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "Machine1", "password": mock_user_password["plain"]},
    )
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    refresh_response = await async_client.post(
        "/api/v1/auth/refresh_tokens",
        json={"refresh_token": refresh_token},
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert "refresh_token" in data
