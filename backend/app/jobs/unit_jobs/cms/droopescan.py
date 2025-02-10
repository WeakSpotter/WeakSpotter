import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class DroopescanJob(Job):
    requirements = []
    key = "droopescan"
    name = "Droopescan"
    license = License.GPLv2

    def run(self) :
        "Scan csm site with droopescan."
        url = self._scan.url
        self.result = {}

        self._raw_output = run_container(
            "ghcr.io/weakspotter/droopescan:latest", f"scan drupal -u {url}"
        )

    def parse_results(self) :
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', self._raw_output)

        # Supprimer l'en-tête jusqu'à la ligne "Processing https://"
        header_end = re.search(r'Processing https?://[^\n]+\n', clean_output)
        if header_end:
            clean_output = clean_output[header_end.end():]  # Garde seulement le texte après l'en-tête

        # Découper la sortie par sections commençant par [+]
        section = re.split(r'\[\+\]', clean_output)

        self.result = section



    def score(self) :
        return 0.0

    def definitions(self):
        return []
