from __future__ import annotations
import os
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError

class JwtProvider:
    """
    Provedor de JWT com PyJWT.

    Atributos públicos usados no projeto:
      - secret: chave HMAC
      - alg: algoritmo (HS256)

    Métodos principais:
      - create(subject: str, extra: dict | None = None) -> str
      - verify(token: str) -> dict

    Aliases (compatibilidade com AuthServiceImpl/routers):
      - create_access_token(sub: str, extra: dict | None = None) -> str
      - verify_token(token: str) -> dict
    """

    def __init__(self, secret: str | None = None, exp_minutes: int | None = None):
        self.secret = secret or os.getenv("JWT_SECRET", "dev-secret")
        if exp_minutes is None:
            exp_env = os.getenv("JWT_EXP_MINUTES", "60")
            try:
                exp_minutes = int(exp_env)
            except ValueError:
                exp_minutes = 60
        self.exp_minutes = exp_minutes
        self.alg = "HS256"

    # ---------- API "canônica" ----------
    def create(self, subject: str, extra: dict | None = None) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(minutes=self.exp_minutes),
        }
        if extra:
            payload.update(extra)
        return jwt.encode(payload, self.secret, algorithm=self.alg)

    def verify(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.alg])
        except InvalidTokenError as e:
            raise ValueError("invalid or expired token") from e

    # ---------- ALIASES p/ compatibilidade ----------
    def create_access_token(self, sub: str, extra: dict | None = None) -> str:
        return self.create(subject=sub, extra=extra)

    def verify_token(self, token: str) -> dict:
        return self.verify(token)
