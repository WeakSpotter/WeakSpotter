from urllib.parse import urlparse

from app.jobs.abstract_job import Job


class DomainJob(Job):
    requirements = []
    key = "domain"
    name = "Domain Extract"

    def run(self):
        self.result = urlparse(self._scan.url).netloc

    def parse_results(self):
        pass

    def definitions(self):
        return {}

    def score(self):
        return 100.0
