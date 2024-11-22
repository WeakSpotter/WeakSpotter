from app.jobs.unit_scans import dns, host_scanning, http

dns_scans = [
    dns.DomainExtractJob(),
    dns.DNSRecordsJob(),
    dns.WhoisJob(),
    dns.CloudflareDetectJob(),
]
host_scans = [host_scanning.NmapScanJob()]
http_scans = [http.VersionCheckJob()]
common_scans = dns_scans + host_scans + http_scans
