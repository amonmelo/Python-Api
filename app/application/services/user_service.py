from uuid import UUID
from typing import Sequence, Optional, Tuple
from app.domain.user import User
from app.application.ports.user_repository import UserRepository
from app.application.ports.auth_service import AuthService

class UserService:
    def __init__(self, repo: UserRepository, auth: AuthService):
        self.repo = repo
        self.auth = auth

    def create_user(self, email: str, name: str, password: str) -> User:
        if self.repo.get_by_email(email):
            raise ValueError("email already in use")
        hashed = self.auth.hash_password(password)
        user = User.new(email=email, name=name, hashed_password=hashed)
        self.repo.add(user)
        return user

    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.repo.get_by_id(user_id)

    def list_users(self, offset: int, limit: int) -> Tuple[Sequence[User], int]:
        return self.repo.list(offset, limit), self.repo.count()

    def update_user(self, user_id: UUID, name: Optional[str], password: Optional[str]) -> User:
        u = self.repo.get_by_id(user_id)
        if not u:
            raise ValueError("not found")
        hashed = u.hashed_password if not password else self.auth.hash_password(password)
        updated = User(
            id=u.id,
            email=u.email,
            name=name or u.name,
            hashed_password=hashed,
            is_active=u.is_active,
            created_at=u.created_at,
        )
        self.repo.update(updated)
        return updated

    def delete_user(self, user_id: UUID) -> None:
        self.repo.delete(user_id)
