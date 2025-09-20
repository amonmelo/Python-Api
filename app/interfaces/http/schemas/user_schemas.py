from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserCreateIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)
    password: str = Field(min_length=8)

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    created_at: datetime

class UserUpdateIn(BaseModel):
    name: str | None = None
    password: str | None = None

class PaginatedUsers(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[UserOut]
