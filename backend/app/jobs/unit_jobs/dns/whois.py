from datetime import datetime

import whois
from app.jobs.abstract_job import Job
from app.jobs.license import License


class WhoisJob(Job):
    requirements = ["domain"]
    key = "whois"
    name = "Whois"
    license = License.MIT

    def run(self) -> None:
        domain = self._scan.data_dict.get("domain")

        self._raw_output = whois.whois(domain)

    def parse_results(self) -> None:
        result = dict(self._raw_output)

        # Convert datetime objects to strings
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = [str(item) for item in value]
            elif isinstance(value, dict):
                result[key] = {
                    subkey: str(subvalue) for subkey, subvalue in value.items()
                }
            elif isinstance(value, type(None)):
                result[key] = None
            elif isinstance(value, type):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = str(value)

        self.result = result

    def score(self) -> float:
        if self.result.contains("null"):
            return -1
        else:
            return 0.0

    def definitions(self):
        return []
