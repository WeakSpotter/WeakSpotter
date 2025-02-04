from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License


class JoomscanJob(Job):
    requirements = []
    key = "joomscan"
    name = "Joomscan"
    license = License.GPLv3

    def run(self) :
        "Scan csm site with joomscan."
        url = self._scan.url
        self.result = {}

        self._raw_output = run_container(
            "ghcr.io/weakspotter/joomscan:latest", f"-u {url}"
        )
    def parse_results(self) -> None:
        self.result = self._raw_output

    def score(self) :
        return 0.0

    def definitions(self):
        return {}
