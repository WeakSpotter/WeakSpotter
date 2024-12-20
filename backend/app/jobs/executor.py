import json
from pathlib import Path
from typing import List

from app.database import SessionDep, save
from app.jobs.abstract_job import Job
from app.models.scan import Scan, ScanStatus


class Executor:
    IMPORT_PREFIX = "app.jobs.unit_jobs"
    CONF_PATH = Path(__file__).parent / "config.json"

    def __init__(self, job_cat: str):
        self.jobs = [self._import_job(job)() for job in self._read_config(job_cat)]
        self.jobs = self._order_jobs(self.jobs)

    def _read_config(self, job_cat) -> List[str]:
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

    def _order_jobs(self, jobs: list[Job]) -> list[Job]:
        """
        Orders the jobs based on their requirements.

        Args:
            jobs (list[Job]): The list of jobs to order.

        Returns:
            list[Job]: The ordered list of jobs.
        """
        ordered_jobs = []
        jobs_dict = {job.key: job for job in jobs}

        while jobs_dict:
            for key, job in list(jobs_dict.items()):
                if all(
                    req in [j.key for j in ordered_jobs] for req in job.requirements
                ):
                    ordered_jobs.append(job)
                    del jobs_dict[key]

        return ordered_jobs

    def run(self, scan: Scan, session: SessionDep) -> None:
        scan.status = ScanStatus.running

        for i, job in enumerate(self.jobs):
            scan.current_step = job.name
            save(session, scan)

            try:
                job.scan(scan)
            except Exception as e:
                print(f"Error running job {job.name}: {e}")
                scan.status = ScanStatus.failed
                scan.progress = 100
                save(session, scan)
                return

            scan.progress = int((i / len(self.jobs)) * 100)
            scan.current_step = ""
            save(session, scan)

        scan.status = ScanStatus.completed
        scan.progress = 100
        save(session, scan)
