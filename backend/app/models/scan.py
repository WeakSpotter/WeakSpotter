import json
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional

from pydantic import computed_field
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .result import Result
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

    # One to many relationship with results
    results: List["Result"] = Relationship(back_populates="scan")

    @property
    def data_dict(self):
        return json.loads(self.data)

    @data_dict.setter
    def data_dict(self, value):
        self.data = json.dumps(value)

    @computed_field
    @property
    def score(self) -> float:
        """Returns the mean of all result scores ignoring those set to -1."""
        scores = [result.score for result in self.results if result.score != -1]
        return sum(scores) / len(scores) if scores else 0
