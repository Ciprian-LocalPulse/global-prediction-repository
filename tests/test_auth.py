def test_register_creates_user_with_default_reputation(client):
    response = client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "correcthorse123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert body["global_accuracy_score"] == 50.0
    assert body["resolved_forecast_count"] == 0


def test_register_rejects_duplicate_username(client):
    payload = {"username": "bob", "email": "bob@example.com", "password": "correcthorse123"}
    client.post("/auth/register", json=payload)
    second = client.post(
        "/auth/register",
        json={"username": "bob", "email": "someoneelse@example.com", "password": "correcthorse123"},
    )
    assert second.status_code == 400


def test_login_returns_bearer_token(client):
    client.post(
        "/auth/register",
        json={"username": "carol", "email": "carol@example.com", "password": "correcthorse123"},
    )
    response = client.post("/auth/login", data={"username": "carol", "password": "correcthorse123"})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_rejects_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "dave", "email": "dave@example.com", "password": "correcthorse123"},
    )
    response = client.post("/auth/login", data={"username": "dave", "password": "wrongpassword"})
    assert response.status_code == 401


def test_protected_endpoint_requires_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401
