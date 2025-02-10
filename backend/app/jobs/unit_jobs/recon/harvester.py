import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class EmailHarvesterJob(Job):
    requirements = ["domain"]
    key = "email_harvester"
    name = "Email Harvester"
    license = License.GPLv3

    def run(self) -> None:
        """Performs an email harvesting scan with theHarvester."""
        domain = self._scan.data_dict.get("domain")

        self._raw_output = run_container(
            "ghcr.io/ozeliurs/theharvester",
            f"-d {domain} -l 100 -b crtsh",
            entrypoint="/root/.local/bin/theHarvester",
        )

    def parse_results(self) -> None:
        """Parses the output of theHarvester and extracts emails."""
        email_pattern = re.compile(
            r"[-\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        )
        self.result = sorted(set(email_pattern.findall(self._raw_output)))

    def score(self) -> float:
        return 0.0

    def definitions(self):
        return []
