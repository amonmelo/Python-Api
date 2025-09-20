from typing import Optional, Sequence, List
from uuid import UUID
from sqlalchemy import select, func, delete, update, insert
from app.domain.user import User
from app.infrastructure.db import SessionLocal, users_table

class SqlAlchemyUserRepository:
    def __init__(self):
        self.Session = SessionLocal

    def _row_to_user(self, r) -> User:
        # SQLAlchemy Row -> access by mapping
        row = r._mapping if hasattr(r, "_mapping") else r
        return User(
            id=UUID(row["id"]),
            email=row["email"],
            name=row["name"],
            hashed_password=row["hashed_password"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        with self.Session() as s:
            row = s.execute(select(users_table).where(users_table.c.id == str(user_id))).fetchone()
            return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        with self.Session() as s:
            row = s.execute(select(users_table).where(users_table.c.email == email.lower())).fetchone()
            return self._row_to_user(row) if row else None

    def list(self, offset: int, limit: int) -> Sequence[User]:
        with self.Session() as s:
            rows = s.execute(
                select(users_table).order_by(users_table.c.created_at.desc()).offset(offset).limit(limit)
            ).fetchall()
            return [self._row_to_user(r) for r in rows]

    def count(self) -> int:
        with self.Session() as s:
            return int(s.execute(select(func.count()).select_from(users_table)).scalar_one())

    def add(self, user: User) -> None:
        with self.Session() as s:
            s.execute(insert(users_table).values(
                id=str(user.id), email=user.email, name=user.name,
                hashed_password=user.hashed_password, is_active=user.is_active, created_at=user.created_at
            ))
            s.commit()

    def update(self, user: User) -> None:
        with self.Session() as s:
            s.execute(update(users_table).where(users_table.c.id==str(user.id)).values(
                name=user.name, hashed_password=user.hashed_password, is_active=user.is_active
            ))
            s.commit()

    def delete(self, user_id: UUID) -> None:
        with self.Session() as s:
            s.execute(delete(users_table).where(users_table.c.id==str(user_id)))
            s.commit()
