import os, time
from datetime import timedelta, datetime, timezone
from app.infrastructure.security.jwt_provider import JwtProvider

def test_jwt_create_and_verify_ok(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("JWT_EXP_MINUTES", "1")
    jp = JwtProvider()
    tok = jp.create("user-123", {"role": "admin"})
    payload = jp.verify(tok)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "admin"

def test_jwt_invalid_token_raises(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    jp = JwtProvider()
    # token com segredo diferente => inválido
    other = JwtProvider(secret="outro-secret")
    tok = other.create("user-123")
    try:
        jp.verify(tok)
        assert False, "era pra ter levantado ValueError"
    except ValueError:
        assert True

def test_jwt_expired_token(monkeypatch):
    # expirar já: set exp_minutes=0 e iat/exp no passado
    jp = JwtProvider(secret="x", exp_minutes=0)
    # força expiração no passado
    tok = jp.create("user-123")
    # Pequena espera para garantir exp < now (em ambientes rápidos já basta)
    time.sleep(0.01)
    try:
        jp.verify(tok)
        assert False, "era pra ter expirado"
    except ValueError:
        assert True

def test_aliases(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "alias-secret")
    jp = JwtProvider()
    tok = jp.create_access_token("abc", {"foo": "bar"})
    payload = jp.verify_token(tok)
    assert payload["sub"] == "abc"
    assert payload["foo"] == "bar"
