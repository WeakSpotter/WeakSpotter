from app.models.scan import Scan, ScanStatus
from app.database import SessionDep, save

from app.jobs.unit_scans import connectivity
from app.jobs.tools import sanitize_url

def scan(scan: Scan, session: SessionDep) -> None:

    scan.status = ScanStatus.running
    scan.url = sanitize_url(scan.url)
    save(session, scan)

    # Stupid work around for sqlite TODO: remove this shiet
    data = scan.data_dict
    data["connectivity"] = connectivity.scan(scan)
    scan.data_dict = data
    save(session, scan)

    print(f"Finished Scanning {scan.url}")

    scan.status = ScanStatus.completed
    save(session, scan)
