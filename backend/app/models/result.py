from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    pass


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
    score: int = -1
    category: Category = Category.unknown
    short_description: str = ""
    description: str = ""
    recommendation: str = ""
