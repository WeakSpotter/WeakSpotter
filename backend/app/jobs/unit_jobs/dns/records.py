from app.jobs.abstract_job import Job
from app.jobs.license import License
from app.jobs.tools import execute_command


class DNSRecordsJob(Job):
    requirements = ["domain"]
    key = "dns_records"
    name = "DNS Records"
    license = License.MPLv2

    def run(self) -> None:
        domain = self._scan.data_dict.get("domain")

        commands = {
            "a": f"dig +short {domain} A | grep '^[.0-9]*$'",
            "aaaa": f"dig +short {domain} AAAA | grep '^[0-9a-fA-F:]*$'",
            "cname": f"dig +short {domain} CNAME",
        }

        results = {key: execute_command(command) for key, command in commands.items()}
        self.result = results

    def parse_results(self) -> None:
        pass

    def definitions(self):
        return []
