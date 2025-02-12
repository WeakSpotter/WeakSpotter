import json
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class UserScanLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    scan_id: Optional[int] = Field(
        default=None, foreign_key="scan.id", primary_key=True
    )


class ScanStatus(IntEnum):
    pending = 0
    running = 1
    completed = 2
    failed = 3


class ScanType(IntEnum):
    simple = 0
    complex = 1


class Scan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: ScanStatus = ScanStatus.pending
    progress: int = 0
    type: ScanType
    current_step: str = ""
    data: str = "{}"

    # Creator relationship (one-to-many)
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional["User"] = Relationship(
        back_populates="created_scans",
        sa_relationship_kwargs={"foreign_keys": "[Scan.creator_id]"},
    )

    # Many-to-many relationship with users
    users: List["User"] = Relationship(back_populates="scans", link_model=UserScanLink)

    @property
    def data_dict(self):
        return json.loads(self.data)

    @data_dict.setter
    def data_dict(self, value):
        self.data = json.dumps(value)


class Severity(IntEnum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    critical = 4


class Result(SQLModel):
    title: str
    score: int
    category: str
    short_description: str
    description: str
    recommendation: str
    severity: Severity
