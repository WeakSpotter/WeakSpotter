from app.database import SessionDep, save
from app.jobs.tools import add_data, sanitize_url
from app.jobs.unit_scans import dns, host_scanning
from app.models.scan import Scan, ScanStatus

dns_scans = [dns.domain_extract, dns.dns_records, dns.whois, dns.cloudflare_detect]
host_scans = [host_scanning.nmap_scan]


def scan(scan: Scan, session: SessionDep) -> None:
    scan.status = ScanStatus.running
    scan.url = sanitize_url(scan.url)
    save(session, scan)

    scans = dns_scans + host_scans

    for s in scans:
        key, value = s(scan)
        add_data(scan, key, value)
        save(session, scan)
