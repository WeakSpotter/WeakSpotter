import json
from datetime import datetime
from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel


class ScanStatus(IntEnum):
    pending = 0
    running = 1
    completed = 2
    failed = 3


class Scan(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: ScanStatus = ScanStatus.pending
    progress: int = 0
    current_step: str = ""
    data: str = "{}"
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

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
