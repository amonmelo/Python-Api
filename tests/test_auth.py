import os
import uuid
os.environ["JWT_SECRET"] = "testsecret"

from fastapi.testclient import TestClient
from app.main import build_app

client = TestClient(build_app())


def test_login_flow():
    from app.infrastructure.security.password_hasher import PasswordHasher
    from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
    from app.domain.user import User

    repo = SqlAlchemyUserRepository()
    hasher = PasswordHasher()

    # e-mail único para evitar conflito
    email = f"alice_{uuid.uuid4().hex[:8]}@example.com"
    u = User.new(email, "Alice", hasher.hash("Secret123!"))
    repo.add(u)

    r = client.post("/auth/login", json={"email": email, "password": "Secret123!"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token


def test_login_wrong_password():
    from app.infrastructure.security.password_hasher import PasswordHasher
    from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
    from app.domain.user import User

    repo = SqlAlchemyUserRepository()
    hasher = PasswordHasher()

    # e-mail único para evitar conflito
    email = f"eve_{uuid.uuid4().hex[:8]}@example.com"
    u = User.new(email, "Eve", hasher.hash("RightPass123!"))
    repo.add(u)

    r = client.post("/auth/login", json={"email": email, "password": "WrongPass"})
    assert r.status_code == 401
