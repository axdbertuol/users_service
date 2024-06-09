def test_create_user(client, session):
    user_create_request = {
        "email": "tes2t@example.com",
        "username": "teste",
        "password": "pass2word",
        "full_name": "sgsd df",
    }
    response = client.post("/api/v1/users/", json=user_create_request)
    assert response.status_code == 201
    json_resp = response.json()
    assert json_resp["success"] is True
    assert "data" in json_resp
    assert "id" in json_resp["data"]
    assert user_create_request["email"] == json_resp["data"]["email"]


def test_update_user(client, session, insert_users):
    user_update_request = {
        "full_name": "xis",
    }
    response = client.put("/api/v1/users/1", json=user_update_request)
    assert response.status_code == 200
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == user_update_request["full_name"]


def test_read_user(client, session, insert_users):

    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


def test_read_users(client, session, insert_users):

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


def test_delete_user(client, session, insert_users):

    response = client.delete("/api/v1/users/2")
    assert response.status_code == 200
    response = client.get("/api/v1/users/2")
    assert response.status_code == 404


# Add similar test cases for update_user and delete_user endpoints...
