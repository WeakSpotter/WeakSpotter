import json

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result, Severity


class SSHAuditJob(Job):
    requirements = ["domain"]
    key = "ssh-audit"
    name = "SSH Audit"
    license = License.MIT

    def run(self) -> None:
        """Performs a scan with SSH_audit on a domain or IP address."""
        domain = self._scan.data_dict.get("domain")

        self._raw_output = run_container(
            image="positronsecurity/ssh-audit",
            command=f"-j {domain}",
            ignore_errors=True,
        )

    def parse_results(self) -> None:
        self.result = json.loads(self._raw_output)        

    def definitions(self):
        if not self.result:
            return [
                Result(
                    title="No SSH Found",
                    severity=Severity.info,
                    score=5,
                    description="No SSH Found results were found for the domain.",
                )
            ]
        if "cves" in self.result and self.result["cves"]: 
            for cve in self.result["cves"]:
                return [
                    Result(
                        title=f"Vulénrabilité SSH {cve}",
                        severity=Severity.critical,
                        score=-10,
                        description=f"La configuration SSH présente une vulnérabilité connue identifiée par {cve}. Il est recommandé de mettre à jour ou de reconfigurer le service SSH pour corriger cette vulnérabilité."
                    )
                ]
