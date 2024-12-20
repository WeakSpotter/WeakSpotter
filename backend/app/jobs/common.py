from app.jobs.unit_scans import cmsmap, dns, harvester, http, scanning, ssh

common_scans = [
    dns.DomainExtractJob(),
    dns.DNSRecordsJob(),
    dns.WhoisJob(),
    dns.CloudflareDetectJob(),
    scanning.NmapScanJob(),
    http.VersionCheckJob(),
    ssh.SshAuditJob(),
    # nikto.NiktoJob(), # Takes too fucking long
    harvester.EmailHarvesterJob(),
    cmsmap.CMSmapJob(),
]
