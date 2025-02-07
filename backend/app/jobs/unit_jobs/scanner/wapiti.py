from app.jobs.abstract_job import Job
from app.jobs.license import License
from app.jobs.container import run_container

import re

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
            "ghcr.io/weakspotter/wapiti:latest", f"-u {url} --format json --output /tmp/wapiti-output.json"
        )

    def parse_results(self):
        output_lines = self._raw_output.split('\n')

        target_line_index = next(
            (i for i, line in enumerate(output_lines) 
            if "A report has been generated in the file /tmp/wapiti-output.json" in line), 
            -1
        )
    
        if target_line_index != -1:
            filtered_output = '\n'.join(output_lines[target_line_index + 1:])
            self.result = filtered_output
        else:
            self.result = self._raw_output

    def score(self):
        return 0.0
    
    def definitions(self):
        return {}