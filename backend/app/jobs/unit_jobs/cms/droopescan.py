import json

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result, Severity


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
            "ghcr.io/weakspotter/droopescan:latest",
            f"scan drupal -u {url} -o json --hide-progressbar",
        )

    def parse_results(self):
        try:
            self.result = json.loads(self._raw_output)
        except json.JSONDecodeError:
            if "is not running drupal" in self._raw_output:
                self.result = {"error": "is not running drupal"}
            else:
                self.result = {"error": "unknown", "content": self._raw_output}

    def definitions(self):
        if "error" in self.result:
            if self.result["error"] == "is not running drupal":
                # Not a drupal website
                return [
                    Result(
                        title="Droopescan",
                        description="Droopescan could not find a Drupal site.",
                    )
                ]

            # The tool fucked up
            return [
                Result(
                    title="Droopescan",
                    description="An unknown error occurred.",
                    severity=Severity.debug,
                )
            ]

        output = []

        return output
