import pytest
from httpx import ASGITransport, AsyncClient
from ..main import app


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:3336"
    ) as client:
        user_create_request = {
            "email": "tes2t@example.com",
            "username": "teste",
            "password": "pass2word",
            "full_name": "sgsd df",
        }
        response = await client.post("/api/v1/users/", json=user_create_request)
        assert response.status_code == 201
        assert response.json()["success"] is True
        assert "data" in response.json()


@pytest.mark.asyncio
async def test_read_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:3336"
    ) as client:
        response = await client.get("/api/v1/users/1")
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "data" in response.json()


# Add similar test cases for update_user and delete_user endpoints...
