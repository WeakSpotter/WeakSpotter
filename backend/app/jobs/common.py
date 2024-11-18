from app.models.scan import Scan, ScanStatus
from app.database import SessionDep, save

from app.jobs.unit_scans import connectivity
from app.jobs.tools import sanitize_url

def scan(scan: Scan, session: SessionDep) -> None:
    scan.status = ScanStatus.running
    scan.url = sanitize_url(scan.url)
    save(session, scan)

    scans = [connectivity.http_status, connectivity.ip]

    for s in scans:
        data = scan.data_dict
        data[s.__name__] = s(scan)
        scan.data_dict = data
        save(session, scan)
