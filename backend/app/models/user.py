from typing import List, Optional

from app.models.scan import Scan
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    scans: List[Scan] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    username: str
    password: str
