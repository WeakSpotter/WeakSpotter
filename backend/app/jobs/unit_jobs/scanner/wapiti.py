import json

from app.jobs.abstract_job import Job
from app.jobs.container import run_container
from app.jobs.license import License
from app.models.result import Result, Severity

wapiti_severity_map = {
    4: Severity.critical,
    3: Severity.error,
    2: Severity.warning,
    1: Severity.warning,
    0: Severity.info,
}

wapiti_score_mapping = {
    4: -10,
    3: -5,
    2: -3,
    1: -1,
    0: 0,
}


class WapitiJob(Job):
    requirements = []
    key = "wapiti"
    name = "Wapiti"
    license = License.GPLv2

    def run(self):
        "Scan CMS site with Wapiti."
        url = self._scan.url
        self.result = {}

        self._raw_output = run_container(
            "ghcr.io/weakspotter/wapiti:latest",
            f"-u {url} --format json --output /tmp/wapiti-output.json",
        )

    def parse_results(self):
        output_lines = self._raw_output.split("\n")

        target_line_index = next(
            (
                i
                for i, line in enumerate(output_lines)
                if "A report has been generated in the file /tmp/wapiti-output.json"
                in line
            ),
            -1,
        )

        if target_line_index != -1:
            filtered_output = "\n".join(output_lines[target_line_index + 1 :])
            self.result = json.loads(filtered_output)
        else:
            self.result = self._raw_output

    def definitions(self):
        output = []

        for cat in self.result.get("vulnerabilities", []):
            if self.result["vulnerabilities"][cat]:
                # We have a vuln
                for vuln in self.result["vulnerabilities"][cat]:
                    classification = self.result["classifications"][cat]
                    output.append(
                        Result(
                            title=vuln["info"],
                            short_description=cat,
                            severity=wapiti_severity_map[vuln["level"]],
                            description=classification["desc"],
                            recommendation=classification["sol"],
                        )
                    )

        return output
