from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("name", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

def init_db():
    metadata.create_all(engine)
