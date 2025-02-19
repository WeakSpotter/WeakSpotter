from typing import List

from app.database import SessionDep, save
from app.executor.abstract_executor import Executor
from app.jobs.abstract_job import Job
from app.models.scan import Scan, ScanStatus


class LinearExecutor(Executor):
    def __init__(self, job_cat: str):
        super().__init__(job_cat)
        self.jobs = self._order_jobs(self.jobs)

    def _order_jobs(self, jobs: List[Job]) -> List[Job]:
        """
        Orders the jobs based on their requirements.

        Args:
            jobs (List[Job]): The list of jobs to order.

        Returns:
            List[Job]: The ordered list of jobs.

        Raises:
            RuntimeError: If there is a circular dependency between jobs
        """
        ordered_jobs = []
        jobs_dict = {job.key: job for job in jobs}

        previous_len = -1

        while jobs_dict:
            # Check for infinite loop - if no jobs were processed in last iteration
            if len(jobs_dict) == previous_len:
                raise RuntimeError("Circular dependency detected between jobs")

            previous_len = len(jobs_dict)

            for key, job in list(jobs_dict.items()):
                if all(
                    req in [j.key for j in ordered_jobs] for req in job.requirements
                ):
                    ordered_jobs.append(job)
                    del jobs_dict[key]

        return ordered_jobs

    def get_jobs(self) -> List[str]:
        return [job.name for job in self.jobs]

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
