import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class JoomscanJob(Job):
    requirements = []
    key = "joomscan"
    name = "Joomscan"
    license = License.GPLv3

    def run(self):
        "Scan CMS site with joomscan."
        url = self._scan.url
        self.result = {}

        # Exécute la commande dans le conteneur Docker
        self._raw_output = run_container(
            "ghcr.io/weakspotter/joomscan:latest", f"-u {url}"
        )

    def parse_results(self):
        # Nettoyer les caractères d'échappement ANSI
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", self._raw_output)

        # Supprimer l'en-tête jusqu'à la ligne "Processing https://"
        header_end = re.search(r"Processing https?://[^\n]+\n", clean_output)
        if header_end:
            clean_output = clean_output[
                header_end.end() :
            ]  # Garde seulement le texte après l'en-tête

        # Découper la sortie par sections commençant par [+]
        sections = re.split(r"\[\+\]", clean_output)

        result = {}

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Séparer le titre de la section du reste
            lines = section.split("\n")
            section_title = lines[0].strip()
            details = lines[1:]  # Le reste de la section

            # Nettoyer les préfixes [++] des sous-sections
            sub_sections = [
                re.sub(r"\[\+\+\]\s*", "", line).strip()
                for line in details
                if "[++]" in line
            ]

            # Si des sous-sections existent, les associer à la section principale
            if sub_sections:
                result[section_title] = sub_sections
            else:
                # Sinon, stocker le texte brut en supprimant aussi d'éventuels [++]
                clean_details = [
                    re.sub(r"\[\+\+\]\s*", "", line).strip()
                    for line in details
                    if line.strip()
                ]
                result[section_title] = clean_details

        self.result = result

    def score(self):
        if (self.result.contains("ver 404")): 
            return -1
        else :
            return 0.0

    def definitions(self):
        return []
