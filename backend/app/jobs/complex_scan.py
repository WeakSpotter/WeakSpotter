from app.database import SessionDep, save
from app.jobs import common
from app.models.scan import Scan, ScanStatus


def scan(scan: Scan, session: SessionDep) -> None:
    try:
        common.scan(scan, session)

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
