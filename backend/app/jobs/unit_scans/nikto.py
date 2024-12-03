import docker
from app.jobs.job import Job
from app.jobs.tools import run_container
from app.models.scan import Scan


class NiktoJob(Job):
    def __init__(self):
        super().__init__("Nikto", "nikto_scan", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan):
        """Performs a scan with Nikto on a domain or IP address."""
        domain = scan.data_dict.get("domain")
        if not domain:
            print("Aucun domaine spécifié.")
            return None

        try:
            result = run_container("ghcr.io/ozeliurs/nikto", f"nikto -h {domain}")
            return NiktoJob.parse_nikto_output(result)
        except docker.errors.DockerException as e:
            print(f"Erreur lors de l'exécution du conteneur Docker: {e}")
            return None

    @staticmethod
    def parse_nikto_output(output: str) -> dict:
        """Analyze the Nikto report and extract useful information."""
        findings = [
            line.strip() for line in output.splitlines() if line.startswith("+")
        ]
        return {"nikto_findings": findings}
