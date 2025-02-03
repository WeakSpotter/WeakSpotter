import re

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class Sublist3rJob(Job):
    requirements = ["domain"]
    key = "sublist3r"
    name = "Sublist3r Scan"
    license = License.GPLv2

    def run(self):
        "Scan a domain with sublist3r."
        domain = self._scan.data_dict.get("domain")

        self._raw_output = run_container(
            "ghcr.io/weakspotter/sublist3r:latest", f"-d {domain}"
        )

    def parse_results(self):
        """Parse the output of sublist3r and extract subdomains."""
        self.result = []
        ansi_escape = re.compile(
            r"\x1B[@-_][0-?]*[ -/]*[@-~]"
        )  # Pattern to match ANSI codes
        subdomains_section = False

        for line in self._raw_output.splitlines():
            if "Total Unique Subdomains Found:" in line:
                subdomains_section = True
                continue
            if subdomains_section:
                clean_line = ansi_escape.sub("", line).strip()
                if clean_line:  # Ensure the line is not empty
                    self.result.append(clean_line)

    def score(self):
        return 0.0

    def definitions(self):
        return {}
