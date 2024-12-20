import docker
from app.jobs.container import run_container
from app.jobs.job import Job
from app.models.scan import Scan
import re


class Sublist3rJob(Job):
    def __init__(self):
        super().__init__("Sublist3r", "sublist3r", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan):
        "Scan a domain with sublist3r."
        domain = scan.data_dict.get("domain")

        if not domain:
            print("Aucun domain specifié.")
            return None

        try:
            result = run_container(
                "ghcr.io/weakspotter/sublist3r:latest", f"-d {domain}"
            )
            return Sublist3rJob.parse_sublist3r_output(result)
        except docker.errors.DockerException as e:
            print(f"Erreur lors de l'éxecution du conteneur Docker: {e}")
            return None

    @staticmethod
    def parse_sublist3r_output(output: str) -> dict:
        "Parse the output of sublist3r and remove ANSI escape codes."
        findings = []
        append_lines = False
        ansi_escape = re.compile(
            r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
        )  # Pattern to match ANSI codes
        for line in output.splitlines():
            if "Total Unique Subdomains Found:" in line:
                append_lines = True
                continue
            if append_lines:
                # Remove ANSI escape codes and add to findings
                clean_line = ansi_escape.sub("", line).strip()
                findings.append(clean_line)

        return {"sublist3r_findings": findings}
