from urllib.parse import urlparse

from app.jobs.abstract_job import Job
from app.jobs.license import License


class DomainJob(Job):
    requirements = []
    key = "domain"
    name = "Domain Extract"
    license = License.Empty

    def run(self):
        self.result = urlparse(self._scan.url).netloc

    def parse_results(self):
        pass

    def definitions(self):
        return {}

    def score(self):
        return 100.0
