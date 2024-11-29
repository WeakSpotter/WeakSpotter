from app.database import SessionDep
from app.jobs import common
from app.jobs.executor import Executor
from app.models.scan import Scan


def scan(scan: Scan, session: SessionDep) -> None:
    jobs = common.test_scan

    Executor(jobs).run(scan, session)
