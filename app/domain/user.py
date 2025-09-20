from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

@dataclass(frozen=True)
class User:
    id: UUID
    email: str
    name: str
    hashed_password: str
    is_active: bool
    created_at: datetime

    @staticmethod
    def new(email: str, name: str, hashed_password: str) -> "User":
        return User(
            id=uuid4(),
            email=email.lower().strip(),
            name=name.strip(),
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
