from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class ZapitJob(Job):
    requirements = []
    key = "zapit"
    name = "Zapit"
    license = License.Apachev2

    def run(self):
        "Scan CMS site with Zapit."
        url = self._scan.url
        self.result = {}

        # Run the command in the Docker container
        self._raw_output = run_container("ghcr.io/weakspotter/zapit:latest", f"{url}")

    def parse_results(self):
        self.result = self._raw_output

    def definitions(self):
        return []
