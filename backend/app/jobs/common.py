from app.jobs.job import LinearJob, ParallelJob
from app.jobs.unit_scans import dns, host_scanning, http

common_scans = [
    dns.DomainExtractJob(),
    ParallelJob([dns.DNSRecordsJob(), dns.WhoisJob()]),
    dns.CloudflareDetectJob(),
    host_scanning.NmapScanJob(),
    http.VersionCheckJob(),
]

common_scans = [
    ParallelJob(
        [
            LinearJob(
                [
                    dns.DomainExtractJob(),
                    ParallelJob(
                        [
                            LinearJob(
                                [
                                    ParallelJob([dns.DNSRecordsJob(), dns.WhoisJob()]),
                                    dns.CloudflareDetectJob(),
                                ]
                            ),
                            host_scanning.NmapScanJob(),
                        ]
                    ),
                    http.VersionCheckJob(),
                ]
            )
        ]
    )
]