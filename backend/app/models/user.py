from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .scan import Scan, UserScanLink


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

    # Scans created by this user (one-to-many)
    created_scans: List[Scan] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "[Scan.creator_id]"}
    )

    # Scans shared with this user (many-to-many)
    scans: List[Scan] = Relationship(
        back_populates="users",
        link_model=UserScanLink
    )

class UserCreate(SQLModel):
    username: str
    password: str
