from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .scan import Scan


class Severity(IntEnum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    critical = 4


class Category(IntEnum):
    unknown = 0


class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    severity: Severity = Severity.info
    score: int = 0
    category: Category = Category.unknown
    short_description: str = ""
    description: str = ""
    recommendation: str = ""

    # Add these lines to create the relationship with Scan
    scan_id: Optional[int] = Field(default=None, foreign_key="scan.id")
    scan: Optional["Scan"] = Relationship(back_populates="results")
