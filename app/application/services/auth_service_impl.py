from app.application.ports.auth_service import AuthService
from app.infrastructure.security.jwt_provider import JwtProvider
from app.infrastructure.security.password_hasher import PasswordHasher

class AuthServiceImpl(AuthService):
    def __init__(self, hasher: PasswordHasher, jwt: JwtProvider):
        self.hasher = hasher
        self.jwt = jwt

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.hasher.verify(plain, hashed)

    def hash_password(self, plain: str) -> str:
        return self.hasher.hash(plain)

    def create_access_token(self, sub: str) -> str:
        return self.jwt.create_access_token(sub=sub)
