from app.models.scan import Scan, ScanStatus
from app.database import SessionDep, save

from app.jobs.unit_scans import connectivity

def scan(scan: Scan, session: SessionDep) -> None:
    raise NotImplementedError("This is a placeholder function")
