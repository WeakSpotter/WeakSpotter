import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


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
            command= f"--url {url}",
            ignore_errors=True,
        )

    def parse_results(self):
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', self._raw_output)

        section = clean_output.split('\n')
        skip_line = 13
        section = section[skip_line:]

        self.result = section


    def score(self):
        return 0.0

    def definitions(self):
        return []
