from app.jobs.unit_scans import cmsmap, dns, harvester, http, scanning

common_scans = [
    dns.DomainExtractJob(),
    dns.DNSRecordsJob(),
    dns.WhoisJob(),
    dns.CloudflareDetectJob(),
    scanning.NmapScanJob(),
    http.VersionCheckJob(),
    # nikto.NiktoJob(), # Takes too fucking long
    harvester.EmailHarvesterJob(),
    cmsmap.CMSmapJob(),
]
