from app.database import SessionDep, save
from app.jobs.tools import add_data, sanitize_url
from app.jobs.unit_scans import dns, host_scanning, http
from app.models.scan import Scan, ScanStatus

dns_scans = [dns.domain_extract, dns.dns_records, dns.whois, dns.cloudflare_detect]
host_scans = [host_scanning.nmap_scan]
http_scans = [http.version_check]


def scan(scan: Scan, session: SessionDep) -> None:
    scan.status = ScanStatus.running
    scan.url = sanitize_url(scan.url)
    save(session, scan)

    scans = dns_scans + host_scans + http_scans
    total_scans = len(scans)

    for index, s in enumerate(scans):
        scan.current_step = s.__name__
        scan.progress = int((index / total_scans) * 100)
        save(session, scan)

        key, value = s(scan)
        add_data(scan, key, value)
        save(session, scan)
