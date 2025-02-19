from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class OralyserJob(Job):
    requirements = []
    key = "oralyser"
    name = "Oralyser"
    license = License.GPLv3

    def run(self):
        "Scan CMS site with Oralyser."
        url = self._scan.url
        self.result = {}

        # Run the command in the Docker container
        self._raw_output = run_container(
            "ghcr.io/weakspotter/oralyser:latest", f"-u {url}"
        )

    def parse_results(self):
        self.result = self._raw_output

    def definitions(self):
        return []
