from app.jobs.abstract_job import Job
from app.jobs.license import License
from app.jobs.tools import execute_command
from app.models.result import Result, Severity


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
        if not self.result:
            return [
                Result(
                    title="No DNS Records Found",
                    severity=Severity.critical,
                    description="No DNS records were found for the domain.",
                )
            ]

        results = []

        if not self.result["a"]:
            results.append(
                Result(
                    title="No A Records Found",
                    severity=Severity.warning,
                    score=0,
                    short_description="No A records were found for the domain.",
                    description="A records are used to point a domain or subdomain to an IPv4 address. Without an A record, the domain will not resolve to an IP address. That would make the domain inaccessible to users on IPv4 networks.",
                    recommendation="Add an A record to the domain's DNS configuration.",
                )
            )
        else:
            results.append(
                Result(
                    title="A Records Found",
                    severity=Severity.info,
                    score=100,
                    short_description="A records were found for the domain.",
                    description="A records are used to point a domain or subdomain to an IPv4 address. The domain will resolve to an IP address.",
                )
            )

        if not self.result["aaaa"]:
            results.append(
                Result(
                    title="No AAAA Records Found",
                    severity=Severity.warning,
                    score=0,
                    short_description="No AAAA records were found for the domain.",
                    description="AAAA records are used to point a domain or subdomain to an IPv6 address. Without an AAAA record, the domain will not resolve to an IPv6 address. That would make the domain inaccessible to users on IPv6 networks.",
                    recommendation="Add an AAAA record to the domain's DNS configuration.",
                )
            )
        else:
            results.append(
                Result(
                    title="AAAA Records Found",
                    severity=Severity.info,
                    score=100,
                    short_description="AAAA records were found for the domain.",
                    description="AAAA records are used to point a domain or subdomain to an IPv6 address. The domain will resolve to an IPv6 address.",
                )
            )

        if self.result["cname"]:
            results.append(
                Result(
                    title="CNAME Record Found",
                    severity=Severity.debug,
                    score=-1,
                    short_description="CNAME record was found for the domain.",
                    description="CNAME records are used to point a domain or subdomain to another domain. The domain will resolve to the target domain.",
                )
            )

        return results
