from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result


class DroopescanJob(Job):
    requirements = []
    key = "droopescan"
    name = "Droopescan"
    license = License.GPLv2

    def run(self):
        "Scan csm site with droopescan."
        url = self._scan.url
        self.result = {}

        self._raw_output = run_container(
            "ghcr.io/weakspotter/droopescan:latest", f"scan drupal -u {url} -o json"
        )

    def parse_results(self):
        self.result = self._raw_output

    def definitions(self):
        if self.result.contains("is not running drupal"):
            return [
                Result(
                    title="Droopescan",
                    description="Droopescan could not find a Drupal site.",
                )
            ]

        return []
