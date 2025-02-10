import json

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


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

    def score(self) -> float:
        return 0.0

    def definitions(self):
        return []
