import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from app.database import SessionDep
from app.jobs.abstract_job import Job
from app.models.scan import Scan


class Executor(ABC):
    IMPORT_PREFIX = "app.jobs.unit_jobs"
    CONF_PATH = Path(__file__).parent / "config.json"
    jobs: List[Job]

    def __init__(self, job_cat: str):
        self.jobs = [self._import_job(job)() for job in self._read_config(job_cat)]

    @abstractmethod
    def get_jobs(self) -> List[str]:
        """
        Returns the list of jobs for the executor.

        :return: A list of job names.
        """

    @abstractmethod
    def run(self, scan: Scan, session: SessionDep) -> None:
        pass

    def _read_config(self, job_cat) -> List[str]:
        """
        Reads the configuration file and retrieves the list of jobs for the given category.

        Args:
            job_cat (str): The category of jobs to retrieve from the configuration file.

        Returns:
            List[str]: A list of job paths for the specified category.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            KeyError: If the specified category is not found in the configuration file.
        """
        try:
            return json.loads(self.CONF_PATH.read_text())[job_cat]
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {self.CONF_PATH}")
        except KeyError:
            raise KeyError(f"Category {job_cat} not found in config file")

    def _import_job(self, job_path: str) -> type:
        """
        Imports a job class from a given job path.

        Args:
            job_path (str): The dot-separated path to the job class.

        Returns:
            type: The imported job class.
        """
        job = f"{self.IMPORT_PREFIX}.{job_path}"
        job = job.split(".")
        module = ".".join(job[:-1])
        job_name = job[-1]
        job_module = __import__(module, fromlist=[job_name])
        job_class = getattr(job_module, job_name)
        return job_class
