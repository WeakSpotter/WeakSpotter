import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class VulnXJob(Job):
    requirements = []
    key = "vulnx"
    name = "VulnX"
    license = License.GPLv3

    def run(self):
        "Scan CMS site with VulnX."
        url = self._scan.url
        self.result = {}

        # Run the command in the Docker container
        self._raw_output = run_container(
            "ghcr.io/weakspotter/vulnx:latest", f"--url {url}"
        )

    def parse_results(self):
        # Nettoyer la sortie brute en supprimant les séquences d'échappement ANSI
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", self._raw_output)

        # Séparer la sortie en lignes
        section = clean_output.split("\n")

        # Filtrer les lignes contenant des crochets [ ] et supprimer leur contenu
        filtered_lines = [
            re.sub(
                r"\[.*?\]", "", line
            ).strip()  # Supprime le contenu entre [ ] et nettoie les espaces
            for line in section
            if "[" in line and "]" in line
        ]

        # Stocker le résultat filtré
        self.result = filtered_lines

    def score(self):
        if (self.result.contains("CMS : Unknown")): 
            return -1
        else :
            return 0.0

    def definitions(self):
        return []
