from typing import List

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class CMSMapJob(Job):
    requirements: List[str] = ["domain"]
    key: str = "cmsmap"
    name: str = "CMSMap Scan"
    license = License.GPLv3

    def run(self) -> None:
        domain = self._scan.data_dict.get("domain")

        self._raw_output = run_container("ghcr.io/ozeliurs/cmsmap", f"http://{domain}")

    def parse_results(self) -> None:
        self.result = [
            line.strip() for line in self._raw_output.splitlines() if "[+]" in line
        ]

    def score(self) -> float:
        if (self.result.contains("null")): 
            return -1
        else: 
            return 0.0

    def definitions(self):
        return []
