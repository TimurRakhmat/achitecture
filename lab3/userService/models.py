from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserCreate(BaseModel):
    username: str
    password_hash: str

class UserResponse(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class DbUser(Base):
    __tablename__ = "conf_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("conf_users_username", "username"),
    )