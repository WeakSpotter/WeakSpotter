from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List

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
    def __init__(self, jobs: List[Job]):
        self.jobs = jobs

    @property
    def name(self):
        return ",".join([job.name for job in self.jobs])

    def run(self, scan: Scan, session: SessionDep) -> None:
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(job.run, scan, session): job for job in self.jobs
            }
            for future in as_completed(futures):
                job = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Job {job.name} generated an exception: {e}")


class LinearJob(JobInterface):
    def __init__(self, jobs: List[Job]):
        self.jobs = jobs
        self._name = jobs[0].name

    @property
    def name(self):
        return self._name

    def run(self, scan: Scan, session: SessionDep) -> None:
        for job in self.jobs:
            self._name = job.name
            job.run(scan, session)
            print(f"Completed job: {job.name}")
