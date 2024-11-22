from abc import ABC, abstractmethod
from typing import Any, Callable

from app.database import SessionDep, save
from app.jobs.tools import add_data
from app.models.scan import Scan


class JobInterface(ABC):
    @abstractmethod
    def run(self, scan: Scan, session: SessionDep) -> None:
        pass


class Job(JobInterface):
    def __init__(self, name: str, key: str, fun: Callable[[Scan], Any]):
        self.name = name
        self.key = key
        self.fun = fun

    def run(self, scan: Scan, session: SessionDep) -> None:
        res = self.fun(scan)
        add_data(scan, self.key, res)
        save(session, scan)


class ParallelJob(JobInterface):
    def __init__(self, jobs: list[Job]):
        self.jobs = jobs

    @property
    def name(self):
        return ",".join([job.name for job in self.jobs])

    def run(self, scan: Scan, session: SessionDep) -> None:
        for job in self.jobs:
            job.run(scan, session)
