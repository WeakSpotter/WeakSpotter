from app.jobs.job import LinearJob, ParallelJob
from app.jobs.unit_scans import dns, http, nikto
from backend.app.jobs.unit_scans import harvester, scanning


common_scans = [
    dns.DomainExtractJob(),
    ParallelJob([dns.DNSRecordsJob(), dns.WhoisJob()]),
    dns.CloudflareDetectJob(),
    scanning.NmapScanJob(),
    http.VersionCheckJob(),
]

common_scans = [
    ParallelJob(
        [
            LinearJob(
                [
                    dns.DomainExtractJob(),
                    harvester.EmailHarvesterJob(),
                    nikto.NiktoJob(),
                    ParallelJob(
                        [
                            LinearJob(
                                [
                                    ParallelJob([dns.DNSRecordsJob(), dns.WhoisJob()]),
                                    dns.CloudflareDetectJob(),
                                ]
                            ),
                            scanning.NmapScanJob(),
                        ]
                    ),
                    http.VersionCheckJob(),
                ]
            )
        ]
    )
]

test_scan = [
    LinearJob(
                [
                    dns.DomainExtractJob(),
                    http.VersionCheckJob(),
                ]
            )
]