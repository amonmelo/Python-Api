import os
os.environ["JWT_SECRET"] = "testsecret"

from fastapi.testclient import TestClient
from app.main import build_app

client = TestClient(build_app())


def _login():
    from app.infrastructure.security.password_hasher import PasswordHasher
    from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
    from app.domain.user import User
    import uuid

    repo = SqlAlchemyUserRepository()
    hasher = PasswordHasher()

    # e-mail único por execução para não bater no UNIQUE(email)
    email = f"bob_{uuid.uuid4().hex[:8]}@example.com"

    u = User.new(email, "Bob", hasher.hash("Secret123!"))
    repo.add(u)

    r = client.post("/auth/login", json={"email": email, "password": "Secret123!"})
    return r.json()["access_token"]


def test_users_crud_and_pagination():
    token = _login()
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r = client.post("/users", headers=headers, json={
        "email": "new@example.com", "name": "New", "password": "Password123!"
    })
    assert r.status_code == 201
    user_id = r.json()["id"]

    # get
    r = client.get(f"/users/{user_id}", headers=headers)
    assert r.status_code == 200

    # list paginated
    r = client.get("/users?offset=0&limit=10", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "total" in data and "items" in data

    # update
    r = client.patch(f"/users/{user_id}", headers=headers, json={"name": "Updated"})
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"

    # delete
    r = client.delete(f"/users/{user_id}", headers=headers)
    assert r.status_code == 204


def test_auth_rejects_invalid_token():
    # token inválido -> 401
    r = client.get("/users", headers={"Authorization": "Bearer invalid.token"})
    assert r.status_code == 401


def test_get_user_not_found():
    import uuid

    token = _login()
    headers = {"Authorization": f"Bearer {token}"}
    # UUID aleatório não existente -> 404
    r = client.get(f"/users/{uuid.uuid4()}", headers=headers)
    assert r.status_code == 404
