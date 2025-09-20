from passlib.context import CryptContext

class PasswordHasher:
    def __init__(self):
        self.ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain: str) -> str:
        return self.ctx.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.ctx.verify(plain, hashed)
