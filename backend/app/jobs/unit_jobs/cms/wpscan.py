from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result


class WPScanJob(Job):
    requirements = []
    key = "wpscan"
    name = "WPScan"
    license = License.WPScan

    def run(self):
        "Scan CMS site with WPScan."
        url = self._scan.url
        self.result = {}

        # Run the command in the Docker container
        self._raw_output = run_container(
            image="wpscanteam/wpscan:latest",
            command=f"--url {url} -f json",
            ignore_errors=True,
        )

    def parse_results(self):
        self.result = self._raw_output

    def definitions(self):
        if self.result.contains("not seem to be running WordPress"):
            return [
                Result(
                    title="WPScan",
                    description="WPScan could not find a WordPress site.",
                )
            ]

        return []
