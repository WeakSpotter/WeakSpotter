import docker
from app.jobs.container import run_container
from app.jobs.job import Job
from app.models.scan import Scan


class NiktoJob(Job):
    def __init__(self):
        super().__init__("SshAudit", "ssh_audit", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan):
        """Performs a scan with SSH_audit on a domain or IP address."""
        domain = scan.data_dict.get("domain")
        if not domain:
            print("Aucun domaine spécifié.")
            return None

        try:
            result = run_container("positronsecurity/ssh-audit", f"-j {domain}")
            return SshAuditJob.parse_ssh_output(result)
        except docker.errors.DockerException as e:
            print(f"Erreur lors de l'exécution du conteneur Docker: {e}")
            return None

    @staticmethod
    def parse_ssh_output(output: str) -> dict:
        """Analyze the SSH Audit report and extract useful information."""
        findings = [
            line.strip() for line in output.splitlines() if line.startswith("+")
        ]
        return {"ssh_findings": findings}
