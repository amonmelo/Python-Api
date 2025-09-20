# app/main.py
"""
FastAPI bootstrap: liga portas/adapters (repo, hasher, JWT) e monta os routers.
Mantém init_db() dentro de build_app() para funcionar em testes sem eventos de startup.
"""
from fastapi import FastAPI

from app.infrastructure.db import init_db
from app.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_provider import JwtProvider
from app.application.services.user_service import UserService
from app.application.services.auth_service_impl import AuthServiceImpl
from app.interfaces.http.routers.auth_router import get_auth_router
from app.interfaces.http.routers.users_router import get_users_router


def build_app() -> FastAPI:
    """Cria e configura a aplicação, conectando serviços e rotas."""
    init_db()

    repo = SqlAlchemyUserRepository()
    jwtp = JwtProvider()
    hasher = PasswordHasher()

    auth = AuthServiceImpl(hasher, jwtp)
    users = UserService(repo, auth)

    app = FastAPI(
        title="User Manager API",
        version="1.0.0",
        description="API REST para gerenciamento de usuários.",
    )

    app.include_router(get_auth_router(users, auth))
    app.include_router(get_users_router(users, jwtp.secret, jwtp.alg))

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = build_app()
