from app.models.scan import Scan, ScanStatus
from app.database import SessionDep, save

from app.jobs import common


def scan(scan: Scan, session: SessionDep) -> None:
    try:
        common.scan(scan, session)

        print(f"Finished Scanning {scan.url}")

        scan.status = ScanStatus.completed
        save(session, scan)
    except Exception as e:
        scan.status = ScanStatus.failed
        save(session, scan)
        print(f"Failed Scanning {scan.url}")
        print(e)
