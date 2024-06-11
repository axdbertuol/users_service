import httpx
import pytest


@pytest.mark.asyncio
async def test_create_user(
    async_client: httpx.AsyncClient, session, override_dependencies
):
    user_create_request = {
        "email": "tes2t@example.com",
        "username": "teste",
        "password": "pass2word",
        "full_name": "sgsd df",
    }
    response = await async_client.post("/api/v1/users", json=user_create_request)
    assert response.status_code == 201
    json_resp = response.json()
    assert json_resp["success"] is True
    assert "data" in json_resp
    assert "id" in json_resp["data"]
    assert user_create_request["email"] == json_resp["data"]["email"]


@pytest.mark.asyncio
async def test_update_user(
    async_client: httpx.AsyncClient, session, override_dependencies, insert_users
):
    user_update_request = {
        "full_name": "xis",
    }
    response = await async_client.put("/api/v1/users/1", json=user_update_request)
    assert response.status_code == 200
    response = await async_client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == user_update_request["full_name"]


@pytest.mark.asyncio
async def test_delete_user(async_client, session, override_dependencies, insert_users):

    response = await async_client.delete("/api/v1/users/2")
    assert response.status_code == 200
    response = await async_client.get("/api/v1/users/2")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_user(async_client, session, override_dependencies, insert_users):

    response = await async_client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_read_users(async_client, session, override_dependencies, insert_users):

    response = await async_client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


# Add similar test cases for update_user and delete_user endpoints...
