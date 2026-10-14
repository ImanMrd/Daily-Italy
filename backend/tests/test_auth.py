import uuid

def test_register_and_login(client):
    unique_user = f"user_{uuid.uuid4().hex[:8]}"
    # Register
    res = client.post("/api/auth/register", json={
        "username": unique_user,
        "password": "mypassword123",
        "email": f"{unique_user}@example.com"
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert "access_token" in data
    assert data["user"]["username"] == unique_user
    assert data["user"]["role"] == "user"

    # Duplicate rejection
    res_dup = client.post("/api/auth/register", json={
        "username": unique_user,
        "password": "anotherpassword"
    })
    assert res_dup.status_code == 400

    # Login
    res_login = client.post("/api/auth/login", json={
        "username": unique_user,
        "password": "mypassword123"
    })
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]

    # Verify Profile
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["username"] == unique_user
