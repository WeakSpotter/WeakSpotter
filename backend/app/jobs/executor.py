from app.database import SessionDep, save
from app.jobs.job import JobInterface, ParallelJob
from app.models.scan import Scan, ScanStatus


class Executor:
    def __init__(self, jobs: list[JobInterface]):
        self.jobs = jobs

    def run(self, scan: Scan, session: SessionDep) -> None:
        scan.status = ScanStatus.running
        try:
            for i, job in enumerate(self.jobs):
                scan.current_step = job.name
                save(session, scan)

                job.run(scan, session)

                scan.progress = int((i / len(self.jobs)) * 100)
                scan.current_step = ""
                save(session, scan)

            print(f"Finished Scanning {scan.url}")

            scan.status = ScanStatus.completed
            scan.progress = 100
            save(session, scan)
        except Exception as e:
            scan.status = ScanStatus.failed
            scan.progress = 100
            save(session, scan)
            print(f"Failed Scanning {scan.url}")
            print(e)

    def mermaid(self):
        """Generates a Mermaid diagram of the jobs and parallel jobs."""
        diagram = ["graph TD"]

        def add_job(job, parent=None):
            job_id = job.name.replace(" ", "_")
            diagram.append(f"{job_id}[{job.name}]")
            if parent:
                parent_id = parent.replace(" ", "_")
                diagram.append(f"{parent_id} --> {job_id}")

            if isinstance(job, ParallelJob):
                for sub_job in job.jobs:
                    add_job(sub_job, job.name)

        for job in self.jobs:
            add_job(job)

        return "\n".join(diagram)
