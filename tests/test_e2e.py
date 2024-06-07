def test_create_user(client, session):
    user_create_request = {
        "email": "tes2t@example.com",
        "username": "teste",
        "password": "pass2word",
        "full_name": "sgsd df",
    }
    response = client.post("/api/v1/users/", json=user_create_request)
    assert response.status_code == 201
    assert response.json()["success"] is True
    assert "data" in response.json()


def test_read_user(client, session, insert_users):

    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()


# Add similar test cases for update_user and delete_user endpoints...
