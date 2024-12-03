import docker
from app.jobs.job import Job
from app.jobs.tools import run_container
from app.models.scan import Scan


class CMSmapJob(Job):
    def __init__(self):
        super().__init__("CMSmap", "cmsmap_scan", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan):
        """Scanne un site CMS avec CMSmap."""
        domain = scan.data_dict.get("domain")

        if not domain:
            print("Aucun domaine spécifié.")
            return None

        try:
            result = run_container(
                "ghcr.io/ozeliurs/cmsmap",
                f"http://{domain}",
            )
            return CMSmapJob.parse_cmsmap_output(result)
        except docker.errors.DockerException as e:
            print(f"Erreur lors de l'exécution du conteneur Docker: {e}")
            return None

    @staticmethod
    def parse_cmsmap_output(output: str) -> dict:
        """Analyse la sortie de CMSmap."""
        findings = []
        for line in output.splitlines():
            if "[+]" in line:  # Les résultats importants commencent souvent par "[+]"
                findings.append(line.strip())

        return {"cmsmap_findings": findings}
