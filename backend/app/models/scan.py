import json

from enum import IntEnum
from datetime import datetime

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel

class ScanStatus(IntEnum):
    pending = 0
    running = 1
    completed = 2
    failed = 3

class Scan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: ScanStatus = ScanStatus.pending
    data: str = "{}"

    @property
    def data_dict(self):
        return json.loads(self.data)

    @data_dict.setter
    def data_dict(self, value):
        self.data = json.dumps(value)
